from django.apps import AppConfig

_startup_superuser_checked = False


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        global _startup_superuser_checked

        if _startup_superuser_checked:
            return

        from accounts.bootstrap import (
            ensure_default_superuser,
            should_attempt_startup_superuser_creation,
        )

        if not should_attempt_startup_superuser_creation():
            return

        _startup_superuser_checked = True
        ensure_default_superuser()
