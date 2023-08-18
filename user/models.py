import os
import uuid

from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Users require an email field")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


def profile_picture_file_path(instance, filename: str):
    email = instance.user.email.split("@")[0]
    directory = email[0]
    _, extension = os.path.splitext(filename)

    filename = f"{slugify(email)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads", "prof-pic", directory, filename)


MARRIAGE_STATUSES = (
    ("none", ""),
    ("single", "Single"),
    ("married", "Married"),
    ("relationship", "In relationship"),
    ("looking", "Looking for someone"),
)

SEX_LIST = (
    ("none", ""),
    ("men", "Men"),
    ("women", "Women"),
)


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=False,
        related_name="profile",
    )
    profile_picture = models.ImageField(upload_to=profile_picture_file_path, blank=True)
    bio = models.CharField(max_length=255, blank=True)
    marriage_status = models.CharField(
        max_length=255, choices=MARRIAGE_STATUSES, default="none"
    )
    sex = models.CharField(max_length=50, choices=SEX_LIST, default="none")

    followers = models.ManyToManyField(User, related_name="following", blank=True)
    following = models.ManyToManyField(User, related_name="followers", blank=True)

    def get_followers_count(self) -> int:
        return self.followers.count()

    def get_following_count(self) -> int:
        return self.following.count()

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"
