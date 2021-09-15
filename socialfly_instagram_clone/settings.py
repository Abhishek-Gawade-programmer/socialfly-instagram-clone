import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY =  os.getenv('SECRET_KEY','temp')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG',True)

ALLOWED_HOSTS = ['localhost',]


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
     'channels',

     'webpush',
    
    # Providers
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.discord',


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
   'pwa',
]



WEBPUSH_SETTINGS = {
   "VAPID_PUBLIC_KEY": os.getenv('VAPID_PUBLIC_KEY','temp'),
   "VAPID_PRIVATE_KEY": os.getenv('VAPID_PRIVATE_KEY','temp'),
   "VAPID_ADMIN_EMAIL": os.getenv('VAPID_ADMIN_EMAIL','temp'),
}








#PWD SETINGS
PWA_APP_NAME = "Socialfly"
PWA_APP_DESCRIPTION = "Socialfly Web App"
PWA_APP_THEME_COLOR = "#000000"
PWA_APP_BACKGROUND_COLOR = "#ffffff"
PWA_APP_DISPLAY = "standalone"
PWA_APP_SCOPE = "/"
PWA_APP_ORIENTATION = "any"
PWA_APP_START_URL = "/"
PWA_APP_STATUS_BAR_COLOR = "default"



PWA_APP_ICONS = [
    {
        "src": "static/logo.jpg",
        "sizes": "160x160"
    }
]
PWA_APP_ICONS_APPLE = [
    {
        "src": "static/logo.jpg",
        "sizes": "160x160"
    }
]
PWA_APP_SPLASH_SCREEN = [
    {
        "src": "static/icon.png",
        "media": "(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)"
    }
]
PWA_APP_DIR = "ltr"
PWA_APP_LANG = "en-US"




# DJANGO ALLAUTH SETTING
AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend'
]



#FACEBOOK SETINGS 
SOCIAL_AUTH_FACEBOOK_KEY = os.getenv('SOCIAL_AUTH_FACEBOOK_KEY')  # App ID
SOCIAL_AUTH_FACEBOOK_SECRET =os.getenv('SOCIAL_AUTH_FACEBOOK_SECRET') #app key

SITE_ID = 2

ACCOUNT_EMAIL_REQUIRED=True
ACCOUNT_EMAIL_VERIFICATION="mandatory"
ACCOUNT_UNIQUE_EMAIL = True

ACCOUNT_SESSION_REMEMBER=True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS=1
LOGIN_REDIRECT_URL="posts:explore"
ACCOUNT_SIGNUP_REDIRECT_URL="users:profile_edit"
ACCOUNT_LOGOUT_REDIRECT_URL="account_login"
SOCIALACCOUNT_QUERY_EMAIL = True
ACCOUNT_LOGOUT_ON_GET= True





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


#EMAIL SETTINGS

SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY') 

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey' # Exactly that. 
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
EMAIL_PORT = 587 # 25 or 587 (for unencrypted/TLS connections).
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')









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



#REDIS
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}



