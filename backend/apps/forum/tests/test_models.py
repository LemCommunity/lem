import datetime
from unittest import mock

import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from apps.forum.models import Category, CompilableMarkdownBase, Post, Reply
from apps.forum.tests.factories import CategoryFactory, PostFactory, ReplyFactory

User = get_user_model()


class TestCompilableMarkdownBase:
    def test_fields(self):
        assert get_field(CompilableMarkdownBase, "markdown")
        assert get_field(CompilableMarkdownBase, "compiled_html").auto_created

    @mock.patch("apps.forum.models.models.Model.save")
    def test_compiled_html(self, mocked_super_save):
        markdown = "**boom!**"
        compiled_html = "<p><strong>boom!</strong></p>\n"
        with mock.patch.object(CompilableMarkdownBase, "__init__", return_value=None):
            model = CompilableMarkdownBase()
        model.markdown = markdown

        model.save(test=1)  # act

        mocked_super_save.assert_called_once_with(test=1)
        assert model.compiled_html == compiled_html


@pytest.mark.django_db()
class TestCategoryModel:
    def test_fields(self):
        assert get_field(Category, "name")

    @pytest.fixture()
    def category(self):
        return CategoryFactory.create(name="books")

    def test_capitalize_name(self, category):
        assert category.name == "Books"

    def test_invalid_name(self):
        with pytest.raises(
            ValidationError,
            match="Input must contain only alphabetic characters without spaces",
        ):
            get_field(Category, "name").run_validators("test test")  # act

    def test_valid_name(self):
        get_field(Category, "name").run_validators("Python")  # act

    def test_str(self, category):
        assert str(category) == category.name


@pytest.mark.django_db()
class TestPostModel:
    def test_fields(self):
        assert get_field(Post, "title")

        assert issubclass(Post, CompilableMarkdownBase)
        assert get_field(Post, "markdown")
        assert get_field(Post, "compiled_html")

        assert get_field(Post, "slug")
        assert get_field(Post, "title")
        assert get_field(Post, "category") == get_field(Category, "posts")
        assert get_field(Post, "author") == get_field(User, "posts")

    @pytest.fixture()
    def post(self):
        return PostFactory.create(
            title="some title",
            created_at=datetime.datetime(1996, 3, 20, 7, 46, 39),
        )

    def test_markdown(self, post):
        markdown = "**boom!**"
        compiled_html = "<p><strong>boom!</strong></p>\n"

        post.markdown = markdown

        post.save()

        assert post.compiled_html == compiled_html

    def test_invalid_title(self):
        with pytest.raises(
            ValidationError,
            match=r"Input must contain only alphabetic characters.*",
        ):
            get_field(Post, "title").run_validators("invalid%#@$ title 123")  # act

    def test_valid_title(self):
        get_field(Post, "title").run_validators(
            "Why django isn't a good idea for this project"
        )  # act

    def test_capitalize_title(self, post):
        assert post.title == "Some title"

    def test_slug(self, post):
        assert post.slug == "20-03-1996-some-title"

    @pytest.fixture()
    def post2(self):
        return PostFactory.create(
            title="some title",
            created_at=datetime.datetime(1996, 3, 20, 7, 46, 39),
        )

    def test_slug_uniqueness(self, post, post2):
        assert post.slug != post2.slug
        assert post2.slug.endswith("-2")

    def test_str(self, post):
        assert str(post) == post.title  # act


@pytest.mark.django_db()
class TestReplyModel:
    def test_fields(self):
        assert issubclass(Post, CompilableMarkdownBase)
        assert get_field(Post, "markdown")
        assert get_field(Post, "compiled_html")

        assert get_field(Reply, "created_at")
        assert get_field(Reply, "updated_at")
        assert get_field(Reply, "children") == get_field(Reply, "parent")
        assert get_field(Reply, "author") == get_field(User, "replies")
        assert get_field(Reply, "post") == get_field(Post, "replies")

    @pytest.fixture()
    def reply_models(self):
        first_reply = ReplyFactory.create(parent=None)
        second_reply = ReplyFactory.create(parent=first_reply)
        return [first_reply, second_reply]

    def test_markdown(self, reply_models):
        markdown = "**boom!**"
        compiled_html = "<p><strong>boom!</strong></p>\n"

        reply = reply_models[0]

        reply.markdown = markdown

        reply.save()

        assert reply.compiled_html == compiled_html

    def test_has_parent(self, reply_models):
        assert reply_models[0].has_parent is False
        assert reply_models[1].has_parent is True

    def test_replies_amount(self, reply_models):
        assert reply_models[0].replies_amount == 1
        assert reply_models[1].replies_amount == 0

    def test_str(self, reply_models):
        assert str(reply_models[0]) == "Reply"


def get_field(model, field):
    return getattr(model, field).field
