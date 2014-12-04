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

# local_settings.py
# An un-svn'ed file which stores local (site/developer) settings which change frequently
# This allows multiple developers to work on the code without svn commits causing conflicts
# If local_settings.py does not exists, it simple uses a default
# Only applies to settings within a use_local_settings if block
use_local_settings = True
try:
    import local_settings
    use_local_settings = True
except:
    use_local_settings = False

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('HVP Admin', 'portal-admin@hvpaustralia.org.au'),
)

MANAGERS = ADMINS

if use_local_settings == True:
    # Database Settings
    DATABASES = {
        # EXAMPLE DB settings, 'a la copy pasta'
        #'example': {
        #    'ENGINE': '',    # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        #    'NAME': '',      # Or path to database file if using sqlite3.
        #    'USER': '',      # Not used with sqlite3.
        #    'PASSWORD': '',  # Not used with sqlite3.
        #    'HOST': '',      # Set to empty string for localhost. Not used with sqlite3.
        #    'PORT': '',      # Set to empty string for default. Not used with sqlite3.
        #}
        
        # DEFAULT HVP portal DB settings
        'default': {
            'ENGINE': local_settings.DATABASE_ENGINE_PORTAL, 
            'NAME': local_settings.DATABASE_NAME_PORTAL,     
            'USER': local_settings.DATABASE_USER_PORTAL,     
            'PASSWORD': local_settings.DATABASE_PASSWORD_PORTAL, 
            'HOST': local_settings.DATABASE_HOST_PORTAL, 
            'PORT': local_settings.DATABASE_PORT_PORTAL 
        },

        # JOOMLA HVP Node DB settings
        'joomla': {
                'ENGINE': local_settings.DATABASE_ENGINE_SITE,
                'NAME': local_settings.DATABASE_NAME_SITE,
                'USER': local_settings.DATABASE_USER_SITE,
                'PASSWORD': local_settings.DATABASE_PASSWORD_SITE,
                'HOST': local_settings.DATABASE_HOST_SITE,
                'PORT': local_settings.DATABASE_PORT_SITE
        },
        
        # LABS DB settings
        'labs': {
                'ENGINE': local_settings.DATABASE_ENGINE_LABS,
                'NAME': local_settings.DATABASE_NAME_LABS,
                'USER': local_settings.DATABASE_USER_LABS,
                'PASSWORD': local_settings.DATABASE_PASSWORD_LABS,
                'HOST': local_settings.DATABASE_HOST_LABS,
                'PORT': local_settings.DATABASE_PORT_LABS
        }
    }

    # EMAIL server settings
    EMAIL_HOST = local_settings.EMAIL_HOST
    EMAIL_PORT = local_settings.EMAIL_PORT
    EMAIL_HOST_USER = local_settings.EMAIL_HOST_USER
    EMAIL_HOST_PASSWORD = local_settings.EMAIL_HOST_PASSWORD
    EMAIL_USE_TLS = local_settings.EMAIL_USE_TLS
    PORTAL_URL = local_settings.PORTAL_URL
    ADMIN_EMAIL = local_settings.ADMIN_EMAIL

else:
    # Database Settings
    DATABASES = {        
        # DEFAULT HVP portal DB settings
        'default': {
            'ENGINE': 'django.db.backends.mysql', 
            'NAME': 'HVP',     
            'USER': '',     
            'PASSWORD': '', 
            'HOST': '', 
            'PORT': ''
        },

        # JOOMLA HVP Node DB settings
        'joomla': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': '',
                'USER': '',
                'PASSWORD': '',
                'HOST': '',
                'PORT': ''
        },
        
        # LABS DB settings
        'labs': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'Labs',
                'USER': '',
                'PASSWORD': '',
                'HOST': '',
                'PORT': ''
        }
    }

    # EMAIL server settings
    EMAIL_HOST = 'mail.hvpaustralia.org.au'
    EMAIL_PORT = '25'
    EMAIL_HOST_USER = 'portal-admin'
    EMAIL_HOST_PASSWORD = '&EWaGA9rev-4'
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
    'pagination.middleware.PaginationMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'Portal.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'Portal.wsgi.application'

# Place the directory path of where your templates are 
if use_local_settings == True:
    HOME_DIR = local_settings.HOME_DIR
else:
    HOME_DIR = ''

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
    #'pagination',
    
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

# Set the server for solr
if use_local_settings == True:
    SOLR_SERVER = local_settings.SOLR_SERVER
else:
    SOLR_SERVER = ''


# The base url for the site
if use_local_settings == True:
    BASE_URL = local_settings.BASE_URL
else:
    BASE_URL = ''

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
