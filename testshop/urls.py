from django.conf.urls import patterns, include, url
from django.conf import settings
from testshop.shop.views import ProductListViewHome, DesignerListView,DesignerDetailView
from testshop.shop.models import Product, Designer,DesignerCreateForm,StaticSitemap

from testshop.utils.views import DesignerCreateView,DesignerUpdateView,DesignerDeleteView, ProductUpdateView
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib import admin
from django.core.urlresolvers import reverse

from testshop.shop.views import home, done, logout, error, form, form2
from testshop.shop.facebook import facebook_view


from testshop.shop.models import Product


admin.autodiscover()

urlpatterns = patterns('testshop.shop.views',
    url(r'^admin/', include(admin.site.urls)),
    url(r"^$", ProductListViewHome.as_view(), 
            name='plugshop-product-list-home'),
    url(r"^how-dhub-works/$", 'howDhubWorks',name="how-dhub-works"),
    url(r"^designers/$", DesignerListView.as_view(), 
            name='plugshop-designer-list'),
    url(r"^designers/(?P<slug>[\-\/\w]+)/$", DesignerDetailView.as_view(),name="designer-detail"),
    url(r'^api/', include('testshop.api.urls')),
)
sitemaps={}
sitemaps['static'] = StaticSitemap(settings.PROJECT_ROOT +'/sitemap1.txt')
urlpatterns += patterns('',
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
)                   
urlpatterns += patterns('',
    url(r'^social/$', home, name='home'),
    url(r'^social/done/$', done, name='done'),
    url(r'^social/error/$', error, name='error'),
    url(r'^social/logout/$', logout, name='logout'),
    url(r'^social/form/$', form, name='form'),
    url(r'^social/form2/$', form2, name='form2'),
    url(r'^social/fb/', facebook_view, name='fb_app'),
    url(r'', include('social_auth.urls')),
)



urlpatterns += patterns('',
    url(r'^paypal/$','testshop.shop.views.paypal'),
)
urlpatterns += patterns('',
   url(r'^paypal/pdt/', 'testshop.shop.views.pdt',name="paypal-pdt"),
#    (r'^paypal/pdt/', include('paypal.standard.pdt.urls')),
)

urlpatterns += patterns('',
    url(r'^ipn-location/', include('paypal.standard.ipn.urls')),
)
urlpatterns += patterns('',
    url(r'^ipn-return/', 'testshop.shop.views.ipnreturn',name='paypal-ipn-myreturn'),
    url(r'^ipn-cancel/', 'testshop.shop.views.ipncancel',name='paypal-mycancel'),
)

urlpatterns += patterns('',
    url(r'^contact-info/','testshop.shop.views.collectContactInfo'),
)

urlpatterns += patterns('',
    url(r'^accounts/',include('testshop.registration.urls')),
    url(r'^accounts/profile','testshop.shop.views.profile'),
)
urlpatterns += patterns('',
    url(r'^admin-designer/add/', permission_required('shop.add_designer')(DesignerCreateView.as_view(
                   )), name='fireflie-create-designer-form'),
    url(r'^admin-designer/update/(?P<slug>[\-\/\w]+)/$', permission_required('shop.change_designer')(DesignerUpdateView.as_view(
                   model=Designer,
                   )), name='fireflie-update-designer-form'),
    url(r'^admin-designer/delete/(?P<slug>[\-\/\w]+)/$', permission_required('shop.delete_designer')(DesignerDeleteView.as_view(
                   )), name='fireflie-delete-designer-form'),
)
urlpatterns += patterns('',\
    url(r"^admin-product/update/(?P<category_path>[\-\/\w]+)/(?P<slug>[\-\/\w]+)$", 
        permission_required('shop.change_product')(ProductUpdateView.as_view(
                   model=Product,
                   )), name='update-product-form'),
)

urlpatterns += patterns('',
    url(r'^shop/', include('testshop.shop.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
