from django.db.models.signals import pre_save
from django.dispatch import receiver

from backend.apps.forum.models import Category, Post


@receiver(pre_save, sender=Category)
def category_name(sender, instance, **kwargs):
    instance.name = instance.name.capitalize()


@receiver(pre_save, sender=Post)
def post_title(sender, instance, **kwargs):
    instance.title = instance.title.capitalize()
