from django.apps import AppConfig
from django.core.signals import request_finished


class ForumConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "backend.apps.forum"

    def ready(self):
        from backend.apps.forum import signals

        request_finished.connect(signals.category_name)
        request_finished.connect(signals.category_lenght)
        request_finished.connect(signals.post_title)
