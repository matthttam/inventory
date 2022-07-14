"""
Django settings for inventory project.

Generated by 'django-admin startproject' using Django 4.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import environ
import os

env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = environ.Path(__file__) - 3

environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

SECRET_KEY = env.str("SECRET_KEY")
DEBUG = env.bool("DEBUG", default=False)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

# Application definition
INSTALLED_APPS = [
    "authentication",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "debug_toolbar",
    "dashboard",
    "devices",
    "locations",
    "people",
    "assignments",
    "googlesync",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "login_required.middleware.LoginRequiredMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "inventory.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "inventory.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# DATABASES = {
#    "default": {
#        "ENGINE": "django.db.backends.sqlite3",
#        "NAME": BASE_DIR / "db.sqlite3",
#    }
# }
DATABASES = {"default": env.db("DATABASE_URL")}

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


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/Chicago"


USE_I18N = True

USE_TZ = True

# Enable FORMAT_MODULE_PATH so L10N can customize formats by locale in 'inventory.formats'.
# https://docs.djangoproject.com/en/4.0/ref/settings/#format-module-path
# USE_L10N = True # Deprecated. Always True in 5.0.
FORMAT_MODULE_PATH = [
    "inventory.formats",
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = env("STATIC_URL")
STATIC_ROOT = Path(BASE_DIR.parent).joinpath(env("STATIC_PATH"))

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Default redirect after login
LOGIN_REDIRECT_URL = "/"

# Paths that do not require a logged in session
# https://github.com/CleitonDeLima/django-login-required-middleware

LOGIN_REQUIRED_IGNORE_PATHS = [
    r"/accounts/logout/$",
    r"/accounts/signup/$",
    r"/accounts/login/$",
    r"/admin/$",
]

LOGIN_REQUIRED_IGNORE_VIEW_NAMES = [
    #'authentication'
]

# Controls if the django-debug-toolbar is displayed
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html
INTERNAL_IPS = [
    "127.0.0.1",
]
