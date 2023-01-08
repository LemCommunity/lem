import markdown2
from factory import LazyAttribute, LazyFunction, Sequence, SubFactory
from factory.django import DjangoModelFactory
from faker import Faker
from mdgen import MarkdownPostProvider

from apps.forum.models import Category, CompilableMarkdownBase, Post, Reply
from apps.users.tests.factories import UserFactory

faker = Faker()
faker.add_provider(MarkdownPostProvider)
fake_markdown = faker.post(size="small")


class CompilableMarkdownBaseFactory(DjangoModelFactory):
    class Meta:
        model = CompilableMarkdownBase
        abstract = True

    markdown = LazyFunction(lambda: faker.post(size="small"))
    compiled_html = LazyAttribute(lambda obj: markdown2.markdown(obj.markdown))


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = Sequence(lambda _: faker.unique.word().lower())


class PostFactory(CompilableMarkdownBaseFactory):
    class Meta:
        model = Post

    title = LazyFunction(lambda: faker.name())

    slug = LazyFunction(lambda: faker.slug())
    created_at = LazyFunction(lambda: faker.date_time())
    updated_at = LazyAttribute(
        lambda obj: faker.date_time_between_dates(datetime_start=obj.created_at)
    )
    category = SubFactory(CategoryFactory)
    author = SubFactory(UserFactory)


class ReplyFactory(CompilableMarkdownBaseFactory):
    class Meta:
        model = Reply

    created_at = LazyFunction(lambda: faker.date_time())
    updated_at = LazyAttribute(
        lambda obj: faker.date_time_between_dates(datetime_start=obj.created_at)
    )
    parent = SubFactory("apps.forum.tests.factories.ReplyFactory", parent=None)
    author = SubFactory(UserFactory)
    post = SubFactory(PostFactory)
