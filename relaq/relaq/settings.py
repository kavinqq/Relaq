import os
from pathlib import Path

from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

dotenv_path = os.path.join(BASE_DIR, "config", ".env")
load_dotenv(dotenv_path=dotenv_path)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-#%+v(9*022+x()--5bfy#l-twba-fn#dhto#ls_t2%0kue(pgc'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    # django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # project apps
    'core',
    'cms',
    'googlemap',
    'outscrapers',

    # third party apps
    'ckeditor',
    'ckeditor_uploader',
    'rest_framework',
    'drf_yasg',
    'corsheaders',    
]


CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]


MIDDLEWARE = [
    # Project middleware
    'core.middleware.request_logging.RequestLoggingMiddleware',

    # CORS middleware
    'corsheaders.middleware.CorsMiddleware',

    # Django middleware
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'relaq.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'relaq.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'zh-Hant'

TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# API keys
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OUTSCRAPER_API_KEY = os.getenv('OUTSCRAPER_API_KEY')
GOOGLE_MAP_API_KEY = os.getenv('GOOGLE_MAP_API_KEY')
PERPLEXITY_API_KEY = os.getenv('PERPLEXITY_API_KEY')

# Catch Limit
CATCH_LIMIT = int(os.getenv('CATCH_LIMIT'))

# admin settings
ADMIN_SITE_HEADER = "Relaq CMS"
ADMIN_SITE_TITLE = "Relaq CMS"
ADMIN_INDEX_TITLE = "Relaq 後台"

# Selenium settings
CHROMIUM_BINARY = os.getenv('CHROMIUM_BINARY')
CHROMEDRIVER_PATH = os.getenv('CHROMEDRIVER_PATH')


# CKEditor settings
CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"  # 注意：這裡要用 URL 路徑，不是文件系統路徑

# 加入基本設定
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': "100%",
    },
}

CKEDITOR_UPLOAD_PATH = 'uploads/'

# Media files (Uploaded files)
MEDIA_URL = '/media/'  # 這是對外的 URL 路徑
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # 這是實際儲存的路徑

# 確保 media 目錄存在
if not os.path.exists(MEDIA_ROOT):
    os.makedirs(MEDIA_ROOT)

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
}

# Swagger settings
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Basic': {
            'type': 'basic'
        },
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

# Logging settings
BASE_LOG_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(BASE_LOG_DIR, exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "formatters": {
        "standard": {
            "format": "[%(asctime)s][%(levelname)s][%(name)s:%(lineno)d]：%(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "simple": {
            "format": "[%(asctime)s][%(levelname)s]：%(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "default": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(BASE_LOG_DIR, "debug.log"),
            "maxBytes": 1024 * 1024 * 100,
            "backupCount": 5,
            "formatter": "standard",
            "encoding": "utf-8",
        },
        "warn": {
            "level": "WARN",
            "class": "logging.handlers.RotatingFileHandler",  
            "filename": os.path.join(BASE_LOG_DIR, "warn.log"),  
            "maxBytes": 1024 * 1024 * 100,  
            "backupCount": 5,  
            "formatter": "standard",  
            "encoding": "utf-8",
        },
        "error": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",  
            "filename": os.path.join(BASE_LOG_DIR, "error.log"),  
            "maxBytes": 1024 * 1024 * 100,  
            "backupCount": 5,  
            "formatter": "standard",  
            "encoding": "utf-8",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console", "default", "warn", "error"],
            "level": "INFO",
            "propagate": False,
        },
    }
}

# Google Map Photo Size
MAX_PHOTO_WIDTH = int(os.getenv('MAX_PHOTO_WIDTH'))
MAX_PHOTO_HEIGHT = int(os.getenv('MAX_PHOTO_HEIGHT'))

# Domain setting for full URLs
DOMAIN = (
    "http://127.0.0.1:8000"
    if DEBUG
    else os.getenv('DOMAIN')
)
