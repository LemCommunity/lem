from django.db import models


class PostManager(models.Manager):
    def sum_posts(self):
        return len(super().all())


class ReplyManager(models.Manager):
    def sum_replies(self, id):
        return len(super().get(id=id).children.all())
