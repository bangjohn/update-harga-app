from django.contrib import admin
from .models import Category, Product, PriceHistory


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'current_price', 'previous_price', 'updated_at')
    list_filter = ('category',)
    search_fields = ('name',)
    readonly_fields = ('previous_price',)
    fields = ('name', 'category', 'image_url', 'current_price', 'previous_price')


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(PriceHistory)
