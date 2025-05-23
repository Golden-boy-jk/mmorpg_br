import logging

from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from .models import Ad, Response, CustomUser, EmailVerificationCode

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Ad)
def send_ad_creation_email(sender, instance, created, **kwargs):
    if created:
        try:
            send_mail(
                f"Ваше объявление '{instance.title}' было успешно создано!",
                f"Здравствуйте, {instance.author.username}!\n\nВаше объявление '{instance.title}' было успешно создано и теперь доступно на платформе.",
                settings.DEFAULT_FROM_EMAIL,
                [instance.author.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Ошибка отправки письма: {str(e)}")


@receiver(pre_delete, sender=Response)
def send_response_deletion_email(sender, instance, **kwargs):
    try:
        send_mail(
            f"Ваш отклик на '{instance.ad.title}' был удален",
            f"Здравствуйте, {instance.user.username}.\n\nВаш отклик на объявление '{instance.ad.title}' был удален автором объявления.",
            settings.DEFAULT_FROM_EMAIL,
            [instance.user.email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Ошибка отправки письма: {str(e)}")


@receiver(post_save, sender=CustomUser)
def send_verification_email(sender, instance, created, **kwargs):
    if created and not instance.is_email_verified:
        code, _ = EmailVerificationCode.objects.get_or_create(user=instance)
        try:
            send_mail(
                subject="Подтверждение регистрации",
                message=f"Ваш код подтверждения: {code.code}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[instance.email],
                fail_silently=False,
            )
        except Exception as e:
            logger.error(f"Ошибка отправки письма подтверждения: {str(e)}")
