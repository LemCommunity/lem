import re

from markdown2 import Markdown

markdowner = Markdown()


def markdown_text(instance):
    new_list = []
    if instance:
        text_list = instance.splitlines()
        for text in text_list:
            mark_text = str(markdowner.convert(text))
            new_list.append(mark_text)
    string = "".join(new_list)
    return string


def is_html(string):
    list_str = string.split("\n")
    return any(re.match(r"^<[a-z]+>", s) for s in list_str)
