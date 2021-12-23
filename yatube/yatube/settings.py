import os

"""Build paths inside the project like this: os.path.join(BASE_DIR, ...)."""
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'posts:index'
"""LOGOUT_REDIRECT_URL = 'posts:index' ."""
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'sent_emails')
NUM_OF_POSTS_ON_PAGE = 10

"""Quick-start development settings - unsuitable for production
See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

SECURITY WARNING: keep the secret key used in production secret!."""
SECRET_KEY = 'zezb)8y%bik%u71pes!j#^5l(@g7o0b4y*jx#a4uwjcm!51ex7'

"""SECURITY WARNING: don't run with debug turned on in production!."""
DEBUG = True

ALLOWED_HOSTS = ['testserver', '127.0.0.1', 'localhost', '[::1]',]

"""Application definition."""

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'posts.apps.PostsConfig',
    'users.apps.UsersConfig',
    'core.apps.CoreConfig',
    'about.apps.AboutConfig',
    'sorl.thumbnail',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'yatube.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.year.year',
            ],
        },
    },
]

WSGI_APPLICATION = 'yatube.wsgi.application'


"""Database
https://docs.djangoproject.com/en/2.2/ref/settings/#databases."""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


"""Password validation
https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators."""

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


"""Internationalization
https://docs.djangoproject.com/en/2.2/topics/i18n/."""

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

"""Static files (CSS, JavaScript, Images)
https://docs.djangoproject.com/en/2.2/howto/static-files/."""

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
HOME_PAGE = '/'
POSTS = '/posts/'
GROUP = '/group/'
PROFILE = '/profile/'
CREATE = '/create/'
