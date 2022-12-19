from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator, RegexValidator
from django.db import models

from backend.apps.forum.utils import MarkdownTextField, get_upload_path

# Create your models here.


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

    @property
    def capitalize_name(self):
        """Return the capitalized name of the category."""
        if not self.name[0].isupper():
            self.name = self.name.capitalize()
        return self.name


class Files:
    """A model for storing images and files.
    Fields:
        image (ImageField): storage for the image.
        file (FileField): storage for the file.
    """

    image = models.ImageField(
        width_field=500,
        height_field=500,
        upload_to=get_upload_path,
        verbose_name="Image",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["png", "jpg", "jpeg"],
                message="Wrong image format. Try with: png, jpg, jpeg",
            ),
        ],
    )
    file = models.FileField(
        upload_to=get_upload_path,
        verbose_name="File",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["doc", "pdf", "ppt"],
                message="Wrong file format. Try with: doc, pdf, ppt",
            ),
        ],
    )


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
                regex=r"^[a-zA-Z]*$",
                message="Input must contain only alphabetic characters",
            ),
        ],
    )
    body = MarkdownTextField(
        verbose_name="Post body",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    category = models.ForeignKey(
        Category,
        verbose_name="Post category",
        on_delete=models.CASCADE,
        related_name="posts_category",
    )
    files = models.OneToOneField(
        Files,
        verbose_name="Post files",
        on_delete=models.CASCADE,
        related_name="posts_files",
    )
    author = models.ForeignKey(
        get_user_model(),
        verbose_name="Post author",
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

    content = MarkdownTextField(verbose_name="Reply content")
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
    files = models.OneToOneField(
        Files,
        on_delete=models.CASCADE,
        verbose_name="Reply files",
        related_name="reply_files",
    )
    author = models.OneToOneField(
        get_user_model(),
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

    def __str__(self):
        """Return the string representation of the model."""
        return "Reply"

    @property
    def is_parent(self):
        """Return `True` if instance is a parent."""
        if self.parent is not None:
            return False
        return True
