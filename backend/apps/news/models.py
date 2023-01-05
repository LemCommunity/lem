from os.path import join

from django.conf import settings

# from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models

# from apps.generic.models import Like


class UserActionTimestamp(models.Model):
    """Abstract model to inherit datetime for obcject creation and/or
    edit by user as well as inherit foreign key to User object."""

    class Meta:
        abstract = True
        ordering = ("-created",)

    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class PolymorphicRelationship(models.Model):
    """Abstract model to inherit generic relationship (polymorphic)
    setup."""

    class Meta:
        abstract = True

    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey("content_type", "object_id")


def directory_path(instance, filename):
    """Returns file path including media type, app name, content type name,
    and file object id.

    Args:
        instance (_class instance_): File or Image class instance
        filename (_str_): filename

    Returns:
        _str_: image's or file's path string
    """
    dir_path = join(
        instance.MEDIA_TYPE,
        instance.content_type.app_label,
        f"{instance.content_type.name}-{instance.object_id}",
    )
    return join(dir_path, filename)


class File(UserActionTimestamp, PolymorphicRelationship):
    MEDIA_TYPE = "files"

    file = models.FileField(upload_to=directory_path, blank=True, null=True)

    def __str__(self) -> str:
        return self.file.url


class Image(UserActionTimestamp, PolymorphicRelationship):
    MEDIA_TYPE = "images"

    image = models.ImageField(upload_to=directory_path, blank=True, null=True)
    alt_text = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.image.url


class Tag(UserActionTimestamp, PolymorphicRelationship):
    class Meta:
        ordering = ["tag"]

    tag = models.SlugField(max_length=50)  # autocomplete?

    def __str__(self) -> str:
        return self.tag


class Highlight(UserActionTimestamp, PolymorphicRelationship):
    highlight = models.BooleanField(default=False)

    def __str__(self):
        return str(self.highlight)


class Comment(UserActionTimestamp, PolymorphicRelationship):
    body = models.TextField(null=False, blank=False)

    def __str__(self) -> str:
        return self.body[:20]


# class NewsManager(models.Manager):
#     # override default get_queryset that returns all objects (not filtered)
#     def get_queryset(self) -> QuerySet:
#         return self.all_objects().filter(status='active')
#
#     # call this function for getting all objects (default get_queryset)
#     def all_objects(self) -> QuerySet:
#         return super().get_queryset()
#
#     # call this function for getting objectes filtered for status "inactive"
#     def inactive(self) -> QuerySet:
#         return self.all_objects().filter(status='inactive')


class News(UserActionTimestamp):
    class Meta:
        verbose_name_plural = "News"

    title = models.CharField(null=False, blank=False, max_length=200)
    # wysiwyg?
    body = models.TextField(null=False, blank=False)
    is_published = models.BooleanField(default=False)
    # optional
    allow_highlights = models.BooleanField(null=False, blank=False, default=True)
    allow_likes = models.BooleanField(null=False, blank=False, default=True)
    allow_comments = models.BooleanField(null=False, blank=False, default=True)

    # text file with inerview
    files = GenericRelation(File, related_query_name="news")
    # image
    images = GenericRelation(Image, related_query_name="news")
    tags = GenericRelation(Tag, related_query_name="news")
    highlights = GenericRelation(Highlight, related_query_name="news")
    likes = GenericRelation(Like, related_query_name="news")
    comments = GenericRelation(Comment, related_query_name="news")

    # model manager should it be useful:
    # objects = NewsManager()

    def __str__(self) -> str:
        return f"{self.id}-{self.title}"

    @property
    def comments_list(self):
        return self.comments.all()
