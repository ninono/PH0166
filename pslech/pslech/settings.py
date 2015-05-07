# -*- coding: utf-8 -*-
"""
Django settings for pslech project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

PROJECT_NAME = 'PSLE CHINESE 华文阅读理解训练系统'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Email settings
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'pslechinesenoreply@gmail.com'
EMAIL_HOST_PASSWORD = 'finalyearproject2014'
EMAIL_PORT = 587
EMAIL_USE_TLS = True


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'rv%0n45xcx&$uz$vo03n4x!(do)8&#zdcu8(tq69^)97d02kss'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition
GRAPH_MODELS = {
        'all_applications':True,
        'group_models':True,
        }

INSTALLED_APPS = (
    'pslechdb',
    'pslechweb',
    'grading',
    'suit',
    'django_extensions',

    'django_ajax',
    'nested_inline',
    'smart_selects',
    'redactor',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'pslech.urls'

WSGI_APPLICATION = 'pslech.wsgi.application'


#WYSIWYG editor
REDACTOR_OPTIONS = {'lang': 'en', 'plugins': ['table'],'buttons':['html', 'formatting', 'bold', 'italic', 'deleted',
'unorderedlist', 'orderedlist', 'outdent', 'indent',
'link', 'alignment', 'horizontalrule','underline']}
REDACTOR_UPLOAD = 'uploads/'
# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':'pslechdb',
        'USER':'ninono',
        'PASSWORD':'abc123',
        'HOST':'',
        'PORT':'',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_ROOT=""
STATIC_URL = '/static/'
STATICFILES_DIRS = (
        os.path.join(BASE_DIR,'static'),
        )
STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        )
#templates
TEMPLATE_DIRS=(
        os.path.join(BASE_DIR,'templates'),
        )
STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        )
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',

    'pslech.context_processors.site_values'
        )
