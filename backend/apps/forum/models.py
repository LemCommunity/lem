from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models
from django_extensions.db.fields import AutoSlugField
from martor.models import MartorField

from backend.apps.forum.managers import CategoryManager, PostManager, ReplyManager
from backend.apps.forum.utils import get_content_html

# Create your models here.
User = get_user_model()


class Category(models.Model):
    """A model representing a category model.

    Fields:
        name (str): The name of the category. Must be unique and contain only
            alphabetic characters.
    """

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    objects = CategoryManager()

    name = models.CharField(
        verbose_name="Category name",
        max_length=100,
        blank=False,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z]+$",
                message="Input must contain only alphabetic characters without spaces",
            ),
        ],
    )

    def __str__(self):
        """Return the string representation of the model."""
        return self.name

    def save(self, *args, **kwargs):
        if self.name is not None:
            self.name = self.name.capitalize()
        return super().save(*args, **kwargs)


class Post(models.Model):
    """A model representing a post model.

    Fields:
        title (CharField): The title of the Post.
        content_markdown (MartorField): The content of the post markdown.
        content_html (TextField): The content of the post html.
        created_at (DateTimeField): The creation datetime of the Post. This field is set
            automatically to the current time when the Post object is first created.
        updated_at (DateTimeField): The update datetime of the Post. This field is set
            automatically to the current time when the Post object is updated.
        slug (AutoSlugField): Create slug field to endpoint, from fields title and
            method get_slug_datetime.
        category (ForeignKey): The category that the Post belongs to. If the Category
            object that the Post belongs to is deleted, the Post will also be deleted.
        author (ForeignKey): The user who wrote the Post. If the user who wrote the
            Post is deleted, the Post will also be deleted.
    """

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    objects = PostManager()

    title = models.CharField(
        verbose_name="Post title",
        max_length=100,
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z ]+$",
                message="Input must contain only alphabetic characters and spaces",
            ),
        ],
    )
    content_markdown = MartorField(
        max_length=300,
        verbose_name="Post markdown content",
    )
    content_html = models.TextField(
        max_length=400,
        verbose_name="Post html content",
        auto_created=True,
        blank=True,
    )
    slug = AutoSlugField(
        populate_from=["title", "get_slug_datetime"],
        verbose_name="Post slug",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created at",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated at",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="posts",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
    )

    def __str__(self):
        """Return the string representation of the model."""
        return self.title

    def save(self, *args, **kwargs):
        if self.title is not None:
            self.title = self.title.capitalize()
        self.content_html = get_content_html(self.content_html, self.content_markdown)
        super(Post, self).save(*args, **kwargs)

    @property
    def get_slug_datetime(self):
        return str(self.created_at.strftime("%H:%M:%S:%d:%m:%Y")).replace(":", "")


class Reply(models.Model):
    """A model representing a reply model.

    Fields:
        content_markdown (MartorField): The content of the post markdown.
        content_html (TextField): The content of the post html.
        created_at (DateTimeField): The date and time at which the reply was created.
        updated_at (DateTimeField): The date and time at which the reply was last
            updated.
        parent (ForeignKey): A foreign key to the parent Reply object. Default is None (Reply belong only to Post).
            Can accept one or more self class.
        author (ForeignKey): A foreign key to the user model representing the author
            of the reply.
        post (ForeignKey): A foreign key to the Post.
    """

    class Meta:
        verbose_name = "reply"
        verbose_name_plural = "replies"

    objects = ReplyManager()

    content_markdown = MartorField(
        max_length=300,
        verbose_name="Reply markdown content",
    )
    content_html = models.TextField(
        max_length=400,
        verbose_name="Reply html content",
        auto_created=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created at",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated at",
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="replies",
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="replies",
    )

    def __str__(self):
        """Return the string representation of the model."""
        return "Reply"

    def save(self, *args, **kwargs):
        self.content_html = get_content_html(self.content_html, self.content_markdown)
        super(Reply, self).save(*args, **kwargs)

    @property
    def has_parent(self):
        """Return `True` if instance is a parent."""
        if self.parent is not None:
            return True
        return False

    @property
    def sum_replies(self):
        if self.children is None:
            return 0
        else:
            return self.children.count()
