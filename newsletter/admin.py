from django.contrib import admin
from .models import Newsletter, Subscriber


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ("subject", "created_at", "sent")
    list_filter = ("sent",)
    search_fields = ("subject", "message")


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("user", "is_active", "subscribed_at")
    list_filter = ("is_active",)
    search_fields = ("user__email",)
