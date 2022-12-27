from factory import Faker, LazyFunction, Sequence, SubFactory
from factory.django import DjangoModelFactory
from faker import Faker as Fake
from mdgen import MarkdownPostProvider

from backend.apps.forum.models import Category, Post, Reply
from backend.apps.forum.utils import get_content_html
from backend.apps.users.tests.factories import UserFactory

fake = Fake()
fake.add_provider(MarkdownPostProvider)
fake_markdown = fake.post(size="small")
fake_unique_word = Sequence(lambda n: fake.unique.word().lower())
fake_unique_two_words = LazyFunction(lambda: fake.unique.name())


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = fake_unique_word


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    title = fake_unique_two_words
    content_markdown = fake_markdown
    content_html = get_content_html(None, fake_markdown)
    slug = title
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
