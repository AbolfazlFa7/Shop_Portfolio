from .base import *

DEBUG = os.getenv("DEBUG", default="True") in ["True", "true"]

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", default="").split(",")

INSTALLED_APPS += [
    # 'debug_toolbar',
]


# Debug Toolbar
# INSTALLED_APPS += ['debug_toolbar']
# MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
# INTERNAL_IPS = [
#     "127.0.0.1",
#     "localhost",
# ]


# Custom middleware
MIDDLEWARE.append("config.middlewares.query_logger.QueryLoggerMiddleware")
QUERY_LOGGER_JUST_COUNT = False  # if False, Show all Query commands too


# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "db.sqlite3",
        # 'USER': env('DATABASE_USER',cast=str),
        # 'PASSWORD': env('DATABASE_PASSWORD',cast=str),
        # 'HOST': env('DATABASE_HOST',cast=str),
        # 'PORT': env('DATABASE_PORT',cast=str),
    }
}

# JWT
JWT_SETTINGS = {
    **JWT_SETTINGS,
    "ACCESS_LIFETIME": timedelta(days=1357),
    "REFRESH_LIFETIME": timedelta(days=1980),
}

# Cache
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "portfolio",
    }
}

# Email
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# Zibal
ZIBAL_MERCHANT_ID = "zibal"
