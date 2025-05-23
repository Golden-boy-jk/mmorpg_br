from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.conf import settings
from django.urls import reverse
from django.template.loader import render_to_string

from .models import CustomUser


@receiver(post_save, sender=CustomUser)
def handle_new_user(sender, instance, created, **kwargs):
    if created:
        # Добавляем пользователя в группу
        group, _ = Group.objects.get_or_create(name="default_users")
        instance.groups.add(group)

        # Отправляем письмо, если пользователь не активен
        if not instance.is_active and instance.verification_code:
            confirmation_link = f"{settings.SITE_URL}{reverse('ads:verify_email', kwargs={'code': instance.verification_code})}"

            subject = "Подтверждение регистрации"
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [instance.email]
            text_content = "Для подтверждения открой письмо в HTML-формате."
            html_content = render_to_string(
                "email/confirmation_email.html",
                {"user": instance, "confirmation_link": confirmation_link},
            )

            msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
            msg.attach_alternative(html_content, "text/html")
            msg.send()
