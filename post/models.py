import os
import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify


class Post(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="posts"
    )
    title = models.CharField(max_length=255)
    content = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now=True)
    people_who_liked = models.ManyToManyField(get_user_model(), related_name="likes")

    def __str__(self):
        return (
            f"Post by {self.user.first_name} {self.user.last_name} at {self.created_at}"
        )


def profile_picture_file_path(instance, filename: str):
    title = instance.post.title
    directory = title[0]
    _, extension = os.path.splitext(filename)

    filename = f"{slugify(title)}-{uuid.uuid4()}.{extension}"

    return os.path.join("uploads/prof-pic/", directory, filename)


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=profile_picture_file_path, blank=True)


class PostComment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.CharField(max_length=400)
