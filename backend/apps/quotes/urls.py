from django.urls import path
from views import quote_cms

urlpatterns = [
    path("", quote_cms, name="welcome"),
]
