from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Newsletter(models.Model):
    subject = models.CharField(max_length=255, verbose_name="Тема письма")
    message = models.TextField(verbose_name="Текст письма")
    created_at = models.DateTimeField(auto_now_add=True)
    sent = models.BooleanField(default=False, verbose_name="Отправлено")

    def __str__(self):
        return self.subject


class Subscriber(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="subscriber"
    )
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, verbose_name="Активная подписка")

    def __str__(self):
        return self.user.email

    @classmethod
    def active_emails(cls):
        return cls.objects.filter(is_active=True).values_list("user__email", flat=True)
