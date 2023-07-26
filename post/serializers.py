from rest_framework import serializers

from post.models import Post, PostImage, PostComment


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ["id", "post", "image"]


class PostListSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField(
        method_name="get_likes_count", read_only=True
    )
    images = PostImageSerializer(many=True, read_only=True)
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
            "likes_count",
        ]
        read_only_fields = ["user"]

    def get_likes_count(self, obj):
        return obj.people_who_liked.count()

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images", None)
        user = self.context["request"].user
        post = Post.objects.create(user=user, **validated_data)
        if uploaded_images:
            for image in uploaded_images:
                new_post_images = PostImage.objects.create(image=image, post=post)
                new_post_images.save()

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
