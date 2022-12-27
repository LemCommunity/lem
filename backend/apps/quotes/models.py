from django.contrib.auth import get_user_model

# from apps.users.models import User
from django.db import models
from django.utils.translation import gettext as _

User = get_user_model()


class Quote(models.Model):
    """
    A model representing a quote.
    """

    class Meta:
        verbose_name = _("Quote")
        verbose_name_plural = _("Quotes")
        ordering = ("text",)

    text = models.TextField(null=False, help_text="The text of the quote.")
    added_by = models.ForeignKey(
        User, on_delete=models.CASCADE, help_text="The user added the quote."
    )
    # TODO:
    # book = models.ForeignKey("Book", on_delete=models.CASCADE)
    # tags = models.ManyToManyField("Tag", on_delete=models.CASCADE)
    # likes = models.ManyToManyField("Like", on_delete=models.CASCADE)
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="The date of creation of the quote."
    )
    updated_at = models.DateTimeField(
        auto_now=False, help_text="The date when the quote was changed."
    )

    def __str__(self):
        return f"Quote: {self.text}"

    # TODO:
    # def number_of_likes(self):
    #     return len(self.likes)


class FavoriteQuote(models.Model):
    """
    A model representing a favorite quote.
    """

    class Meta:
        verbose_name = _("Favorite quote")
        verbose_name_plural = _("Favorite quotes")
        ordering = ("quote",)

    quote = models.ForeignKey(
        Quote, on_delete=models.CASCADE, help_text="The object of the quote."
    )

    added_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="the user added the quote to favorite.",
    )
    created_at = models.DateTimeField(
        auto_now=True, help_text="The date of adding quote to favorite."
    )
    updated_at = models.DateTimeField(auto_now=False)

    def __str__(self):
        return f"Favorite Quote: {self.quote}"
