from django.shortcuts import redirect
from .tasks import send_newsletter


def send_newsletter_view(request):
    subject = "Новости MMORPG мира"
    message = "Привет! Это свежие новости с твоего любимого форума."

    send_newsletter.delay(subject, message)
    return redirect("home")
