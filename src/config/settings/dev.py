from .base import *

DEBUG = os.getenv("DEBUG", default="True") in ["True", "true"]

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", default="").split(",")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

ZIBAL_MERCHANT_ID = "zibal"
