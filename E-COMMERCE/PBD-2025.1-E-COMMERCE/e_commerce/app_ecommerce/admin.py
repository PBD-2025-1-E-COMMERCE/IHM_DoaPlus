from django.contrib import admin

# Register your models here.
from app_ecommerce.models import Category, ItemDetails, Company, Item, Image, Color, Size, Storage



class ItemDetailsInlinte(admin.TabularInline):
    model = ItemDetails

class ImageInline(admin.TabularInline):
    model = Image


class ItemAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline,
        ItemDetailsInlinte
    ]
    
admin.site.register(Item, ItemAdmin)
admin.site.register(Company)
admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Storage)

