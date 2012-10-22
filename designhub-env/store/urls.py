from django.conf.urls.defaults import *

from satchmo_store.urls import urlpatterns

from localsite.views import home, done, logout, error, form, form2
from localsite.facebook import facebook_view

#designers
from localsite.views import DesignerListView, DesignerDetailView, DesignerAjaxListView

from local_settings import LOCAL_DEV
if LOCAL_DEV:
    urlpatterns += patterns('',
        url(r'^comments/', include('django.contrib.comments.urls')),
        url(r"^talents/$", DesignerListView.as_view(), 
                name='designer-list'),
        url(r"^talents/ajax/$", DesignerAjaxListView.as_view(),
                name='designer-list-ajax'),
        url(r'^fbtab/$','localsite.views.fabtabFeaturedToday'),
        url(r'^launching/$','localsite.views.launching'),
        url(r"^talents/(?P<slug>[\-\/\w]+)/$", DesignerDetailView.as_view(), name="designer-detail"),     
        url(r"^sale/$", 'localsite.views.saleindex', name='sale-index'), 
        url(r"^invite/$", 'localsite.views.invite', name='invite'),          
        url(r'^social/$', home, name='home'),
        url(r'^social/done/$', done, name='done'),
        url(r'^social/error/$', error, name='error'),
        url(r'^social/logout/$', logout, name='logout'),
        url(r'^social/form/$', form, name='form'),
        url(r'^social/form2/$', form2, name='form2'),
        url(r'^social/fb/', facebook_view, name='fb_app'),
        url(r'^accounts/create-email-password/', 'localsite.views.createEmailPassword', name='create-email-password'),
        url(r'', include('social_auth.urls')),
    )
else:
    urlpatterns += patterns('',
        url(r'^comments/', include('django.contrib.comments.urls')),
        url(r"^talents/$", DesignerListView.as_view(),{'SSL': True}, 
                name='designer-list'),
        url(r"^talents/ajax/$", DesignerAjaxListView.as_view(),{'SSL': True}, 
                name='designer-list-ajax'),
        url(r'^fbtab/$','localsite.views.fabtabFeaturedToday',{'SSL': True}),
        url(r'^launching/$','localsite.views.launching',{'SSL': True}),
        url(r"^talents/(?P<slug>[\-\/\w]+)/$", DesignerDetailView.as_view(),{'SSL': True}, name="designer-detail"),     
        url(r"^sale/$", 'localsite.views.saleindex',{'SSL': True}, name='sale-index'),
        url(r"^invite/$", 'localsite.views.invite',{'SSL': True}, name='invite'),            
        url(r'^social/$', home,{'SSL': True}, name='home'),
        url(r'^social/done/$', done,{'SSL': True}, name='done'),
        url(r'^social/error/$', error,{'SSL': True}, name='error'),
        url(r'^social/logout/$', logout,{'SSL': True}, name='logout'),
        url(r'^social/form/$', form,{'SSL': True}, name='form'),
        url(r'^social/form2/$', form2,{'SSL': True}, name='form2'),
        url(r'^social/fb/', facebook_view,{'SSL': True}, name='fb_app'),
        
        url(r'^accounts/create-email-password/', 'localsite.views.createEmailPassword',{'SSL': True}, name='create-email-password'),
        url(r'', include('social_auth.urls')),
    )
