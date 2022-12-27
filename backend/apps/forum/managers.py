from django.db import models


class PostManager(models.Manager):
    def sum_posts(self):
        return super().count()


class ReplyManager(models.Manager):
    pass
