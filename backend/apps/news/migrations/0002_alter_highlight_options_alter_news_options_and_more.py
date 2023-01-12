# Generated by Django 4.1.4 on 2023-01-12 21:22

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("news", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="highlight",
            options={"verbose_name": "highlight", "verbose_name_plural": "highlights"},
        ),
        migrations.AlterModelOptions(
            name="news",
            options={"verbose_name_plural": "news"},
        ),
        migrations.AlterField(
            model_name="comment",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="user",
            ),
        ),
        migrations.AlterField(
            model_name="highlight",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="user",
            ),
        ),
        migrations.AlterField(
            model_name="news",
            name="allow_comments",
            field=models.BooleanField(default=True, verbose_name="allow comments"),
        ),
        migrations.AlterField(
            model_name="news",
            name="allow_highlights",
            field=models.BooleanField(default=True, verbose_name="allow highlights"),
        ),
        migrations.AlterField(
            model_name="news",
            name="allow_likes",
            field=models.BooleanField(default=True, verbose_name="allow likes"),
        ),
        migrations.AlterField(
            model_name="news",
            name="body",
            field=models.TextField(verbose_name="news body"),
        ),
        migrations.AlterField(
            model_name="news",
            name="is_published",
            field=models.BooleanField(default=False, verbose_name="is published"),
        ),
        migrations.AlterField(
            model_name="news",
            name="title",
            field=models.CharField(
                help_text="Min lenght of 3 chars, max length of 200 chars, only alphanumeric, ', \", dot and space allowed",
                max_length=200,
                validators=[
                    django.core.validators.MinLengthValidator(
                        3, message="Min length is 3 characters."
                    ),
                    django.core.validators.MaxLengthValidator(
                        200, message="Max length is 200 characters."
                    ),
                    django.core.validators.RegexValidator(
                        message="Only alphanumeric, ', \", dot and space allowed.",
                        regex="^[\\w\\.\\'\\\" ]+$",
                    ),
                ],
                verbose_name="news title",
            ),
        ),
        migrations.AlterField(
            model_name="news",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="user",
            ),
        ),
        migrations.AlterField(
            model_name="tag",
            name="name",
            field=models.CharField(
                help_text="Uniqe word, only alphanumeric allowed",
                max_length=50,
                unique=True,
                validators=[
                    django.core.validators.MinLengthValidator(
                        3, message="Min length is 3 characters."
                    ),
                    django.core.validators.MaxLengthValidator(
                        200, message="Max length is 200 characters."
                    ),
                    django.core.validators.RegexValidator(
                        message="Only alphanumeric allowed.", regex="^[\\w]+$"
                    ),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="tag",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="user",
            ),
        ),
    ]
