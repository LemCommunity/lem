from apps.users.models import User
from django.db import models


# # Create your models here.
class Quote(models.Model):
    """
    A model representing a quote.
    """

    text = models.TextField(null=False, help_text="The text of the quote.")
    added_by = models.ForeignKey(
        User, on_delete=models.CASCADE, help_text="The user added the quote."
    )
    # book = models.ForeignKey("Book", on_delete=models.CASCADE)
    # tags = models.ManyToManyField("Tag", on_delete=models.CASCADE)
    # likes = models.ManyToManyField("Like", on_delete=models.CASCADE)
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="The date of creation of the quote."
    )
    last_updated = models.DateTimeField(
        auto_now=False, help_text="The date when the quote was changed."
    )

    class Meta:
        ordering = ("text",)

    def __str__(self):
        return f"Quote: {self.text}"


#     # def number_of_likes(self):
#     #     return len(self.likes)


class FavoriteQuote(models.Model):
    """
    A model representing a favorite quote.
    """

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
    last_updated = models.DateTimeField(auto_now=False)

    class Meta:
        ordering = ("quote",)

    def __str__(self):
        return f"Favorite Quote: {self.quote}"
