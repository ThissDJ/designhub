# encoding: utf-8
from django.conf.urls import patterns, url
from django.utils.translation import ugettext as _

from plugshop import settings
from plugshop.views import *
from plugshop.exceptions import NoUrlFound
from testshop.shop.modviews import *

PREFIX = settings.URL_PREFIX

urlpatterns = patterns('plugshop.views',
    url(r"^$", ProductListViewV1.as_view(), 
            name='plugshop-product-list'),
    url(r"^cart/$", CartViewV1.as_view(), 
            name="plugshop-cart"),
    url(r"^order/$", OrderView.as_view(), 
            name="plugshop-order"),
    url(r"^(?P<category_path>[\-\/\w]+)/$", CategoryViewV1.as_view(), 
            name='plugshop-category'),
    url(r"^(?P<category_path>[\-\/\w]+)/(?P<slug>[\-\/\w]+)$", 
            ProductViewV1.as_view(), 
            name='plugshop-product'),
)

def get_url(name):
    patterns = filter(lambda x: x.name == name, urlpatterns)
    try:
        pattern = patterns[0]
    except IndexError:
        raise NoUrlFound(_("No url with name '%s'" % name))

    return pattern._regex
        