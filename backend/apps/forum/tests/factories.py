from factory import Faker, LazyAttribute, LazyFunction, Sequence, SubFactory
from factory.django import DjangoModelFactory
from faker import Faker as Fake
from mdgen import MarkdownPostProvider

from backend.apps.forum.models import Category, Post, Reply
from backend.apps.forum.utils import get_content_html
from backend.apps.users.tests.factories import UserFactory

fake = Fake()
fake.add_provider(MarkdownPostProvider)
fake_markdown = fake.post(size="small")


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = Sequence(lambda _: fake.unique.word().lower())


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    title = LazyFunction(lambda: fake.name())
    content_markdown = fake_markdown
    content_html = get_content_html(None, fake_markdown)
    slug = LazyAttribute(lambda _: fake.slug())
    created_at = Faker(provider="date_time")
    updated_at = Faker(provider="date_time")
    category = SubFactory(CategoryFactory)
    author = SubFactory(UserFactory)


class ReplyFactory(DjangoModelFactory):
    class Meta:
        model = Reply

    content_markdown = fake_markdown
    content_html = get_content_html(None, fake_markdown)
    created_at = Faker(provider="date_time")
    updated_at = Faker(provider="date_time")
    parent = SubFactory("backend.apps.forum.tests.factories.ReplyFactory", parent=None)
    author = SubFactory(UserFactory)
    post = SubFactory(PostFactory)
