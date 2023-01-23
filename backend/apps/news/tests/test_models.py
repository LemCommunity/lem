import pytest

from apps.news.models import Comment, News

pytestmark = pytest.mark.django_db


def test_new_news_build(news):
    count_before = News.objects.all().count()
    news = news.build()
    count_after = News.objects.all().count()
    assert count_after == count_before
    assert news.title
    assert news.slug
    assert news.user


def test_new_news_create(news):
    count_before = News.objects.all().count()
    news = news.create()
    count_after = News.objects.all().count()
    assert count_after == count_before + 1
    assert news.title
    assert news.slug
    assert news.user


def test_create_tag_on_news(tagged_news):
    count_before = News.objects.all().count()
    tagged_news = tagged_news.create()
    count_after = News.objects.all().count()
    print(tagged_news.created)
    print(tagged_news.modified)
    print(tagged_news.tag)
    print(tagged_news.slug)
    print(tagged_news.object_id)
    print(tagged_news.content_object.id)
    print(tagged_news.content_type)
    print(tagged_news.content_type.app_label)
    print(tagged_news.content_type.model)
    assert tagged_news.content_type.model == "news"
    assert tagged_news.object_id is not None
    assert tagged_news.object_id == tagged_news.content_object.id
    assert count_after == count_before + 1


def test_create_highlight_on_news(highlighted_news):
    highlighted_news = highlighted_news.create()
    assert highlighted_news.content_type.model == "news"
    assert highlighted_news.object_id is not None
    assert highlighted_news.object_id == highlighted_news.content_object.id


def test_create_comment_on_news(commented_news):
    count_before = Comment.objects.all().count()
    commented_news = commented_news.create()
    count_after = Comment.objects.all().count()
    assert commented_news.content_type.model == "news"
    assert commented_news.object_id is not None
    assert commented_news.object_id == commented_news.content_object.id
    assert count_after == count_before + 1


def test_create_comment_on_comment(commented_comment):
    count_before = Comment.objects.all().count()
    commented_comment = commented_comment.create()
    count_after = Comment.objects.all().count()
    assert commented_comment.content_type.model == "comment"
    assert commented_comment.object_id is not None
    assert commented_comment.object_id == commented_comment.content_object.id
    assert count_after == count_before + 2


# to be done later
# def test_news_get_absolute_url(news: News):
#     assert news.get_absolute_url() == f"/apps/news/news/{news.slug}/"
