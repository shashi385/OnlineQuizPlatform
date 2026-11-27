#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate

python manage.py shell <<'PY'
import os
from django.contrib.auth import get_user_model

User = get_user_model()

username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "")

if username and password:
    user, created = User.objects.get_or_create(
        **{User.USERNAME_FIELD: username}
    )

    user.is_staff = True
    user.is_superuser = True
    user.is_active = True

    if created or os.environ.get("RESET_ADMIN_PASSWORD") == "1":
        user.set_password(password)

    if hasattr(user, "email"):
        user.email = email

    user.save()
    print("QuizMaster admin account ready!")
else:
    print("Admin creation skipped: environment variables missing.")
PY