from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, StudentProfile, Room

# Register your models here.


class CustomUserAdmin(UserAdmin):
    """Admin configuration for CustomUser model"""

    # Add user_type and phone to the user list display
    list_display = UserAdmin.list_display + ('user_type', 'phone')

    # Add user_type and phone to the user edit form
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'phone')}),
    )

    # Add user_type and phone to the user creation form
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'phone')}),
    )


class StudentProfileAdmin(admin.ModelAdmin):
    """Admin configuration for StudentProfile model"""

    list_display = ('student_id', 'user', 'department',
                    'faculty', 'academic_year', 'is_allocated')
    list_filter = ('department', 'faculty', 'academic_year', 'is_allocated')
    search_fields = ('student_id', 'user__username',
                     'user__first_name', 'user__last_name')

    # Make the admin form more organized
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Academic Information', {
            'fields': ('student_id', 'department', 'faculty', 'academic_level', 'academic_year', 'semester', 'date_of_enrollment')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact', 'emergency_contact_name')
        }),
        ('Hostel Status', {
            'fields': ('is_allocated',)
        }),
    )


class RoomAdmin(admin.ModelAdmin):
    """Admin configuration for Room model"""

    list_display = ('room_number', 'block', 'floor', 'room_type',
                    'capacity', 'current_occupancy', 'available_beds', 'is_available')
    list_filter = ('block', 'floor', 'room_type', 'is_available',
                   'has_attached_bathroom', 'has_ac')
    search_fields = ('room_number', 'block')

    # Organize the admin form
    fieldsets = (
        ('Room Information', {
            'fields': ('room_number', 'block', 'floor', 'room_type')
        }),
        ('Capacity', {
            'fields': ('capacity', 'current_occupancy', 'is_available')
        }),
        ('Facilities', {
            'fields': ('has_attached_bathroom', 'has_ac')
        }),
    )

    # Add some helpful features
    list_per_page = 20

    # Custom actions
    actions = ['make_available', 'make_unavailable']

    def make_available(self, request, queryset):
        """Action to mark rooms as available"""
        queryset.update(is_available=True)
        self.message_user(
            request, f"{queryset.count()} rooms marked as available.")
    make_available.short_description = "Mark selected rooms as available"

    def make_unavailable(self, request, queryset):
        """Action to mark rooms as unavailable"""
        queryset.update(is_available=False)
        self.message_user(
            request, f"{queryset.count()} rooms marked as unavailable.")
    make_unavailable.short_description = "Mark selected rooms as unavailable"

    # Display method for available_beds (since it's a property)
    def available_beds(self, obj):
        return obj.available_beds
    available_beds.short_description = 'Available Beds'


# Register all models
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(StudentProfile, StudentProfileAdmin)
admin.site.register(Room, RoomAdmin)

# Customize admin site header and title
admin.site.site_header = "Hostel Management System"
admin.site.site_title = "HMS Admin"
admin.site.index_title = "Welcome to Hostel Management System"
