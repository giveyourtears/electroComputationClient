from askue_rs.settings.default import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*=&i(!$i@wfg)w#*xw-9fx!cvebt*h10g*+l=i^rea%qfp5#x)'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
default = 'postgres+psycopg2://developer:developer@localhost:5432/askue_rs_test'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'askue_rs',
        'USER' : 'XXXXXXXXX',
        'PASSWORD' : 'XXXXXXXXX',
        'HOST' : 'XXXXXXXXX',
        'PORT' : '5432',
        'DEFAULT_TABLESPACE': 'askue_rs_ts'
    },
    'dn_emax': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dn_emax',
        'USER' : 'XXXXXXXXX',
        'PASSWORD' : 'XXXXXXXXX',
        'HOST' : 'XXXXXXXXX',
        'PORT' : '5432',
        'DEFAULT_TABLESPACE': 'dn_emax_ts'
    },
    'dn_emax_data': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dn_emax_data',
        'USER' : 'XXXXXXXXX',
        'PASSWORD' : 'XXXXXXXXX',
        'HOST' : 'XXXXXXXXX',
        'PORT' : '5432',
        'DEFAULT_TABLESPACE': 'dn_emax_data_ts'
    }
}
