import markdown2
from django.db import models


class MarkdownTextField(models.TextField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return markdown2.markdown(value)
