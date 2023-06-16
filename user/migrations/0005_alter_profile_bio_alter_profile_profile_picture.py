# Generated by Django 4.2.1 on 2023-06-16 11:32

from django.db import migrations, models
import user.models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0004_alter_profile_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="bio",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name="profile",
            name="profile_picture",
            field=models.ImageField(
                blank=True, upload_to=user.models.profile_picture_file_path
            ),
        ),
    ]
