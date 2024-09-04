"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os

from django.core.management.utils import get_random_secret_key

from pathlib import Path

import django_heroku

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY", get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "t", "1")

# Allowed origins on CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    os.getenv(
        "FRONTEND_DEV_URL",
        "https://2024-1-measure-soft-gram.vercel.app",
    ),
    os.getenv(
        "FRONTEND_PROD_URL",
        "https://2024-1-measure-soft-gram.vercel.app",
    ),
]
CORS_ALLOW_CREDENTIALS = True

STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Application definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django_extensions",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework.authtoken",
    "simple_history",
    "corsheaders",
    "debug_toolbar",
    "dj_rest_auth",
    "dj_rest_auth.registration",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.github",
    "django_apscheduler",
]

APPLICATION_APPS = [
    "accounts",
    "organizations",
    "metrics",
    "measures",
    "subcharacteristics",
    "characteristics",
    "tsqmi",
    "release_configuration",
    "goals",
    "entity_trees",
    "math_model",
    "utils",
    "releases",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + APPLICATION_APPS

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware"
]

CSRF_TRUSTED_ORIGINS = [
    "https://*.2023-2-measuresoftgram-service-production.up.railway.app"
]
ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

POSTGRES_DB = os.getenv("POSTGRES_DB", "postgres")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "0.0.0.0")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": POSTGRES_DB,
        "USER": POSTGRES_USER,
        "PASSWORD": POSTGRES_PASSWORD,
        "HOST": POSTGRES_HOST,
        "PORT": POSTGRES_PORT,
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


django_heroku.settings(locals())

# Django Rest Framework config
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 500,
    "DEFAULT_PARSER_CLASSES": ("rest_framework.parsers.JSONParser",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
    ),
}

# allauth related configs
SITE_ID = int(os.getenv("SITE_ID", "1"))

UNIQUE_EMAIL = False
ACCOUNT_EMAIL_VERIFICATION = "none"

LOGIN_REDIRECT_URL = os.getenv("LOGIN_REDIRECT_URL", "127.0.0.1:8080")

SOCIALACCOUNT_PROVIDERS = {
    "github": {
        "APP": {
            "client_id": os.getenv("GITHUB_CLIENT_ID", ""),
            "secret": os.getenv("GITHUB_SECRET", ""),
        },
        "SCOPE": [
            "read:user",
            "user:email",
            "read:project",
            "read:org",
            "repo",
        ],
    }
}

CREATE_FAKE_DATA = os.getenv("CREATE_FAKE_DATA", "False").lower() in (
    "true",
    "t",
    "1",
)

AMBIENT_TEST_OR_DEV = os.getenv("AMBIENT_TEST_OR_DEV", "True").lower() in (
    "true",
    "t",
    "1",
)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")

GITHUB_ISSUE_METRICS_THRESHOLD = int(os.getenv("GITHUB_ISSUE_METRICS_THRESHOLD", "7"))

MAXIMUM_NUMBER_OF_HISTORICAL_RECORDS = int(
    os.getenv(
        "MAXIMUM_NUMBER_OF_HISTORICAL_RECORDS",
        "100",
    )
)

GITHUB_PIPELINE_METRICS_THRESHOLD = int(
    os.getenv("GITHUB_PIPELINE_METRICS_THRESHOLD", "90")
)

DATA_UPLOAD_MAX_NUMBER_FIELDS = int(
    os.getenv(
        "DATA_UPLOAD_MAX_NUMBER_FIELDS",
        "100000",
    )
)

AUTH_USER_MODEL = "accounts.CustomUser"

if DEBUG:
    import socket  # only if you haven't already imported this

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + [
        "127.0.0.1",
        "10.0.2.2",
    ]

GITHUB_METRICS = [
    {
        "key": "sum_ci_feedback_times",
        "name": "Sum of time spent in seconds on builds",
        "metric_type": "INT",
    },
    {
        "key": "total_builds",
        "name": "Total build count",
        "metric_type": "INT",
    },
    {
        "key": "resolved_issues",
        "name": "Total resolved issues count on the release period",
        "metric_type": "INT",
    },
    {
        "key": "total_issues",
        "name": "Total issues count on the release period",
        "metric_type": "INT",
    },
]

GITHUB_SUPPORTED_MEASURES = [
    {
        "team_throughput": {
            "metrics": [
                "resolved_issues",
                "total_issues",
            ]
        }
    },
    {"ci_feedback_time": {"metrics": ["sum_ci_feedback_times", "total_builds"]}},
]

SCHEDULER_CONFIG = {
    "apscheduler.jobstores.default": {
        "class": "django_apscheduler.jobstores:DjangoJobStore",
    },
    "apscheduler.executors.default": {
        "class": "apscheduler.executors.pool:ThreadPoolExecutor",
        "max_workers": "1",
    },
    "apscheduler.job_defaults.coalesce": "false",
    "apscheduler.job_defaults.max_instances": "1",
    "apscheduler.timezone": "America/Sao_Paulo",
}
SCHEDULER_AUTOSTART = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
        },
    },
}
