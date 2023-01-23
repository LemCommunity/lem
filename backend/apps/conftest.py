import pytest

from apps.news.models import Comment, Highlight, News, Tag
from apps.news.tests.factories import (
    CommentedCommentFactory,
    CommentedNewsFactory,
    HighlightedNewsFactory,
    NewsFactory,
    TaggedNewsFactory,
)
from apps.users.models import User
from apps.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def _media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture()
def user(db) -> User:
    return UserFactory()


@pytest.fixture()
def news() -> News:
    return NewsFactory


@pytest.fixture()
def highlighted_news() -> Highlight:
    return HighlightedNewsFactory


@pytest.fixture()
def tagged_news() -> Tag:
    return TaggedNewsFactory


@pytest.fixture()
def commented_news() -> Comment:
    return CommentedNewsFactory


@pytest.fixture()
def commented_comment() -> Comment:
    return CommentedCommentFactory
