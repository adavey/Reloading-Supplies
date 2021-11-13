from crawl_sites.models import Manufacturer, Website, Product, Website_Product
from django.contrib import admin

class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display=('manufacturer_name', 'name', 'size')

    def manufacturer_name (self, instance):
        return instance.manufacturer.name

class Website_ProductAdmin(admin.ModelAdmin):
    model = Website_Product
    list_display=('website_name','product_name', 'url')

    def website_name (self, instance):
        return instance.website.name

    def product_name (self, instance):
        return instance.product.name        

# Register your models here.
admin.site.register(Manufacturer)
admin.site.register(Website)
admin.site.register(Product, ProductAdmin)
admin.site.register(Website_Product, Website_ProductAdmin)