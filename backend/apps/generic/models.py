from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Like(models.Model):
    """
    Model representing a "like" by a user on a piece of content.

    Fields:
        user (models.ForeignKey): Foreign key to the User who made the like.
        content_type (models.ForeignKey): Foreign key to the ContentType of the liked content.
        object_id (models.PositiveIntegerField): Primary key of the liked content.
        content_object (GenericForeignKey): Generic foreign key to the liked content.
    """

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    LIKE = "L"
    DISLIKE = "D"
    TYPE_CHOICES = [
        (LIKE, "Like"),
        (DISLIKE, "Dislike"),
    ]
    like_type = models.CharField(max_length=1, choices=TYPE_CHOICES)

    class Meta:
        """
        Meta options for the Like model.
        """

        ordering = ["user"]
        verbose_name = "Like"
        verbose_name_plural = "Likes"

    def likes_counter(self):

        # Get all the likes for the given content type and object id
        likes = Like.objects.filter(
            content_type=self.content_type, object_id=self.object_id, like_type="L"
        )

        # Count the number of dislikes and return the result
        return likes.count()

    def dislikes_counter(self):

        # Get all the dislikes for the given content type and object id
        dislikes = Like.objects.filter(
            content_type=self.content_type, object_id=self.object_id, like_type="D"
        )

        # Count the number of dislikes and return the result
        return dislikes.count()
