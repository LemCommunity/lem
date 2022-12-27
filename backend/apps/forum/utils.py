import re

from django.db import models
from markdown2 import Markdown
from martor.models import MartorField

markdowner = Markdown()


def get_content_html(
    instance: models.TextField, mark_obj: MartorField
) -> models.TextField | None:
    """Create content_html field"""
    if mark_obj is not None:
        instance = markdown_to_html(mark_obj)
    else:
        instance = None
    return instance


def markdown_to_html(instance: MartorField) -> str:
    """Create html from markdown field"""
    new_list = []
    if instance:
        text_list = instance.splitlines()
        for text in text_list:
            mark_text = str(markdowner.convert(text))
            new_list.append(mark_text)
    string = "".join(new_list)
    return string


def is_html(string: str) -> bool:
    """Check if string is html"""
    list_str = string.split("\n")
    return any(re.match(r"^<[a-z]+>", s) for s in list_str)
