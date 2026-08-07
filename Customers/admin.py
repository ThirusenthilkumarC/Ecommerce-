from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'price',
        'description',
        'image',
        'status'
    )

    search_fields = ('name',)
    list_filter = ('status',)