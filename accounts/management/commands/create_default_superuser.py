from django.core.management.base import BaseCommand

from accounts.bootstrap import ensure_default_superuser


class Command(BaseCommand):
    help = "Create the default admin superuser if it does not already exist."

    def handle(self, *args, **options):
        created, message = ensure_default_superuser()
        if created:
            self.stdout.write(self.style.SUCCESS(message))
            return
        self.stdout.write(self.style.WARNING(message))
