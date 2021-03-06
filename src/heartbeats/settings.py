"""
Django settings for heartbeats project.

Generated by 'django-admin startproject' using Django 2.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'k7vu#b2z5hh9!2fj%7ynzcw*0@rdiimjwxww2we3ouy(x79-zf'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'corsheaders',
    'silk',
    'django_q',
    'djmail',
    'app'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'silk.middleware.SilkyMiddleware'
]

ROOT_URLCONF = 'heartbeats.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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


WSGI_APPLICATION = 'heartbeats.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        "HOST": os.environ['DB_HOST'],
        'PORT': os.environ['DB_PORT'],
        'USER': 'root',
        "PASSWORD": os.environ['DB_PASSWORD'],
        'NAME': os.environ['DB_NAME'],
        'TEST': {'CHARSET': 'UTF8'}
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'Zh-cn'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True
# When USE_TZ is True and the database doesn't support time zones (e.g.
# SQLite, MySQL, Oracle), Django reads and writes datetimes in local time
# according to this option if it is set and in UTC if it isn't.
CORS_ORIGIN_ALLOW_ALL = True

SILKY_AUTHENTICATION = True  # User must login
SILKY_AUTHORISATION = True  # User must have permissions


def SILKY_PERMISSIONS(user): return user.is_superuser


SILKY_META = True  # silk保存到数据库耗时
SILKY_PYTHON_PROFILER = True
SILKY_MAX_REQUEST_BODY_SIZE = -1  # Silk takes anything <0 as no limit
SILKY_MAX_RESPONSE_BODY_SIZE = 1024  # If response body>1024kb, ignore


SILKY_MAX_RECORDED_REQUESTS = 500  # 限制记录数，避免数据库持续增长
SILKY_MAX_RECORDED_REQUESTS_CHECK_PERCENT = 100
# 实际呢, 就是当 10 / 100 >= random.random() 时,清除50条记录.
# 这俩配置是一起生效的.


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
REST_FRAMEWORK = {
    'DATETIME_FORMAT': "%Y-%m-%d %H:%M:%S",
}


DJMAIL_REAL_BACKEND = "djmail.backends.async.EmailBackend"
DEFAULT_FROM_EMAIL = os.environ['DEFAULT_FROM_EMAIL']
EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']


EMAIL_PORT = int(os.environ['EMAIL_PORT'])
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_USE_TLS = True


STATIC_URL = '/static_django/'
STATIC_ROOT = os.path.join(BASE_DIR, "static_django")


# Django Q config
Q_CLUSTER = {
    'name': 'DjangORM',
    'workers': 5,
    'timeout': 25 * 60,  # 25分钟任务还未完成就杀掉
    'retry': 60 * 30,  # 30min 还未执行完就会再次触发任务
    'queue_limit': 100,
    'save_limit': 500,
    'bulk': 5,
    'sync': False,
    'daemonize_workers': False,  # 允许worker创建子进程
    'orm': 'default',
    'catch_up': False  # 当由于某种原因导致scheduler未触发任务，中间漏掉的时间就忽略掉
}

LOG_DIR = os.path.join(BASE_DIR, "log")
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s'}
    },
    'filters': {
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, "default.log"),  # 日志输出文件
            'maxBytes': 1024 * 1024 * 5,  # 文件大小
            'backupCount': 5,  # 备份份数
            'formatter': 'standard',  # 使用哪种formatters日志格式
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, "error.log"),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'app_handler': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, "app.log"),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'standard',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['default', 'error'],
            'level': 'INFO',
            'propagate': False
        },
        'app': {
            'handlers': ['app_handler'],
            'level': 'INFO',
            'propagate': False
        }
    }
}
