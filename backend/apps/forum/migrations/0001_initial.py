# Generated by Django 4.1.4 on 2022-12-27 20:27

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import martor.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
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
                (
                    "name",
                    models.CharField(
                        max_length=100,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Input must contain only alphabetic characters",
                                regex="^[A-Za-z]+$",
                            )
                        ],
                        verbose_name="Name of the category",
                    ),
                ),
            ],
            options={
                "verbose_name": "Category",
                "verbose_name_plural": "Categories",
            },
        ),
        migrations.CreateModel(
            name="Post",
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
                (
                    "content_html",
                    models.TextField(
                        auto_created=True,
                        blank=True,
                        max_length=400,
                        verbose_name="Post html content",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        max_length=100,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Input must contain only alphabetic characters and spaces",
                                regex="^[a-zA-Z ]+$",
                            )
                        ],
                        verbose_name="Post title",
                    ),
                ),
                (
                    "content_markdown",
                    martor.models.MartorField(
                        max_length=300, verbose_name="Post markdown content"
                    ),
                ),
                (
                    "slug",
                    django_extensions.db.fields.AutoSlugField(
                        blank=True,
                        editable=False,
                        populate_from=["title", "get_slug_datetime"],
                        verbose_name="Post slug",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Updated at"),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="post",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="post",
                        to="forum.category",
                    ),
                ),
            ],
            options={
                "verbose_name": "Post",
                "verbose_name_plural": "Posts",
            },
        ),
        migrations.CreateModel(
            name="Reply",
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
                (
                    "content_html",
                    models.TextField(
                        auto_created=True,
                        blank=True,
                        max_length=400,
                        verbose_name="Reply html content",
                    ),
                ),
                (
                    "content_markdown",
                    martor.models.MartorField(
                        max_length=300, verbose_name="Reply markdown content"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Updated at"),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reply",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="child",
                        to="forum.reply",
                    ),
                ),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reply",
                        to="forum.post",
                    ),
                ),
            ],
            options={
                "verbose_name": "reply",
                "verbose_name_plural": "replies",
            },
        ),
    ]
