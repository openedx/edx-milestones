"""
These settings are here to use during tests, because django requires them.

In a real-world use case, apps in this project are installed into other
Django applications, so these settings will not be used.
"""
from __future__ import unicode_literals
DEBUG = True
TEST_MODE = True
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
TRANSACTIONS_MANAGED = {}
USE_TZ = False
TIME_ZONE = {}
SECRET_KEY = 'SHHHHHH'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'milestones.db'
    },
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',

    'milestones',
    'django_nose',
)

MIDDLEWARE_CLASSES = {}
