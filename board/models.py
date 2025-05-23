from django.urls import reverse
import uuid
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


# Категории
class Category(models.TextChoices):
    TANK = "TANK", "Танки"
    HEALER = "HEALER", "Хилы"
    DD = "DD", "ДД"
    TRADER = "TRADER", "Торговцы"
    GUILDMASTER = "GUILDMASTER", "Гилдмастеры"
    QUESTGIVER = "QUESTGIVER", "Квестгиверы"
    BLACKSMITH = "BLACKSMITH", "Кузнецы"
    LEATHERWORKER = "LEATHERWORKER", "Кожевники"
    ALCHEMIST = "ALCHEMIST", "Зельевары"
    SPELLMASTER = "SPELLMASTER", "Мастера заклинаний"


class Ad(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=Category.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    content = CKEditor5Field("Контент", config_name="extends")
    # video = models.FileField(upload_to='videos/', null=True, blank=True) # если надо загрузить видео

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["category"]),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("ads:ad_detail", kwargs={"pk": self.pk})

    def get_category_label(self):
        return self.get_category_display()


class Response(models.Model):
    STATUS_CHOICES = [
        ("pending", "В ожидании"),
        ("accepted", "Принят"),
        ("rejected", "Отклонён"),
    ]

    ad = models.ForeignKey(Ad, related_name="responses", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="reviewed_responses",
        on_delete=models.SET_NULL,
    )

    class Meta:
        indexes = [
            models.Index(fields=["created_at"]),
        ]
        verbose_name = "Отклик"
        verbose_name_plural = "Отклики"

    def __str__(self):
        return f"Отклик от {self.user.email} на '{self.ad.title}'"

    @property
    def is_accepted(self):
        return self.status == "accepted"

    @property
    def is_rejected(self):
        return self.status == "rejected"


class Newsletter(models.Model):
    subject = models.CharField(max_length=255)
    message = CKEditor5Field("Текст письма", config_name="extends")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.subject


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email


class EmailVerificationCode(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} — {self.code}"

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(hours=24)
