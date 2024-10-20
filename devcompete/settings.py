"""
Django settings for devcompete project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-smx=65#5rdp@759n-nj2dk)(md1lwp!3*3$3gv$4d(26l-nzdu'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["https://devcompete.azurewebsites.net", "http://devcompete.azurewebsites.net","devcompete.azurewebsites.net","*"]

CORS_ALLOWED_ORIGINS = ["*"]
CSRF_TRUSTED_ORIGINS = ["https://devcompete.azurewebsites.net", "http://devcompete.azurewebsites.net"]
if os.getenv('WEBSITE_HOSTNAME') is not None:
    CORS_ALLOWED_ORIGINS.append('https://'+ os.environ['WEBSITE_HOSTNAME'])
    CORS_ALLOWED_ORIGINS.append('http://'+ os.environ['WEBSITE_HOSTNAME'])
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = [
    "https://devcompete.azurewebsites.net", "http://devcompete.azurewebsites.net","devcompete.azurewebsites.net"]

if os.getenv('WEBSITE_HOSTNAME') is not None:
    CORS_ORIGIN_WHITELIST.append('https://'+ os.environ['WEBSITE_HOSTNAME'])
    CORS_ORIGIN_WHITELIST.append('http://'+ os.environ['WEBSITE_HOSTNAME'])

SECURE_SSL_REDIRECT = \
    os.getenv('SECURE_SSL_REDIRECT', '0').lower() in ['true', 't', '1']
if SECURE_SSL_REDIRECT:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Application definition

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "allauth_ui",
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.auth0',
    "widget_tweaks",
    'contest',
    'users',
    'channels',
    'pratice',
    'ckeditor'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

ROOT_URLCONF = 'devcompete.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'devcompete.wsgi.application'
ASGI_APPLICATION = 'devcompete.asgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
EMAIL_BACKEND = "django.core.mail.backends.dummy.EmailBackend"

# if os.getenv('WEBSITE_HOSTNAME') is not None:
DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
    'default': {
    # 'ENGINE': 'django.db.backends.mysql',
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': os.getenv("DB_NAME"),
    'USER': os.getenv("DB_USER"),
    'PASSWORD': os.getenv("DB_PASS"),
    'HOST': os.getenv("DB_HOST"),
    'PORT': os.getenv("DB_PORT", 5432),
    # 'SSL': 'ENABLED'
    }
}
# else:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': BASE_DIR / 'db.sqlite3',
#         }
#     }
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {   
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

ACCOUNT_EMAIL_REQUIRED = True

SOCIALACCOUNT_PROVIDERS = {
    'auth0': {
        'AUTH0_URL': 'https://devcompete.us.auth0.com',
        'OAUTH_PKCE_ENABLED': True,
    }
}
if os.getenv('WEBSITE_HOSTNAME') is not None:
    ACCOUNT_DEFAULT_HTTP_PROTOCOL='https'
else:
    ACCOUNT_DEFAULT_HTTP_PROTOCOL='http'

# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels_redis.core.RedisChannelLayer',

#         'CONFIG': {
#             "hosts": [{
#             "address": os.getenv("REDIS_URL"),  # "REDIS_TLS_URL"
#         }],
#         },
#     },
# }

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
