import markdown2
from django.db import models
from django.utils import timezone


class MarkdownText(markdown2.Sanitizer):
    allow_tags = ["p", "em", "strong", "a", "img"]
    allow_attributes = ["href", "title", "src", "alt"]


class MarkdownTextField(models.TextField):
    def clean(self, value):
        sanitizer = MarkdownText()
        value = markdown2.clean(value, sanitizer=sanitizer)
        return super().clean(value)


def get_upload_path(instance, filename):
    # Get the current time in a string format
    now = timezone.now().strftime("%Y/%m/%d")
    # Return the file path
    return f"forum/{instance.user.id}/{now}/{filename}"
