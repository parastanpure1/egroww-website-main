import os
import sys

from django.contrib.auth import get_user_model
from django.db import DEFAULT_DB_ALIAS, connections
from django.db.utils import OperationalError, ProgrammingError

from accounts.models import User


def should_attempt_startup_superuser_creation():
    skipped_commands = {
        "makemigrations",
        "migrate",
        "collectstatic",
        "shell",
        "dbshell",
        "createsuperuser",
        "create_default_superuser",
        "test",
    }

    if len(sys.argv) > 1 and sys.argv[1] in skipped_commands:
        return False

    if "runserver" in sys.argv and os.environ.get("RUN_MAIN") != "true":
        return False

    return True


def ensure_default_superuser():
    username = os.getenv("DEFAULT_SUPERUSER_USERNAME", "admin")
    email = os.getenv("DEFAULT_SUPERUSER_EMAIL", "admin@example.com")
    password = os.getenv("DEFAULT_SUPERUSER_PASSWORD", "admin123")

    user_model = get_user_model()
    connection = connections[DEFAULT_DB_ALIAS]

    try:
        existing_tables = connection.introspection.table_names()
    except (OperationalError, ProgrammingError):
        return False, "Database unavailable; skipped default superuser creation."

    if user_model._meta.db_table not in existing_tables:
        return False, "User table not ready; skipped default superuser creation."

    if user_model.objects.filter(username=username).exists():
        return False, f"Superuser '{username}' already exists. No changes made."

    user = user_model.objects.create_superuser(
        username=username,
        email=email,
        password=password,
    )
    if hasattr(user, "role"):
        user.role = User.Role.ADMIN
        user.save(update_fields=["role"])

    return True, f"Superuser '{username}' created successfully."
