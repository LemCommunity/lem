from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext as _


class Quote(models.Model):
    """
    A model representing a quote.

    Fields:
        text (models.textField): The text of the quote
        added_by (models.ForeignKey): The foreign key of the User who added this Quote to.
        book (models.ForeignKey): The foreign key of the ContentType of the book.
        tags (GenericRelation): The many to many relation to the tag
        likes (GenericRelation): The many to many relation to the like
        created_at (models.DateTimeField): The date of added the Quote. This field is set automatically
            when the Quote is created.
        updated_at (models.DateTimeField): The date of updated the Quote. This field is set automatically
            when the Quote was updated

    """

    class Meta:
        verbose_name = _("Quote")
        verbose_name_plural = _("Quotes")
        ordering = ("text",)

    text = models.TextField(null=False, help_text="The text of the quote.")
    added_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        help_text="The user added the quote.",
    )
    book = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        help_text="The foreign key to the book model.",
    )
    tags = GenericRelation(ContentType)
    likes = GenericRelation(ContentType)
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="The date of creation of the quote."
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="The date when the quote was changed."
    )

    def __str__(self):
        return f"Quote: {self.text}"

    # TODO:
    # def number_of_likes(self):
    #     return len(self.likes)


class FavoriteQuote(models.Model):
    """
    A model representing a favorite quote.

    Fields:
        quote (models.ForeignKey): The foreign key of the quote.
        added_by (ForeignKey): the foreign key of User who added this FavoriteQuote.
        created_at (models.DateTimeField): The date of added the Quote. This field is set automatically
            when the Quote is created.
        updated_at (models.DateTimeField): The date of updated the Quote. This field is set automatically
            when the Quote was updated
    """

    class Meta:
        verbose_name = _("Favorite quote")
        verbose_name_plural = _("Favorite quotes")
        ordering = ("quote",)

    quote = models.ForeignKey(
        Quote, on_delete=models.CASCADE, help_text="The object of the quote."
    )

    added_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        help_text="the user added the quote to favorite.",
    )
    created_at = models.DateTimeField(
        auto_now=True, help_text="The date of adding quote to favorite."
    )
    updated_at = models.DateTimeField(auto_now=False)

    def __str__(self):
        return f"Favorite Quote: {self.quote}"
