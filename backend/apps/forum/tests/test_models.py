from typing import List

import factory
import pytest
from faker import Faker

from backend.apps.forum.models import Category, Post, Reply
from backend.apps.forum.tests.factories import (
    CategoryFactory,
    PostFactory,
    ReplyFactory,
)
from backend.apps.users.tests.factories import UserFactory

fake = Faker()


@pytest.mark.django_db(transaction=True)
class TestCategoryModel:
    @pytest.fixture()
    def category_model(self) -> List[str]:
        data = []
        for _ in range(5):
            category = CategoryFactory.create(
                name=factory.LazyFunction(lambda: fake.bothify(text="??????").lower())
            )
            data.append(category.name)
        return data

    def test_category_capitalize_name(self, category_model: List[str]) -> None:
        for category_name in category_model:
            assert category_name[0].isupper() is True

    @pytest.fixture()
    def category_model_invalid(self) -> Category:
        return CategoryFactory.build(name=factory.LazyFunction(lambda: fake.name()))

    def test_category_capitalize_name_invalid(
        self, category_model_invalid: Category
    ) -> None:
        if category_model_invalid.name.find(" ") != -1:
            with pytest.raises(ImportError):
                category_name_error()


def category_name_error() -> None:
    raise ImportError("Invalid category name")


@pytest.mark.django_db(transaction=True)
class TestPostModel:
    @pytest.fixture()
    def post_model(self) -> Post:
        return PostFactory.create(
            title="some title",
            body="# Markdown\n\nText.",
            category=CategoryFactory.create(name="category"),
            author=UserFactory.create(
                username="emil123",
                email="emil123@example.com",
                first_name="Emil",
                last_name="Dostowski",
            ),
        )

    def test_post_model(self, post_model) -> None:
        assert post_model.title == "Some title"
        assert post_model.body == "<h1>Markdown</h1>\n<p></p>\n<p>Text.</p>\n"
        assert post_model.is_html_text is True
        assert post_model.category.name == "Category"
        assert post_model.author.email == "emil123@example.com"

    def test_post_sum(self):
        for _ in range(10):
            PostFactory.create()
        assert Post.objects.sum_posts() == 10


@pytest.mark.django_db(transaction=True)
class TestReplyModel:
    @pytest.fixture()
    def reply_models(self) -> List[None | Reply]:
        first_reply = ReplyFactory.create(parent=ReplyFactory.create())
        second_reply = ReplyFactory.create(parent=None)
        return [first_reply, second_reply]

    def test_reply_model(self, reply_models) -> None:
        assert reply_models[0].is_parent is True
        assert reply_models[1].is_parent is False

    @pytest.fixture()
    def reply_fifty_model(self) -> List[None | Reply]:
        reply_parent = ReplyFactory.create(parent=None)
        for _ in range(50):
            ReplyFactory.create(parent=reply_parent)
        return reply_parent

    def test_reply_parent_sum(self, reply_fifty_model):
        assert reply_fifty_model.sum_replies == 50
