# newsletter/management/commands/send_newsletter.py
from django.core.management.base import BaseCommand
from django.core.mail import send_mass_mail
from users.models import User
from newsletter.models import Newsletter


class Command(BaseCommand):
    help = "Send unsent newsletter emails to subscribed users"

    def handle(self, *args, **kwargs):
        newsletters = Newsletter.objects.filter(sent=False)

        for newsletter in newsletters:
            users = User.objects.filter(is_subscribed=True)
            messages = [
                (
                    newsletter.subject,
                    newsletter.message,
                    "from@example.com",
                    [user.email],
                )
                for user in users
            ]

            send_mass_mail(messages, fail_silently=False)
            newsletter.sent = True
            newsletter.save()

        self.stdout.write(self.style.SUCCESS("Newsletters sent successfully."))
