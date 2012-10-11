# Django settings for satchmo project.
# This is a recommended base setting for further customization, default for clonesatchmo.py
import os

DIRNAME = os.path.dirname(os.path.normpath(os.path.abspath(__file__)))

DJANGO_PROJECT = 'store'
DJANGO_SETTINGS_MODULE = 'store.settings'

ADMINS = (
     ('', ''),         # tuple (name, email) - important for error reports sending, if DEBUG is disabled.
)

MANAGERS = ADMINS

# Local time zone for this installation. All choices can be found here:
# http://www.postgresql.org/docs/current/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
TIME_ZONE = 'US/Pacific'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'en-us'
LANGUAGES = (
            ('en', "English"),
            ('zh', 'Chinese'),
            )
SITE_ID = 1

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
# Image files will be stored off of this path
#
# If you are using Windows, recommend using normalize_path() here
#
# from satchmo_utils.thumbnail import normalize_path
# MEDIA_ROOT = normalize_path(os.path.join(DIRNAME, 'static/'))
#MEDIA_ROOT = os.path.join(DIRNAME, 'static/')
MEDIA_ROOT = os.path.join(DIRNAME, '../../../../mediasa/media/')

MEDIA_URL="/static/media/"
STATIC_ROOT = os.path.join(DIRNAME, '../../../../mediasa/')
STATIC_URL = '/static/'


# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
#MEDIA_URL="/media/"

# STATIC_ROOT can be whatever different from other dirs
#STATIC_ROOT = os.path.join(DIRNAME, 'static-collect/')
#STATIC_URL = '/static/'

STATICFILES_DIRS = (
       # os.path.join(DIRNAME, 'static/'),
)

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/static/media/'  # remove for Django 1.4 as deprecated

# Make this unique, and don't share it with anybody.
SECRET_KEY = '21il=e#b0q-0pnr2mi($kvcrd39%bb@g6i2=@bf$bp*^pl%cl_'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.DomainRedirectMiddleware',
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.doc.XViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "threaded_multihost.middleware.ThreadLocalMiddleware",
    "satchmo_store.shop.SSLMiddleware.SSLRedirect",
    'pagination.middleware.PaginationMiddleware',
    #"satchmo_ext.recentlist.middleware.RecentProductMiddleware",
   # 'debug_toolbar.middleware.DebugToolbarMiddleware',
)

#this is used to add additional config variables to each request
# NOTE: If you enable the recent_products context_processor, you MUST have the
# 'satchmo_ext.recentlist' app installed.
TEMPLATE_CONTEXT_PROCESSORS = (
#    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
#    'django.core.context_processors.media',
#    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'social_auth.context_processors.social_auth_by_name_backends',
    'social_auth.context_processors.social_auth_backends',
    'social_auth.context_processors.social_auth_by_type_backends',
    'social_auth.context_processors.social_auth_login_redirect',
        'satchmo_store.shop.context_processors.settings',
        'django.contrib.auth.context_processors.auth',
        #'satchmo_ext.recentlist.context_processors.recent_products',
        # do not forget following. Maybe not so important currently
        # but will be
        'django.core.context_processors.media',   # MEDIA_URL
        'django.core.context_processors.static',  # STATIC_URL
)

ROOT_URLCONF = 'store.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(DIRNAME,'templates'),
)

INSTALLED_APPS = (
    'django.contrib.sites',
    'satchmo_store.shop',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.comments',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'registration',
    'sorl.thumbnail',
    'keyedcache',
    'livesettings',
    'l10n',
    'satchmo_utils.thumbnail',
    'satchmo_store.contact',
    'tax',
    'tax.modules.no',
    'tax.modules.area',
    'tax.modules.percent',
    'shipping',
    #'satchmo_store.contact.supplier',
    #'shipping.modules.tiered',
    #'satchmo_ext.newsletter',
    #'satchmo_ext.recentlist',
    #'testimonials',         # dependency on  http://www.assembla.com/spaces/django-testimonials/
    'product',
    'product.modules.configurable',
    'product.modules.custom',
    #'product.modules.downloadable',
    #'product.modules.subscription',
    #'satchmo_ext.product_feeds',
    #'satchmo_ext.brand',
    'payment',
    'payment.modules.paypal',
    #'payment.modules.purchaseorder',
    #'payment.modules.giftcertificate',
    #'satchmo_ext.wishlist',
    #'satchmo_ext.upsell',
    #'satchmo_ext.productratings',
    'satchmo_ext.satchmo_toolbar',
    'satchmo_utils',
    #'shipping.modules.tieredquantity',
    #'satchmo_ext.tieredpricing',
    #'typogrify',            # dependency on  http://code.google.com/p/typogrify/
   # 'debug_toolbar',
    'app_plugins',
    'store.localsite',
    'south',
    'social_auth',
    'pagination',
)

