import markdown2
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models
from django_extensions.db.fields import AutoSlugField
from martor.models import MartorField

from apps.forum.managers import CategoryManager, PostManager, ReplyManager

# Create your models here.
User = get_user_model()


class CompilableMarkdownBase(models.Model):
    """A abstract model for storing Markdown. Automatically convert markdown to html.

    Fields:
        markdown (MartorField (TextField)): Markdown text.
        compiled_html (TextField): Compiled Markdown to html, is auto created and not editable.
    """

    class Meta:
        abstract = True

    markdown = MartorField(
        max_length=1000,
        verbose_name="Markdown content",
    )
    compiled_html = models.TextField(
        editable=False,
        verbose_name="HTML content",
        auto_created=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        """When the model is saved, the markdown field is converted to HTML and saved in the compiled_html field."""
        self.compiled_html = markdown2.markdown(self.markdown)
        return super().save(*args, **kwargs)


class Category(models.Model):
    """A model representing a category model.

    Fields:
        name (CharField): The name of the category. Must be unique and contain only
            alphabetic characters.
    """

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    objects = CategoryManager()

    name = models.CharField(
        verbose_name="Category name",
        max_length=100,
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
        """If the name is not None, capitalize it and then save the category."""
        if self.name is not None:
            self.name = self.name.capitalize()
        return super().save(*args, **kwargs)


class Post(CompilableMarkdownBase):
    """A model representing a post model.

    Fields:
        title (CharField): The title of the Post.
        markdown (MartorField (TextField)): Markdown text.
        compiled_html (TextField): Compiled Markdown to html, is auto created and not editable.
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
                regex=r"^[a-zA-Z\'\" ]+$",
                message="Input must contain only alphabetic characters (' and \" included) and spaces",
            ),
        ],
    )

    slug = AutoSlugField(
        populate_from=["slug_datetime", "title"],
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
        """If the title is not None, capitalize it and then save the post"""
        if self.title is not None:
            self.title = self.title.capitalize()
        super(Post, self).save(*args, **kwargs)

    @property
    def slug_datetime(self):
        """Takes the date time of the post and converts it into a string."""
        return str(self.created_at.strftime("%d-%m-%Y"))


class Reply(CompilableMarkdownBase):
    """A model representing a reply model.

    Fields:
        markdown (MartorField (TextField)): Markdown text.
        compiled_html (TextField): Compiled Markdown to html, is auto created and not editable.
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

    @property
    def has_parent(self):
        """Return `True` if instance is a parent."""
        if self.parent is not None:
            return True
        return False

    @property
    def replies_amount(self):
        """It returns the amount of replies a reply has as children."""
        return self.children.count()
