"""News app models"""

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models
from django.urls import reverse
from django_extensions.db.fields import (
    AutoSlugField,
    CreationDateTimeField,
    ModificationDateTimeField,
)

# from apps.generic.models import Like, File, Picture


class UserActionTimestampedMixin(models.Model):
    """Abstract model to inherit timestamp for obcject creation or
    modification by user as well as inherit foreign key to User object."""

    class Meta:
        abstract = True
        ordering = ("-created",)

    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class PolymorphicRelationship(models.Model):
    """Abstract model to inherit generic relationship (polymorphic)
    setup."""

    class Meta:
        abstract = True

    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey("content_type", "object_id")


class Highlight(UserActionTimestampedMixin, PolymorphicRelationship):
    """Highlight model"""

    highlight = models.BooleanField(default=False)

    def __str__(self):
        return str(self.highlight)


class Tag(UserActionTimestampedMixin, PolymorphicRelationship):
    """Tag model"""

    class Meta:
        ordering = ["name"]

    name = models.CharField(unique=True, max_length=50)
    # TODO add validators

    slug = AutoSlugField(populate_from="name")

    def __str__(self) -> str:
        return self.name


class Comment(UserActionTimestampedMixin, PolymorphicRelationship):
    """Comment model"""

    body = models.TextField(null=False, blank=False)
    # TODO add validators

    # likes = GenericRelation(Like, related_query_name="comment")

    def __str__(self) -> str:
        return self.body[:20]


# draft for further development depending on needs
class NewsManager(models.Manager):
    def get_queryset(self):
        """override default get_queryset and returns published news"""
        return self.all_objects().filter(is_published=True)

    # call this function for getting all news (default get_queryset)
    def all_objects(self):
        """call this function for getting all news (default get_queryset)"""
        return super().get_queryset()

    # call this function for getting not published news
    def inactive(self):
        return self.all_objects().filter(is_published=False)


class News(UserActionTimestampedMixin):
    class Meta:
        verbose_name_plural = "News"

    title = models.CharField(
        null=False,
        blank=False,
        max_length=200,
        validators=[
            MinLengthValidator(3, message="Title must be of at least 3 characters."),
            MaxLengthValidator(
                200, message="Title cannot be longer then 200 characters."
            ),
            # TODO add RegexValidator
        ],
    )
    slug = AutoSlugField(populate_from=["title"])

    body = models.TextField(null=False, blank=False)
    # TODO add body validator, html safety issue?

    is_published = models.BooleanField(default=False)

    allow_highlights = models.BooleanField(null=False, blank=False, default=True)
    allow_likes = models.BooleanField(null=False, blank=False, default=True)
    allow_comments = models.BooleanField(null=False, blank=False, default=True)

    objects = NewsManager()

    # files = GenericRelation(File, related_query_name="news")  # interview text
    # images = GenericRelation(Image, related_query_name="news")  # news image

    tags = GenericRelation(Tag, related_query_name="news")
    highlights = GenericRelation(Highlight, related_query_name="news")

    # likes = GenericRelation(Like, related_query_name="news")

    comments = GenericRelation(Comment, related_query_name="news")

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("news-detail", args=[self.slug])
