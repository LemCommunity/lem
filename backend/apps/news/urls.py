from django.urls import path

from . import views

# temporary
app_name = "news"
urlpatterns = [
    path("", views.welcome, name="welcome"),
]
