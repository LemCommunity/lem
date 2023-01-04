from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator


class ParentValidator(BaseValidator):
    def __init__(self, message=None):
        self.message = message or "There cannot be more than one child"
        self.data = []

    def __call__(self, instance):
        self.data.append(instance)
        if len(self.data) > 1:
            raise ValidationError(message=self.message)
