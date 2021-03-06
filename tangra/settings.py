"""
Django settings for tangra project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

MEDIA_ROOT = os.path.join(BASE_DIR, 'static/files')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*jzdj)7d44k*6sn08h1dt4rza89+(@1y+0d*68lwlkh_@3evn5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

STATIC_URL = "/static/"
STATICFILES_DIRS = (
    os.path.normpath(os.path.join(BASE_DIR, "static")) + "/",
)

LOGIN_URL = '/admin'

AUTH_USER_MODEL = 'custom_auth.User'

# Email configuration
EMAIL_BACKEND =         'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST =            'smtp.gmail.com'
EMAIL_HOST_USER =       'taglab.developer@gmail.com'
EMAIL_HOST_PASSWORD =   'T4GlabDev'
EMAIL_SUBJECT_PREFIX =  '[Tangra] '
EMAIL_PORT =            587
EMAIL_USE_TLS =         True
EMAIL_HOST_NAME =       'Admin'


SUIT_CONFIG = {
    'ADMIN_NAME': 'Tangra',
    'HEADER_TIME_FORMAT': 'h:i A e',
    'CONFIRM_UNSAVED_CHANGES': True,
    'MENU': (
        # Reorder app models
        {
        'app': 'studies',
        'models': (
            {'model':'auth.user', 'label':'Participants'},
            {'model':'studies.study', 'label':'Studies'},
            'group',
            'userstage'
            ),
        'icon':'icon-leaf'
        },
        # Separator
        '-',
        # Custom app, with models
        {'label': 'Settings', 'icon':'icon-cog', 'url': '#'},
    ),
}


# Application definition

INSTALLED_APPS = (
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'studies',
    'custom_auth',

    # These are for the public API
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # These are for the public API
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
)

ROOT_URLCONF = 'tangra.urls'

WSGI_APPLICATION = 'tangra.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Canada/Eastern'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'

# Setting for the public API.
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES' :(
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    )
}

# Setting for CORS or the API won't work!
CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_HEADERS = (
    'x-requested-with',
    'content-type',
    'accept',
    'origin',
    'authorization',
    'x-csrftoken'
)
