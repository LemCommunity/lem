from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models
from martor.models import MartorField

from backend.apps.forum.managers import PostManager, ReplyManager
from backend.apps.forum.utils import is_html, markdown_text

# Create your models here.
User = get_user_model()


class Category(models.Model):
    """A model representing a category model.

    Fields:
        name (str): The name of the category. Must be unique and contain only
            alphabetic characters.
    """

    name = models.CharField(
        max_length=100,
        blank=False,
        unique=True,
        verbose_name="Category name",
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z]*$",
                message="Input must contain only alphabetic characters",
            ),
        ],
    )

    def __str__(self):
        """Return the string representation of the model."""
        return self.name


class Post(models.Model):
    """A model representing a post model.

    Fields:
        title (CharField): The title of the Post. This field must be unique across all
            Post objects.
        body (TextField): The content of the post.
        created_at (DateTimeField): The creation time of the Post. This field is set
            automatically to the current time when the Post object is first created.
        category (ForeignKey): The category that the Post belongs to. If the Category
            object that the Post belongs to is deleted, the Post will also be deleted.
        author (ForeignKey): The user who wrote the Post. If the user who wrote the
            Post is deleted, the Post will also be deleted.
    """

    title = models.CharField(
        max_length=100,
        verbose_name="Post title",
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z ]+$",
                message="Input must contain only alphabetic characters",
            ),
        ],
    )
    body = MartorField()
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    category = models.OneToOneField(
        Category,
        verbose_name="Post category",
        on_delete=models.CASCADE,
        related_name="posts_category",
    )
    author = models.ForeignKey(
        User,
        verbose_name="Post author",
        on_delete=models.CASCADE,
        related_name="posts_author",
    )

    objects = PostManager()

    def __str__(self):
        """Return the string representation of the model."""
        return self.title

    def save(self, *args, **kwargs):
        self.body = markdown_text(self.body)
        super(Post, self).save(*args, **kwargs)

    @property
    def is_html_text(self):
        if self.body is not None:
            return is_html(self.body)


class Reply(models.Model):
    """A model representing a reply model.

    Fields:
        content (TextField): The content of the reply.
        created_at (DateTimeField): The date and time at which the reply was created.
        updated_at (DateTimeField): The date and time at which the reply was last
            updated.
        parent (ForeignKey): A foreign key to the parent Post object. If the parent
            Post is deleted, all its child Posts will also be deleted. This field can
            be left blank (NULL in the database).
        author (ForeignKey): A foreign key to the user model representing the author
            of the reply.
        post (ForeignKey): A foreign key to the Post.
    """

    content = MartorField()
    created_at = models.DateTimeField(
        verbose_name="Reply created",
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name="Reply updated",
        auto_now=True,
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Parent for Post object or None",
        related_name="children",
    )
    author = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Reply author",
        related_name="reply_author",
    )
    post = models.OneToOneField(
        Post,
        on_delete=models.CASCADE,
        verbose_name="Reply post",
        related_name="reply_post",
    )

    objects = ReplyManager()

    def __str__(self):
        """Return the string representation of the model."""
        return "Reply"

    def save(self, *args, **kwargs):
        self.content = markdown_text(self.content)
        super(Reply, self).save(*args, **kwargs)

    @property
    def is_parent(self):
        """Return `True` if instance is a parent."""
        if self.parent is not None:
            return True
        return False

    @property
    def is_html_text(self):
        if self.content is not None:
            return is_html(self.content)
