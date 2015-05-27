################################################################################
# 
# Human Variome Database Portal.
#
# === License ===
#
# Last Author:   $Author: MelvinLuong $
# Last Modified: $Date: 2014-06-10 10:49:07 +1000 (Tue, 10 Jun 2014) $ 
#
# === Description ===
# Django settings for HVP Portal.
#
################################################################################

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('HVP Admin', 'portal-admin@hvpaustralia.org.au'),
)

BASE_URL = ''

MANAGERS = ADMINS

# Database Settings
DATABASES = {        
    # DEFAULT HVP portal DB settings
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'Portal',     
        'USER': 'root',     
        'PASSWORD': 'password', 
        'HOST': 'localhost', 
        'PORT': '3306'
    },
    
    # LABS DB settings
    'labs': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'Labs',
            'USER': 'root',
            'PASSWORD': 'password',
            'HOST': 'localhost',
            'PORT': '3306'
    }
}

# EMAIL server settings
EMAIL_HOST = 'mail.hvpaustralia.org.au'
EMAIL_PORT = '25'
EMAIL_HOST_USER = 'portal-admin'
EMAIL_HOST_PASSWORD = 'PASSWORD'
EMAIL_USE_TLS = False
PORTAL_URL = 'http://portal.hvpaustralia.org.au'
ADMIN_EMAIL = 'portal-admin@hvpaustralia.org.au'


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '1234567890'

# AAF secret used to decode encrypted jwt
AAF_SECRET = '1234567890'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'Portal.urls'

# Python dotted path to the WSGI application used by Django's runserver.
# Comment this out if you are running in debug
#WSGI_APPLICATION = 'Portal.wsgi.application'

# Place the directory path of where your templates are 
import os
BASE_DIR = os.path.dirname(__file__)
HOME_DIR = os.path.join(BASE_DIR, 'templates')

TEMPLATE_DIRS = (
    HOME_DIR,
    'search/indexes/hvp/'
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'taggit',
    
    'Portal.home',
    'Portal.hvp',
    'Portal.search',
    'Portal.users',
    
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

AUTHENTICATION_BACKENDS = (
    'Portal.hvp.EmailModelBackend.EmailModelBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# Sets the session cookie age in seconds
# 10 minutess should be long enough?
SESSION_COOKIE_AGE = 6000 

# Set the model that extends the existing user attributes
AUTH_PROFILE_MODULE = 'hvp.UserProfile'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'logfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': 'errors.log',
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'standard',
        },
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers':['console'],
            'propagate': True,
            'level':'WARN',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'Portal': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
        },
    }
}
