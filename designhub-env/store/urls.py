from django.conf.urls.defaults import *

from satchmo_store.urls import urlpatterns

from localsite.views import home, done, logout, error, form, form2
from localsite.facebook import facebook_view

#designers
from localsite.views import DesignerListView,DesignerDetailView

urlpatterns += patterns('',
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r"^talents/$", DesignerListView.as_view(), 
            name='designer-list'),
    url(r"^talents/(?P<slug>[\-\/\w]+)/$", DesignerDetailView.as_view(),name="designer-detail"),                 
    url(r'^social/$', home, name='home'),
    url(r'^social/done/$', done, name='done'),
    url(r'^social/error/$', error, name='error'),
    url(r'^social/logout/$', logout, name='logout'),
    url(r'^social/form/$', form, name='form'),
    url(r'^social/form2/$', form2, name='form2'),
    url(r'^social/fb/', facebook_view, name='fb_app'),
    url(r'', include('social_auth.urls')),
)