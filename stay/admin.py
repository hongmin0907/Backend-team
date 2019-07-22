from django.contrib import admin

from .models import *

# Register your models here.
class CategoryOption(admin.ModelAdmin):
    list_display = ['staying']

class ImageInline(admin.TabularInline):
    model = Image

class CommentInline(admin.TabularInline):
    model = Comment

class StayOption(admin.ModelAdmin):
    list_display = ['name', 'location','username']
    ordering = ['location']
    inlines = [ImageInline]
    inlines = [CommentInline]


class RoomOption(admin.ModelAdmin):
    list_display = ['stay', 'name']

class CommentOption(admin.ModelAdmin):
    list_display = ['username', 'text']

class ImageOption(admin.ModelAdmin):
    list_display = ['stay', 'room','image']

class ReservationOption(admin.ModelAdmin):
    list_display = ['username', 'stay', 'room', 'checkIn', 'checkOut', 'booker', 'phoneNumber']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['staying']

admin.site.register(Category, CategoryOption)
admin.site.register(Stay, StayOption)
admin.site.register(Image, ImageOption)
admin.site.register(Room, RoomOption)
admin.site.register(Reservation, ReservationOption)
