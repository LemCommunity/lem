from django.contrib.auth import get_user_model
from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from backend.apps.forum.models.models import Category, Post, Reply


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = Faker("category")


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    title = Faker("title")
    body = Faker("body")
    category = SubFactory(CategoryFactory)
    author = SubFactory(get_user_model())


class ReplyFactory(DjangoModelFactory):
    class Meta:
        model = Reply

    content = Faker("comment")
    parent = SubFactory(CategoryFactory)
    author = SubFactory(get_user_model())
    post = SubFactory(PostFactory)
