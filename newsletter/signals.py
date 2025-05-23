from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Subscriber

User = get_user_model()


@receiver(post_save, sender=User)
def create_subscriber_for_new_user(sender, instance, created, **kwargs):
    if created:
        Subscriber.objects.create(user=instance)
