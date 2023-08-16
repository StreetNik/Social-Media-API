import re

from rest_framework import serializers

from post.models import Post, PostImage, PostComment, HashTag


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ["id", "post", "image"]


class HashTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashTag
        fields = ["id", "name"]


class PostListSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField(
        method_name="get_likes_count", read_only=True
    )
    images = PostImageSerializer(many=True, read_only=True)
    hash_tags = HashTagSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(
            max_length=10000, allow_empty_file=False, use_url=False
        ),
        write_only=True,
        required=False,
    )

    time_to_create = serializers.DateTimeField(
        write_only=True,
        required=False,
    )

    class Meta:
        model = Post
        fields = [
            "id",
            "user",
            "title",
            "content",
            "images",
            "uploaded_images",
            "created_at",
            "likes_count",
            "hash_tags",
            "time_to_create"
        ]
        read_only_fields = ["user"]

    def get_likes_count(self, obj) -> int:
        return obj.people_who_liked.count()

    def find_hashtags_in_text(self, string):
        hashtag_pattern = r'#(\w+)'
        hashtags = re.findall(hashtag_pattern, string)

        return hashtags

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images", None)
        user = self.context["request"].user
        validated_data.pop("hash_tags", None)
        time_to_create = validated_data.pop("time_to_create", None)

        post = Post.objects.create(user=user, **validated_data)

        hash_tags = self.find_hashtags_in_text(post.content)

        if uploaded_images:
            for image in uploaded_images:
                new_post_images = PostImage.objects.create(image=image, post=post)
                new_post_images.save()

        for hashtag in hash_tags:
            new_hash_tag, _ = HashTag.objects.get_or_create(name=hashtag)
            post.hash_tags.add(HashTag.objects.get(name=hashtag))

        if time_to_create:
            Post.objects.filter(pk=post.pk).update(created_at=time_to_create)

        return post


class PostDetailSerializer(serializers.ModelSerializer):
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(
            max_length=10000, allow_empty_file=False, use_url=False
        ),
        write_only=True,
        required=False,
    )

    class Meta:
        model = Post
        fields = [
            "id",
            "user",
            "title",
            "content",
            "images",
            "uploaded_images",
            "created_at",
            "people_who_liked",
        ]
        read_only_fields = ("created_at", "user", "people_who_liked")

    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop("uploaded_images", None)

        # Update the post fields
        instance.title = validated_data.get("title", instance.title)
        instance.content = validated_data.get("content", instance.content)
        instance.save()

        if uploaded_images:
            # Remove existing images
            instance.images.all().delete()

            # Create and associate new images
            for image in uploaded_images:
                new_post_images = PostImage.objects.create(image=image, post=instance)
                new_post_images.save()

        return instance


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = ["id", "user", "post", "content", "created_at"]
        read_only_fields = ("created_at", "user", "post", "id")
