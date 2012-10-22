from django.contrib import admin
from models import MyNewProduct
from models import Designer
from models import DesignerImage
from models import Brand
from models import InviteReward
from satchmo_utils.thumbnail.field import ImageWithThumbnailField
from satchmo_utils.thumbnail.widgets import AdminImageWithThumbnailWidget
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
class DesignerImage_Inline(admin.StackedInline):
    model = DesignerImage
    extra = 3
    
    formfield_overrides = {
        ImageWithThumbnailField : {'widget' : AdminImageWithThumbnailWidget},
    }

class MyNewProductOptions(admin.ModelAdmin):
    actions = ('make_featured', 'make_unfeatured')
    
    def make_featured(self, request, queryset):
        rows_updated = queryset.update(featured=True)
        if rows_updated == 1:
            message_bit = _("1 product was")
        else:
            message_bit = _("%s products were" % rows_updated)
        self.message_user(request, _("%s successfully marked as featured") % message_bit)
        return HttpResponseRedirect('')
    make_featured.short_description = _("Mark selected products as featured")

    def make_unfeatured(self, request, queryset):
        rows_updated = queryset.update(featured=False)
        if rows_updated == 1:
            message_bit = _("1 product was")
        else:
            message_bit = _("%s products were" % rows_updated)
        self.message_user(request, _("%s successfully marked as not featured") % message_bit)
        return HttpResponseRedirect('')
    make_unfeatured.short_description = _("Mark selected products as not featured")
    
class DesignerOptions(admin.ModelAdmin):
    inlines = [DesignerImage_Inline]
    list_display = ()
    actions = ('make_active', 'make_inactive','make_featured', 'make_unfeatured')

    def make_active(self, request, queryset):
        rows_updated = queryset.update(active=True)
        if rows_updated == 1:
            message_bit = _("1 product was")
        else:
            message_bit = _("%s products were" % rows_updated)
        self.message_user(request, _("%s successfully marked as active") % message_bit)
        return HttpResponseRedirect('')
    make_active.short_description = _("Mark selected products as active")

    def make_inactive(self, request, queryset):
        rows_updated = queryset.update(active=False)
        if rows_updated == 1:
            message_bit = _("1 product was")
        else:
            message_bit = _("%s products were" % rows_updated)
        self.message_user(request, _("%s successfully marked as inactive") % message_bit)
        return HttpResponseRedirect('')
    make_inactive.short_description = _("Mark selected products as inactive")

    
    def make_featured(self, request, queryset):
        rows_updated = queryset.update(featured=True)
        if rows_updated == 1:
            message_bit = _("1 product was")
        else:
            message_bit = _("%s products were" % rows_updated)
        self.message_user(request, _("%s successfully marked as featured") % message_bit)
        return HttpResponseRedirect('')
    make_featured.short_description = _("Mark selected products as featured")

    def make_unfeatured(self, request, queryset):
        rows_updated = queryset.update(featured=False)
        if rows_updated == 1:
            message_bit = _("1 product was")
        else:
            message_bit = _("%s products were" % rows_updated)
        self.message_user(request, _("%s successfully marked as not featured") % message_bit)
        return HttpResponseRedirect('')
    make_unfeatured.short_description = _("Mark selected products as not featured")

    list_display += ('slug', 'name','featured','active',)
admin.site.register(MyNewProduct,MyNewProductOptions)
admin.site.register(Designer,DesignerOptions)

class BaseBrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('name',) 
    }

class BrandAdmin(BaseBrandAdmin):
    pass


admin.site.register(Brand,BrandAdmin)
admin.site.register(InviteReward)