from .base import *     # NOQA

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'PORT': '3306',
        'NAME': 'blog',
        'USER': 'root',
        'PASSWORD': '123456',
    }
}


