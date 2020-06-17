from askue_rs.settings.default import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SECRET_KEY = '5#2=5(j#2ei!5qlms6&&nxh&*8nsr+$k%hgz!bx0f)d2mrqd^i'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
default = 'postgres+psycopg2://developer:developer@localhost:5432/askue_rs_test'

# for orm
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'askue_rs_test',
        'USER' : 'developer',
        'PASSWORD' : 'developer',
        'HOST' : 'localhost',
        'PORT' : '5432',
        'DEFAULT_TABLESPACE': 'pg_default'
    },
    'dn_emax': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dn_emax',
        'USER' : 'developer',
        'PASSWORD' : 'developer',
        'HOST' : 'localhost',
        'PORT' : '5432',
        'DEFAULT_TABLESPACE': 'pg_default'
    },
    'dn_emax_data': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dn_emax_data',
        'USER' : 'developer',
        'PASSWORD' : 'developer',
        'HOST' : 'localhost',
        'PORT' : '5432',
        'DEFAULT_TABLESPACE': 'pg_default'
    }
}