# Generated by Django 4.2.1 on 2023-05-24 03:31

from django.db import migrations
import user.models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="user",
            managers=[
                ("objects", user.models.UserManager()),
            ],
        ),
    ]
