from .base import *
# SECRET_KEY = 'django-insecure-_v+4-9_m1mu0b1$a^(bsophfy1galhvu@=y^qq9n*q(solf%ow'
SECRET_KEY = config('SECRET_KEY')
DEBUG = True
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
