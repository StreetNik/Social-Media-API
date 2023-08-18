# Generated by Django 4.2.1 on 2023-07-28 09:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("post", "0004_postcomment_created_at"),
    ]

    operations = [
        migrations.CreateModel(
            name="HashTag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name="post",
            name="hash_tags",
            field=models.ManyToManyField(related_name="hash_tags", to="post.hashtag"),
        ),
    ]
