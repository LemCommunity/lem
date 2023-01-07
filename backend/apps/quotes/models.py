from django.contrib.auth import get_user_model
from django.db import models

from apps.quotes.managers import ChalengeCommentManager, ChalengeManager

# Create your models here.
User = get_user_model()


class Challenge(models.Model):
    """A model representing a challenge model.

    Fields:
        active (BooleanField): Whether the user actived the challenge
        book_to_read (IntegerField): how many books user the user needs to read
        books_read (IntegerField): how many books the user has read
        created_at (DateTimeField): The creation datetime of the Post. This field is set
            automatically to the current time when the Post object is first created.
        updated_at (DateTimeField): The update datetime of the Post. This field is set
            automatically to the current time when the Post object is updated.
        user (ForeignKey): the user who took up the challenge
    """

    class Meta:
        verbose_name = "Chalenge"
        verbose_name_plural = "Chalenges"

    object = ChalengeManager()

    active = models.BooleanField(default=False)

    book_to_read = models.IntegerField

    books_read = models.IntegerField

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created at",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated at",
    )

    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="challenges"
    )

    def __str__(self) -> str:
        """Return the string representation of the model."""
        return "Chalenge"


class ChalengeComments(models.Model):
    """A model representing a challenge model.

    Fields:
        comment (TextField): The user comment to The Chalenge
        created_at (DateTimeField): The creation datetime of the Post. This field is set
            automatically to the current time when the Post object is first created.
        updated_at (DateTimeField): The update datetime of the Post. This field is set
            automatically to the current time when the Post object is updated.
        user (ForeignKey): the user who write the comment
        challenge ForeignKey): which chalenge is commented
        reply_to (ForeignKey): optional if comment is reply to another comment
    """

    object = ChalengeCommentManager()

    comment = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created at",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated at",
    )
    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="challenges_comment"
    )

    challenge = models.ForeignKey(
        Challenge, on_delete=models.DO_NOTHING, related_name="chalenge"
    )

    reply_to = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.DO_NOTHING, related_name="reply"
    )

    def __str__(self) -> str:
        """Return the string representation of the model."""
        return str(self.comment)

    @property
    def replies_amount(self):
        """It returns the amount of replies a reply has as children."""
        return self.reply.count()