#AUTHENTICATION_BACKENDS = (
#    'satchmo_store.accounts.email-auth.EmailBackend',
#    'django.contrib.auth.backends.ModelBackend',
#)

#DEBUG_TOOLBAR_CONFIG = {
#    'INTERCEPT_REDIRECTS' : False,
#}

#### Satchmo unique variables ####
from django.conf.urls.defaults import patterns, include
SATCHMO_SETTINGS = {
    'SHOP_BASE' : '',
    'MULTISHOP' : False,
    'SHOP_URLS' : patterns('', (r'^i18n/', include('l10n.urls')),)
    #'SHOP_URLS' : patterns('satchmo_store.shop.views',)
}

SKIP_SOUTH_TESTS=True
L10N_SETTINGS = {
  'currency_formats' : {
     'HKD' : {'symbol': u'HK$', 'positive' : u"HK$%(val)0.2f", 'negative': u"HK$(%(val)0.2f)",
               'decimal' : '.'},
  },
  'default_currency' : 'HKD',
  'show_admin_translations': False,
  'allow_translation_choice': False,
}

#### social network account ####
AUTHENTICATION_BACKENDS = (
    'satchmo_store.accounts.email-auth.EmailBackend',
#    'django.contrib.auth.backends.ModelBackend',
#    'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.contrib.weibo.WeiboBackend',
#    'social_auth.backends.google.GoogleOAuthBackend',
#    'social_auth.backends.google.GoogleOAuth2Backend',
#    'social_auth.backends.google.GoogleBackend',
#    'social_auth.backends.yahoo.YahooBackend',
#    'social_auth.backends.browserid.BrowserIDBackend',
#    'social_auth.backends.contrib.linkedin.LinkedinBackend',
#    'social_auth.backends.contrib.livejournal.LiveJournalBackend',
#    'social_auth.backends.contrib.orkut.OrkutBackend',
#    'social_auth.backends.contrib.foursquare.FoursquareBackend',
#    'social_auth.backends.contrib.github.GithubBackend',
#    'social_auth.backends.contrib.dropbox.DropboxBackend',
#    'social_auth.backends.contrib.flickr.FlickrBackend',
#    'social_auth.backends.contrib.instagram.InstagramBackend',
#    'social_auth.backends.contrib.vkontakte.VKontakteBackend',
#    'social_auth.backends.contrib.skyrock.SkyrockBackend',
#    'social_auth.backends.contrib.yahoo.YahooOAuthBackend',
#    'social_auth.backends.OpenIDBackend',
#    'social_auth.backends.contrib.bitbucket.BitbucketBackend',
#    'social_auth.backends.contrib.mixcloud.MixcloudBackend',
#    'social_auth.backends.contrib.live.LiveBackend',
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
WEIBO_CLIENT_KEY = '1737320750'
WEIBO_CLIENT_SECRET = '7430edaf4c83d7e2fc8e04d5a43e2862'
#LOGIN_URL          = '/login-form/'
#LOGIN_REDIRECT_URL = '/logged-in/'
#LOGIN_ERROR_URL    = '/login-error/'

SOCIAL_AUTH_COMPLETE_URL_NAME  = 'socialauth_complete'
SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'

SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'

SOCIAL_AUTH_EXTRA_DATA = False

SOCIAL_AUTH_SESSION_EXPIRATION = False

EMAIL_HOST = 'smtp.webfaction.com'
EMAIL_HOST_USER = 'dhub'
EMAIL_HOST_PASSWORD = 'dhub4'
DEFAULT_FROM_EMAIL = 'info@designhub.hk'
SERVER_EMAIL = 'info@designhub.hk'
# Load the local settings
from local_settings import *

# debug_toolbar settings
if DEBUG:
    INTERNAL_IPS = ('127.0.0.1',)
    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )

    INSTALLED_APPS += (
        'debug_toolbar',
    )

    DEBUG_TOOLBAR_PANELS = (
        'debug_toolbar.panels.version.VersionDebugPanel',
        'debug_toolbar.panels.timer.TimerDebugPanel',
        'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
        'debug_toolbar.panels.headers.HeaderDebugPanel',
        #'debug_toolbar.panels.profiling.ProfilingDebugPanel',
        'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
        'debug_toolbar.panels.sql.SQLDebugPanel',
        'debug_toolbar.panels.template.TemplateDebugPanel',
        'debug_toolbar.panels.cache.CacheDebugPanel',
        'debug_toolbar.panels.signals.SignalDebugPanel',
        'debug_toolbar.panels.logger.LoggingPanel',
    )

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    }
