from django.contrib import admin
from .models import Skill, Profile, Listing, Booking, Review

# Register your models here.

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ('name', 'category')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username', 'bio')

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'price', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'teacher__username')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('student', 'listing', 'date', 'status')
    list_filter = ('status', 'date')
    search_fields = ('student__username', 'listing__title')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('booking', 'rating')
    list_filter = ('rating',)
