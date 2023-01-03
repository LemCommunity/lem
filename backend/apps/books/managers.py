from django.db import models


class ReviewManager(models.Manager):
    def all_reviews(self):
        return self.all()

    def positive_reviews(self):
        return self.filter(score__gte=3)

    def negative_reviews(self):
        return self.filter(score__lt=3)
