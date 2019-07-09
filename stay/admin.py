from django.contrib import admin

from .models import *

# Register your models here.
class ImageInline(admin.TabularInline):
    model = Image

class StayOption(admin.ModelAdmin):
    list_display = ['name', 'location','username']
    inlines = [ImageInline]
    ordering = ['location']


class ImageOption(admin.ModelAdmin):
    list_display = ['stay', 'image']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['staying']


admin.site.register(Stay, StayOption)
admin.site.register(Image, ImageOption)
admin.site.register(Category)
