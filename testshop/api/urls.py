from django.conf.urls import patterns, include, url
from djangorestframework.views import ListOrCreateModelView,InstanceModelView
from testshop.api.resources import CommentResource

from djangorestframework.permissions import IsUserOrIsAnonReadOnly

from testshop.api.handlers import AutoOwnerPaginatorListOrCreateModelView,ReadOnlyInstanceModelView

urlpatterns = patterns('',
    url(r'^comment/$', AutoOwnerPaginatorListOrCreateModelView.as_view(resource=CommentResource, permissions = ( IsUserOrIsAnonReadOnly, ) )),
    #comment detail handling
    url(r'^comment/(?P<pk>[\d]+)/$', ReadOnlyInstanceModelView.as_view(resource=CommentResource, permissions = ( IsUserOrIsAnonReadOnly, ) )),    
    url(r'^comment/product/(?P<product__id>[\d]+)/$', AutoOwnerPaginatorListOrCreateModelView.as_view(resource=CommentResource, permissions = ( IsUserOrIsAnonReadOnly, ) )),    
)
