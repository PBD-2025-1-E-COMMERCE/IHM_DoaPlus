from django.contrib import admin

# Register your models here.
from app_ecommerce.models import Category, ItemDetails, Company, Item, Image, Color, Size, Storage, Ongs, Causa

class ItemDetailsInlinte(admin.TabularInline):
    model = ItemDetails

class ImageInline(admin.TabularInline):
    model = Image

class CausaAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline
    ]
    
admin.site.register(Causa, CausaAdmin)
admin.site.register(Company)
admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Storage)
admin.site.register(Ongs)


