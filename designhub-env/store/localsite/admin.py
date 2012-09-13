from django.contrib import admin
from models import MyNewProduct
from models import Designer
from models import DesignerImage
from models import Brand
from satchmo_utils.thumbnail.field import ImageWithThumbnailField
from satchmo_utils.thumbnail.widgets import AdminImageWithThumbnailWidget
class DesignerImage_Inline(admin.StackedInline):
    model = DesignerImage
    extra = 3
    
    formfield_overrides = {
        ImageWithThumbnailField : {'widget' : AdminImageWithThumbnailWidget},
    }


class DesignerOptions(admin.ModelAdmin):
    inlines = [DesignerImage_Inline]

admin.site.register(MyNewProduct)
admin.site.register(Designer,DesignerOptions)

class BaseBrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('name',) 
    }

class BrandAdmin(BaseBrandAdmin):
    pass


admin.site.register(Brand,BrandAdmin)