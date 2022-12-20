from django.contrib.auth import get_user_model
from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from backend.apps.forum.models import Category, Post, Reply

User = get_user_model()


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ("name",)

    name = Faker("name")


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    title = Faker("title")
    body = Faker("body")
    category = SubFactory(CategoryFactory)
    author = SubFactory(User)


class ReplyFactory(DjangoModelFactory):
    class Meta:
        model = Reply

    content = Faker("comment")
    parent = SubFactory(CategoryFactory)
    author = SubFactory(User)
    post = SubFactory(PostFactory)
