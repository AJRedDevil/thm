"""
Django settings for thm project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['LOCAL_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'jobs',
    'south',
    'rest_framework',
    'rest_framework.authtoken',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# AUTH BACKEND DEFINITIONS
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    )
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}
# TEMPLATE CONTEXT DEFINITIONS
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.core.context_processors.media',
)
# TEMPLATE PATH CONFIGURATION 
TEMPLATE_PATH = os.path.join(PROJECT_PATH, 'templates')
TEMPLATE_DIRS = (TEMPLATE_PATH)
## MISCELLANEOUS SETTINGS
ROOT_URLCONF = 'thm.urls'
WSGI_APPLICATION = 'thm.wsgi.application'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Toronto'
USE_I18N = True
USE_L10N = True
USE_TZ = True
APPEND_SLASH = True
# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
# TURN DEBUG OFF
DEBUG = False
TEMPLATE_DEBUG = False
ALLOWED_HOSTS = ['*']

# DATABASE ENGINE CONFIGURATIONS
import dj_database_url
DATABASES = {
    "default": dj_database_url.config()
}



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

# Static asset configuration
# STATIC_URL = 'http://s3.amazonaws.com/%s/' % AWS_STATIC_BUCKET
STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, 'static'),
)
# CONFIGURING QUESTRUSERPROFILE AS THE AUTH BACKEND
AUTH_USER_MODEL = 'users.UserProfile'
# LOGIN URL DEFINITIONS
LOGIN_URL = '/signin/'
LOGIN_REDIRECT_URL = '/home/'
## LOGGING DEFINITION AND CONFIGURATION

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'users': {
            'handlers':['console'],
            'level':'DEBUG',
        },
        'jobs': {
            'handlers':['console'],
            'level':'DEBUG',
        },
    }
}

# LOCAL CONFIG IMPORT, IMPORTS ALL CONFIG FROM local_setting.py, required only for a dev env
try:
    from local_setting import *
except ImportError:
    pass

# # Use amazon S3 storage only on production
# if not DEBUG:
#     ##This for media, user uploaded files
#     DEFAULT_FILE_STORAGE = 'libs.s3utils.MediaRootS3BotoStorage'
#     ##This for CSS,
#     STATICFILES_STORAGE = 'libs.s3utils.StaticRootS3BotoStorage'
#     MEDIA_ROOT = '/%s/' % DEFAULT_FILE_STORAGE
#     MEDIA_URL = '//s3.amazonaws.com/%s/' % AWS_MEDIA_BUCKET