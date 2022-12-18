from django.contrib.auth import get_user_model
from django.db import models

from .validators import validate_alphabetic

# Create your models here.


class Category(models.Model):
    """A model representing a category model.

    Fields:
        name (str): The name of the category. Must be unique and contain only
            alphabetic characters.
    """

    name = models.CharField(
        max_length=100,
        unique=True,
    )

    def __str__(self):
        """Return the string representation of the model."""
        return self.name

    @property
    def capitalize_name(self):
        """Return the capitalized name of the category."""
        if not self.name[0].isupper():
            self.name = self.name.capitalize()
        return self.name

    def clean(self):
        """Validate the name field of the category."""
        validate_alphabetic(self.name)


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
    )
    body = models.TextField()
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="posts_category",
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="posts_author",
    )

    def __str__(self):
        """Return the string representation of the model."""
        return self.title

    @property
    def capitalize_title(self):
        """Return the capitalized title of the post."""
        if not self.title[0].isupper():
            self.title = self.title.capitalize()
        return self.title

    def clean(self):
        """Validate the name field of the post."""
        validate_alphabetic(self.title)


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

    content = models.TextField()
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="reply_author",
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="reply_post",
    )

    def __str__(self):
        """Return the string representation of the model."""
        return "Reply"

    @property
    def is_parent(self):
        """Return `True` if instance is a parent."""
        if self.parent is not None:
            return False
        return True
