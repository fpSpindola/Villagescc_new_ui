"""
Django settings for ccproject project.

Generated by 'django-admin startproject' using Django 1.9.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
from datetime import timedelta

from database.databases import Database
from database.connection_strings import POSTGRESQL

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'oe@ut#9t8xzd0%19xobf3c4jqa75&#!@+e27ioubq=#r1^4h#8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'ccproject', 'locale/'),
)


SERVER_EMAIL = 'info@villages.cc'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.zoho.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'info@villages.cc'
EMAIL_HOST_USER = 'info@villages.cc'
EMAIL_HOST_PASSWORD = 'infovillagescc'
SITE_DOMAIN = 'villages.cc'
HELP_EMAIL = 'info@villages.cc'
EMAIL_SUBJECT_PREFIX = "[Villages] "

# Application definition

INSTALLED_APPS = [
    'dal',
    'dal_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # Custom apps
    'geo',
    'profile',
    'post',
    'feed',
    'relate',
    'general',
    'pages',
    'admin',
    'about',
    'listings',
    'tags',
    'django_user_agents',

    # Ripple
    'account',
    'payment',
    'management',


    'accounts.apps.AccountsConfig',
    'frontend.apps.FrontendConfig',
    'endorsement.apps.EndorsementConfig',
    'payment_raja.apps.PaymentConfig',
    'categories.apps.CategoriesConfig'

]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'profile.middleware.ProfileMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
    'geo.middleware.LocationMiddleware',
]

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.request",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
)

ROOT_URLCONF = 'ccproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),
                 os.path.join(BASE_DIR, 'accounts', 'templates'),
                 os.path.join(BASE_DIR, 'accounts', 'sign_in', 'templates'),
                 os.path.join(BASE_DIR, 'notification', 'templates'),
                 os.path.join(BASE_DIR, 'listings', 'templates'),
                 os.path.join(BASE_DIR, 'management', 'templates'),
                 os.path.join(BASE_DIR, 'categories', 'templates')],
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

WSGI_APPLICATION = 'ccproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'villages_new_ui',
        'USER': 'postgres',
        'PASSWORD': 'test123!'
    },
    'ripple': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'villagesripple_new_ui',
        'USER': 'postgres',
        'PASSWORD': 'test123!'
    }
}

DATABASE_ROUTERS = ('ripple.router.RippleRouter',)

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = (
    'profile.auth_backends.CaseInsensitiveModelBackend',
)

SESSIONS_DIRECTORY = os.path.join(BASE_DIR, 'sessions')

SESSION_ENGINE = 'django.contrib.sessions.backends.file'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 43200      # 12 hours in seconds
SESSION_FILE_PATH = SESSIONS_DIRECTORY
# SESSION_COOKIE_SECURE = True
LOCATION_COOKIE_NAME = 'location_id'
LOCATION_COOKIE_AGE = timedelta(days=365)

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

ENDORSEMENT_BONUS = 5

FEED_ITEMS_PER_PAGE = 20
LISTING_ITEMS_PER_PAGE = 20

MEDIA_URL = '/media/'

MEDIA_ROOT = 'media'

GEOIP_PATH = '/usr/share/GeoIP'

PASSWORD_RESET_LINK_EXPIRY = timedelta(days=7)

LOCATION_SESSION_KEY = 'location_id'
DEFAULT_LOCATION = ('49.2696243', '-123.0696036')  # East Vancouver.

INVITATION_ONLY = False