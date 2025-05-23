from celery import shared_task
from django.core.mail import send_mass_mail
from django.conf import settings
from .models import CustomUser


@shared_task
def send_newsletter(subject, message):
    recipients = list(
        CustomUser.objects.filter(is_email_verified=True).values_list(
            "email", flat=True
        )
    )
    emails = [
        (subject, message, settings.DEFAULT_FROM_EMAIL, [email]) for email in recipients
    ]
    send_mass_mail(emails, fail_silently=False)
