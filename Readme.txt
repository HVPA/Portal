Prerequisite:
- Python 2.4+
- Django 1.4+*
- django-taggit
- jwt
- MySQL 
- Apache 2
- WSGI
*Django versions higher than 1.6 may not work correctly since there was significant changes Django and
portal was not optimised to run on anything above 1.4

What is the Portal Django app?
This web app powers the HVPA portal website that manages users and user access to variant clinical data 
and provides variant data search and discovery capabilities.

Dev Setup:
Run tox to setup the python virtualenv with all the python module dependencies.
 - Configure the "settings.py" with the database details.
 - Then run "manage.py syncdb" to create the DB and tables.
 - Run "manage.py runserver" to run in debug mode.

Prod Deployment Setup:
The portal has been extensively tested on linux based environments but should work on Windows.
Make sure you have Apache2, WSGI and MySQL setup properly and run tox to setup the python virtualenv with all the
python module dependencies.

Please see Django documentation for deploying the django app at https://docs.djangoproject.com/en/dev/howto/deployment/
