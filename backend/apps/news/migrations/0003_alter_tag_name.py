# Generated by Django 4.1.4 on 2023-01-12 23:12

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0002_alter_highlight_options_alter_news_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tag",
            name="name",
            field=models.CharField(
                help_text="Must be unique, only alphanumeric allowed",
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
                        re.compile("^[-a-zA-Z0-9_]+\\Z"),
                        "Enter a valid “slug” consisting of letters, numbers, underscores or hyphens.",
                        "invalid",
                    ),
                ],
            ),
        ),
    ]
