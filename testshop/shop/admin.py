from django.contrib import admin

from testshop.shop.models import *

from plugshop.admin import BaseProductAdmin, BaseCategoryAdmin

class CategoryAdmin(BaseCategoryAdmin):
    pass

class ProductAdmin(BaseProductAdmin):
    pass

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)

admin.site.register(ProductImage)

class BaseDesignerAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('name',) 
    }

class DesignerAdmin(BaseDesignerAdmin):
    pass

admin.site.register(Designer,DesignerAdmin)

admin.site.register(ContactInfo)
admin.site.register(Storage)
admin.site.register(Comment)