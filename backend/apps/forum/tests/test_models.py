import datetime
from typing import List

import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from faker import Faker

from backend.apps.forum.models import Category, Post, Reply
from backend.apps.forum.tests.factories import (
    CategoryFactory,
    PostFactory,
    ReplyFactory,
)
from backend.apps.forum.utils import is_html

User = get_user_model()
fake = Faker()


@pytest.mark.django_db(transaction=True)
class TestCategoryModel:
    @pytest.fixture()
    def category_model_name(self) -> str:
        category = CategoryFactory.create(name="books")
        return category.name

    def test_category_capitalize_name(self, category_model_name: str) -> None:
        assert category_model_name == "Books"

    def test_invalid_category_name(self):
        name = "test test"
        regex = RegexValidator(
            regex=r"^[a-zA-Z]+$",
            message="Input must contain only alphabetic characters",
        )
        with pytest.raises(ValidationError) as error:
            CategoryFactory.create(name=regex(name))
        assert error.value.message == "Input must contain only alphabetic characters"

    def test_category_model(self) -> None:
        assert get_field(Category, "name")


@pytest.mark.django_db(transaction=True)
class TestPostModel:
    @pytest.fixture()
    def post_model(self) -> Post:
        return PostFactory.create()

    def test_content_is_html(self, post_model):
        assert is_html(post_model.content_html) is True

    def test_post_model(self) -> None:
        assert get_field(Post, "title")
        assert get_field(Post, "content_markdown")
        assert get_field(Post, "content_html")
        assert get_field(Post, "slug")
        assert get_field(Post, "title")
        assert get_field(Post, "category") == get_field(Category, "posts")
        assert get_field(Post, "author") == get_field(User, "posts")

    def test_invalid_post_title(self):
        title = "test%^&*("
        regex = RegexValidator(
            regex=r"^[a-zA-Z ]+$",
            message="Input must contain only alphabetic characters and spaces",
        )
        with pytest.raises(ValidationError) as error:
            PostFactory.create(title=regex(title))
        assert (
            error.value.message
            == "Input must contain only alphabetic characters and spaces"
        )

    def test_content_slug(self):
        post_model = PostFactory.create(
            title="some title",
            created_at=datetime.datetime(1996, 3, 20, 7, 46, 39),
        )
        assert post_model.slug == "some-title-07463920031996"

    def test_content_html(self):
        post_model = PostFactory.create(content_markdown="# Markdown\n\nText.")
        assert post_model.content_html == "<h1>Markdown</h1>\n<p></p>\n<p>Text.</p>\n"

    def test_post_sum(self):
        for _ in range(10):
            PostFactory.create()
        assert Post.objects.all().count() == 10


@pytest.mark.django_db(transaction=True)
class TestReplyModel:
    @pytest.fixture()
    def reply_models(self) -> List[None | Reply]:
        first_reply = ReplyFactory.create(parent=ReplyFactory.create())
        second_reply = ReplyFactory.create(parent=None)
        return [first_reply, second_reply]

    def test_reply_model_has_parent(self, reply_models) -> None:
        assert reply_models[0].has_parent is True
        assert reply_models[1].has_parent is False

    def test_reply_model(self) -> None:
        assert get_field(Reply, "content_markdown")
        assert get_field(Reply, "content_html")
        assert get_field(Reply, "created_at")
        assert get_field(Reply, "updated_at")
        assert get_field(Reply, "children") == get_field(Reply, "parent")
        assert get_field(Reply, "author") == get_field(User, "replies")
        assert get_field(Reply, "post") == get_field(Post, "replies")

    @pytest.fixture()
    def reply_fifty_model(self) -> List[None | Reply]:
        reply_parent = ReplyFactory.create(parent=None)
        for _ in range(50):
            ReplyFactory.create(parent=reply_parent)
        return reply_parent

    def test_reply_parent_sum(self, reply_fifty_model):
        assert reply_fifty_model.sum_replies == 50


def get_field(model, field):
    return getattr(model, field).field
