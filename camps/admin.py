from django.contrib import admin
from .models import Camp, CampRegistration

@admin.register(Camp)
class CampAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'capacity', 'available_slots')
    list_filter = ('date',)
    search_fields = ('title', 'location', 'description')
    date_hierarchy = 'date'

@admin.register(CampRegistration)
class CampRegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'camp', 'registered_at')
    list_filter = ('camp', 'registered_at')
    search_fields = ('user__username', 'camp__title')
    date_hierarchy = 'registered_at'
