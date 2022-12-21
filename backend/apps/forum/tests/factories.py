from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from backend.apps.forum.models import Category, Post, Reply
from backend.apps.forum.tests.providers import fake_post
from backend.apps.users.tests.factories import UserFactory


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = Faker(provider="bothify", text="??????")


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    title = Faker(provider="name")
    body = fake_post
    created_at = Faker(provider="date_time")
    category = SubFactory(CategoryFactory)
    author = SubFactory(UserFactory)


class ReplyFactory(DjangoModelFactory):
    class Meta:
        model = Reply

    content = fake_post
    parent = SubFactory("backend.apps.forum.tests.factories.ReplyFactory", parent=None)
    author = SubFactory(UserFactory)
    post = SubFactory(PostFactory)
