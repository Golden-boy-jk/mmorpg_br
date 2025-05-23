from django.urls import path
from . import views

urlpatterns = [
    path("newsletter/", views.send_newsletter_view, name="send_newsletter"),
]
