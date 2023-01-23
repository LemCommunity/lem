import factory
from django.contrib.contenttypes.models import ContentType
from faker import Faker

from apps.news.models import Comment, Highlight, Tag
from apps.users.tests.factories import UserFactory

fake = Faker()


class UserActionTimestampedMixinFactory(factory.django.DjangoModelFactory):
    class Meta:
        abstract = True

    created = fake.date_time()
    modified = fake.date_time_between_dates(datetime_start=created)
    user = factory.SubFactory(UserFactory)


class PolymorphicRelationshipFactory(factory.django.DjangoModelFactory):
    class Meta:
        exclude = ["content_objects"]
        abstract = True

    object_id = factory.SelfAttribute("content_object.id")
    content_type = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(o.content_object)
    )


class NewsFactory(UserActionTimestampedMixinFactory):
    class Meta:
        model = "news.News"

    title = fake.text(max_nb_chars=50)
    slug = fake.slug(title)
    body = fake.text(max_nb_chars=160)
    is_published = False
    allow_highlights = True
    allow_likes = True
    allow_comments = True


class TaggedNewsFactory(
    UserActionTimestampedMixinFactory, PolymorphicRelationshipFactory
):
    class Meta:
        model = Tag

    tag = fake.word()
    slug = fake.slug(tag)
    content_object = factory.SubFactory(NewsFactory)


class HighlightedNewsFactory(
    UserActionTimestampedMixinFactory, PolymorphicRelationshipFactory
):
    class Meta:
        model = Highlight

    highlight = True
    content_object = factory.SubFactory(NewsFactory)


class CommentedNewsFactory(
    UserActionTimestampedMixinFactory, PolymorphicRelationshipFactory
):
    class Meta:
        model = Comment

    body = fake.text()
    content_object = factory.SubFactory(NewsFactory)


class CommentedCommentFactory(
    UserActionTimestampedMixinFactory, PolymorphicRelationshipFactory
):
    class Meta:
        model = Comment

    body = fake.text()
    content_object = factory.SubFactory(CommentedNewsFactory)
