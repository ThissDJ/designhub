# -*- coding: UTF-8 -*-
import os
import sys

PROJECT_ROOT = os.path.dirname(__file__)
PROJECT_PATH = os.path.abspath(PROJECT_ROOT)

sys.path.insert(0, os.path.join(PROJECT_ROOT, "../../"))

DEBUG = False
TEMPLATE_DEBUG = DEBUG
PAYPAL_DEBUG = True
ADMINS = (
    #('Your Name', 'your_email@example.com'),
)
INTERNAL_IPS = ('192.168.0.105',)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, '../shop.sqlite'),
    }
}

TIME_ZONE = 'Asia/Shanghai'
LANGUAGE_CODE = 'zh-cn'

LANGUAGES = (
    ('zh-cn', u'简体中文'), # instead of 'zh-CN'
    ('zh-tw', u'繁體中文'), # instead of 'zh-TW'
)

SITE_ID = 2
SITE_NAME = 'http://www.designhub.hk'

PAYPAL_RECEIVER_EMAIL = "design_1345392724_biz@gmail.com"

#PAYPAL_RECEIVER_EMAIL = "klijun_1343311282_biz@gmail.com" 
#PAYPAL_RECEIVER_EMAIL = "style.lcw@gmail.com"
#live PAYPAL_IDENTITY_TOKEN = "sSxVfArR_5WStaZ-v7TJ5HX4prmd1a6U3tDjgKOnqFeXNUPD5VX2TymqS0W"
#live ljj PAYPAL_IDENTITY_TOKEN = "oIDJR8MmSAoG9T6nWY4O5VEEHMfFZgAY34qN9Lw2L-q57roG5zLtYoxEeOa"
PAYPAL_IDENTITY_TOKEN = "4y_VYJUytP0Sc510ZIAifEDh9B2To1cMHsA7sM9OIGSKlkvPjW1gp1g4cU0"
EMAIL_HOST = 'smtp.webfaction.com'
EMAIL_HOST_USER = 'dhub'
EMAIL_HOST_PASSWORD = 'dhub4'
DEFAULT_FROM_EMAIL = 'info@designhub.hk'
SERVER_EMAIL = 'info@designhub.hk'


USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = '/home/thissdj/webapps/mediadh/' #os.path.join(PROJECT_ROOT, "../../mediadh/")
MEDIA_URL = '/media/'
UPLOAD_URI = 'upload/'
FILE_UPLOAD_PERMISSIONS = 0644
STATIC_ROOT = ''
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, "static/"),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = '-!q3u(5##(3ap@%h*g$koz963$__o6%0px_f!9bu_s3hk*4dmy'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.DomainRedirectMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    
    'plugshop.middleware.CartMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'testshop.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'testshop.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, "templates/"),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'social_auth.context_processors.social_auth_by_name_backends',
    'social_auth.context_processors.social_auth_backends',
    'social_auth.context_processors.social_auth_by_type_backends',
    'social_auth.context_processors.social_auth_login_redirect',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',    
    'django.contrib.admin',
    'south',
    'mptt',
    'django_thumbs',
    'debug_toolbar',
    'plugshop',
    'testshop.utils',
    'testshop.registration',    
    'testshop.shop',
    'paypal.standard.pdt',
    'paypal.standard.ipn',
    'testshop.api',
    'djangorestframework',
    'social_auth',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TOOLBAR_CALLBACK': lambda r: DEBUG,
}

