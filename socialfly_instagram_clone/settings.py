import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY','something')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG',True)

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    #3rd party
     'simple_history',
     'channels',
    
    # Providers
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',


    'crispy_forms',
    'easy_thumbnails',

    #ALLAUTH APPS
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    #my apps
    'core',
    'users.apps.UsersConfig',
    'posts',
    'chats',
]

AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend'
]

SITE_ID = 2

ACCOUNT_EMAIL_REQUIRED=True
ACCOUNT_EMAIL_VERIFICATION="none"
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_LOGOUT_ON_GET = True 
ACCOUNT_SESSION_REMEMBER=True

LOGIN_REDIRECT_URL="posts:explore"
ACCOUNT_SIGNUP_REDIRECT_URL="user:profile_edit"
ACCOUNT_LOGOUT_REDIRECT_URL="account_login"

# SOCIALACCOUNT_QUERY_EMAIL = True
# ACCOUNT_LOGOUT_ON_GET= True
# ACCOUNT_UNIQUE_EMAIL = True
# ACCOUNT_EMAIL_REQUIRED = True


#CHAT SETTINGS
ASGI_APPLICATION = 'socialfly_instagram_clone.asgi.application'


MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
     'simple_history.middleware.HistoryRequestMiddleware',
]

ROOT_URLCONF = 'socialfly_instagram_clone.urls'

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

WSGI_APPLICATION = 'socialfly_instagram_clone.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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





# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/


LANGUAGE_CODE = 'en-us'

TIME_ZONE =  'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATICFILES_DIRS = [BASE_DIR/'static',]
STATIC_ROOT = BASE_DIR/'static_root'
MEDIA_ROOT = BASE_DIR/'media_root'

from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
        messages.DEBUG: 'secondary',
        messages.INFO: 'info',
        messages.SUCCESS: 'success',
        messages.WARNING: 'warning',
        messages.ERROR: 'danger',
 }

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#HISTORY SETINGS 
SIMPLE_HISTORY_REVERT_DISABLED=True
SIMPLE_HISTORY_HISTORY_ID_USE_UUID = True

#REDIS
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [("127.0.0.1", 6379)],
            # "hosts": [('redis://:bho4IPFEczahprp1SlfOQTYaJUFip41y@redis-17575.c15.us-east-1-4.ec2.cloud.redislabs.com:17575/0')],
        },
    },
}



CELERY_BROKER_URL = "redis://:bho4IPFEczahprp1SlfOQTYaJUFip41y@redis-17575.c15.us-east-1-4.ec2.cloud.redislabs.com:17575/0"
CELERY_RESULT_BACKEND = "redis://:bho4IPFEczahprp1SlfOQTYaJUFip41y@redis-17575.c15.us-east-1-4.ec2.cloud.redislabs.com:17575/0"

