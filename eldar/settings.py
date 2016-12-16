# """
# Django settings for eldar project.

# Generated by 'django-admin startproject' using Django 1.8.

# For more information on this file, see
# https://docs.djangoproject.com/en/1.8/topics/settings/

# For the full list of settings and their values, see
# https://docs.djangoproject.com/en/1.8/ref/settings/
# """

# # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# # Quick-start development settings - unsuitable for production
# # See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=pa)h(2gy8p$629)u4()2ha+--rufkc7a967vl2xl*i+(bpd58'

# # SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'rest_framework',
	'corsheaders',
	'lager',
	'vaktir',
)

MIDDLEWARE_CLASSES = (
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',	
	'corsheaders.middleware.CorsMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'eldar.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': ['templates',],
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

WSGI_APPLICATION = 'eldar.wsgi.application'


# # Database
# # https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	}
}

# This needs further investigation
CACHES = {
	'default': {
		'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
	}
}


# # Internationalization
# # https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# # Static files (CSS, JavaScript, Images)
# # https://docs.djangoproject.com/en/1.8/howto/static-files/
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
	os.path.join(BASE_DIR,'vaktir/static'),
)

REST_FRAMEWORK = {
  
}

CORS_ORIGIN_ALLOW_ALL = True

# CORS_ORIGIN_WHITELIST = (
# 	'localhost:3000'
# )

# LOGGING = {
# 	'version': 1,
# 	'filters': {
# 		'require_debug_true': {
# 			'()': 'django.utils.log.RequireDebugTrue',
# 		}
# 	},
# 	'handlers': {
# 		'console': {
# 			'level': 'DEBUG',
# 			'filters': ['require_debug_true'],
# 			'class': 'logging.StreamHandler',
# 		}
# 	},
# 	'loggers': {
# 		# 'django': {
# 		# 	'handlers': ['console'],
# 		# 	'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
# 		# },
# 		'django.db.backends': {
# 			'level': 'DEBUG',
# 			'handlers': ['console'],
# 		}
# 	},
# }

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'