PLUGSHOP_MODELS = {
    'PRODUCT': 'testshop.shop.models.Product',
    'CATEGORY': 'testshop.shop.models.Category',
    'ORDER': 'plugshop.models.order.Order',
    'ORDER_PRODUCTS': 'testshop.shop.models.OrderProductsSize',
#    'ORDER_PRODUCTS': 'plugshop.models.order_products.OrderProducts',
}
from django.utils.translation import ugettext as _
PLUGSHOP_CONFIG = {
    'REQUEST_NAMESPACE': 'cart',
    'SESSION_NAMESPACE': 'cart',
    'STATUS_CHOICES': (
        (1, _('Created')),
        (2, _('Confirmed')),
        (3, _('Denied')),
        (4, _('Delivered')),
    ),
}
AUTHENTICATION_BACKENDS = (
    'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleOAuthBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
    'social_auth.backends.google.GoogleBackend',
    'social_auth.backends.yahoo.YahooBackend',
    'social_auth.backends.browserid.BrowserIDBackend',
    'social_auth.backends.contrib.linkedin.LinkedinBackend',
    'social_auth.backends.contrib.livejournal.LiveJournalBackend',
    'social_auth.backends.contrib.orkut.OrkutBackend',
    'social_auth.backends.contrib.foursquare.FoursquareBackend',
    'social_auth.backends.contrib.github.GithubBackend',
    'social_auth.backends.contrib.dropbox.DropboxBackend',
    'social_auth.backends.contrib.flickr.FlickrBackend',
    'social_auth.backends.contrib.instagram.InstagramBackend',
    'social_auth.backends.contrib.vkontakte.VKontakteBackend',
    'social_auth.backends.contrib.skyrock.SkyrockBackend',
    'social_auth.backends.contrib.yahoo.YahooOAuthBackend',
    'social_auth.backends.OpenIDBackend',
    'social_auth.backends.contrib.bitbucket.BitbucketBackend',
    'social_auth.backends.contrib.mixcloud.MixcloudBackend',
    'social_auth.backends.contrib.live.LiveBackend',
    'django.contrib.auth.backends.ModelBackend',
)

TWITTER_CONSUMER_KEY         = ''
TWITTER_CONSUMER_SECRET      = ''
FACEBOOK_APP_ID              = '330400780383211'
FACEBOOK_API_SECRET          = '5424fbed650b11a814df2e068ca31d30'
LINKEDIN_CONSUMER_KEY        = ''
LINKEDIN_CONSUMER_SECRET     = ''
ORKUT_CONSUMER_KEY           = ''
ORKUT_CONSUMER_SECRET        = ''
GOOGLE_CONSUMER_KEY          = ''
GOOGLE_CONSUMER_SECRET       = ''
GOOGLE_OAUTH2_CLIENT_ID      = ''
GOOGLE_OAUTH2_CLIENT_SECRET  = ''
FOURSQUARE_CONSUMER_KEY      = ''
FOURSQUARE_CONSUMER_SECRET   = ''
GITHUB_APP_ID                = ''
GITHUB_API_SECRET            = ''
DROPBOX_APP_ID               = ''
DROPBOX_API_SECRET           = ''
FLICKR_APP_ID                = ''
FLICKR_API_SECRET            = ''
INSTAGRAM_CLIENT_ID          = ''
INSTAGRAM_CLIENT_SECRET      = ''
VK_APP_ID                    = ''
VK_API_SECRET                = ''
BITBUCKET_CONSUMER_KEY       = ''
BITBUCKET_CONSUMER_SECRET    = ''
LIVE_CLIENT_ID               = ''
LIVE_CLIENT_SECRET           = ''
SKYROCK_CONSUMER_KEY         = ''
SKYROCK_CONSUMER_SECRET      = ''
YAHOO_CONSUMER_KEY           = ''
YAHOO_CONSUMER_SECRET        = ''
MIXCLOUD_CLIENT_ID           = ''
MIXCLOUD_CLIENT_SECRET       = ''

#LOGIN_URL          = '/login-form/'
#LOGIN_REDIRECT_URL = '/logged-in/'
#LOGIN_ERROR_URL    = '/login-error/'

SOCIAL_AUTH_COMPLETE_URL_NAME  = 'socialauth_complete'
SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'

SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'

SOCIAL_AUTH_EXTRA_DATA = False

SOCIAL_AUTH_SESSION_EXPIRATION = False
