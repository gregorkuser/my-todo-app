from .base import *
# SECRET_KEY = 'django-insecure-_v+4-9_m1mu0b1$a^(bsophfy1galhvu@=y^qq9n*q(solf%ow'
SECRET_KEY = config('SECRET_KEY')
DEBUG = False
DEBUG = False
ALLOWED_HOSTS = ['your-heroku-app.herokuapp.com']
import dj_database_url
DATABASES = {
    'default': dj_database_url.config(default=config('DATABASE_URL'))
}
