from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import CustomUser, StudentProfile, Room, RoomApplication, RoomAllocation, Notice, Complaint

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
                    'capacity', 'current_occupancy', 'available_beds', 'availability_badge')
    list_filter = ('block', 'floor', 'room_type', 'is_available',
                   'has_attached_bathroom', 'has_ac')
    search_fields = ('room_number', 'block')
    
    def availability_badge(self, obj):
        if obj.is_available and obj.available_beds > 0:
            return format_html('<span class="status-badge status-approved">Available</span>')
        elif obj.is_available and obj.available_beds == 0:
            return format_html('<span class="status-badge status-pending">Full</span>')
        else:
            return format_html('<span class="status-badge status-rejected">Unavailable</span>')
    availability_badge.short_description = 'Availability'

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


class RoomApplicationAdmin(admin.ModelAdmin):
    """Admin configuration for RoomApplication model"""
    
    list_display = ('student', 'room', 'status', 'status_badge', 'priority_score', 'application_date', 'reviewed_by')
    list_filter = ('status', 'room__block', 'room__room_type', 'application_date')
    search_fields = ('student__student_id', 'student__user__username', 'room__room_number')
    list_editable = ('status', 'priority_score')
    
    def status_badge(self, obj):
        colors = {
            'pending': 'warning',
            'approved': 'success', 
            'rejected': 'danger'
        }
        return format_html(
            '<span class="status-badge status-{}">{}</span>',
            obj.status,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    fieldsets = (
        ('Application Info', {
            'fields': ('student', 'room', 'preferences', 'priority_score')
        }),
        ('Status & Review', {
            'fields': ('status', 'reviewed_by', 'reviewed_date', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('application_date', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('application_date', 'created_at', 'updated_at')
    
    actions = ['approve_applications', 'reject_applications', 'set_reviewed_by_me']
    
    def approve_applications(self, request, queryset):
        from django.utils import timezone
        updated = queryset.filter(status='pending').update(
            status='approved', 
            reviewed_by=request.user,
            reviewed_date=timezone.now()
        )
        self.message_user(request, f"{updated} applications approved and students allocated.")
    approve_applications.short_description = "Approve selected pending applications"
    
    def reject_applications(self, request, queryset):
        from django.utils import timezone
        updated = queryset.filter(status='pending').update(
            status='rejected', 
            reviewed_by=request.user,
            reviewed_date=timezone.now()
        )
        self.message_user(request, f"{updated} applications rejected.")
    reject_applications.short_description = "Reject selected pending applications"
    
    def set_reviewed_by_me(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(
            reviewed_by=request.user,
            reviewed_date=timezone.now()
        )
        self.message_user(request, f"{updated} applications marked as reviewed by you.")
    set_reviewed_by_me.short_description = "Mark as reviewed by me"
    
    def save_model(self, request, obj, form, change):
        if change and 'status' in form.changed_data:
            from django.utils import timezone
            obj.reviewed_by = request.user
            obj.reviewed_date = timezone.now()
        super().save_model(request, obj, form, change)


class RoomAllocationAdmin(admin.ModelAdmin):
    """Admin configuration for RoomAllocation model"""
    
    list_display = ('student', 'room', 'is_active', 'status_badge', 'allocated_date', 'allocated_by', 'checkout_date')
    list_filter = ('is_active', 'room__block', 'room__room_type', 'allocated_date')
    search_fields = ('student__student_id', 'student__user__username', 'room__room_number')
    list_editable = ('is_active',)
    
    def status_badge(self, obj):
        if obj.is_active:
            return format_html('<span class="status-badge status-active">Active</span>')
        else:
            return format_html('<span class="status-badge status-rejected">Inactive</span>')
    status_badge.short_description = 'Status'
    
    fieldsets = (
        ('Allocation Details', {
            'fields': ('student', 'room', 'is_active', 'allocated_by')
        }),
        ('Checkout Information', {
            'fields': ('checkout_date', 'checkout_reason'),
            'classes': ('collapse',)
        }),
        ('Notes', {
            'fields': ('allocation_notes',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('allocated_date', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('allocated_date', 'created_at', 'updated_at')
    
    actions = ['activate_allocations', 'deactivate_allocations', 'checkout_students']
    
    def activate_allocations(self, request, queryset):
        updated = queryset.filter(is_active=False).update(is_active=True)
        self.message_user(request, f"{updated} allocations activated.")
    activate_allocations.short_description = "Activate selected allocations"
    
    def deactivate_allocations(self, request, queryset):
        updated = queryset.filter(is_active=True).update(is_active=False)
        self.message_user(request, f"{updated} allocations deactivated.")
    deactivate_allocations.short_description = "Deactivate selected allocations"
    
    def checkout_students(self, request, queryset):
        from django.utils import timezone
        updated = queryset.filter(is_active=True).update(
            is_active=False, 
            checkout_date=timezone.now(),
            checkout_reason="Admin checkout"
        )
        self.message_user(request, f"{updated} students checked out.")
    checkout_students.short_description = "Checkout selected students"
    
    def save_model(self, request, obj, form, change):
        if not change:  # New allocation
            obj.allocated_by = request.user
        super().save_model(request, obj, form, change)


class NoticeAdmin(admin.ModelAdmin):
    """Admin configuration for Notice model"""
    
    list_display = ('title', 'category', 'priority', 'is_published', 'created_by', 'created_at', 'expires_at')
    list_filter = ('category', 'priority', 'is_published', 'is_active', 'created_at')
    search_fields = ('title', 'content')
    list_editable = ('is_published', 'priority')
    
    fieldsets = (
        ('Notice Content', {
            'fields': ('title', 'content', 'category', 'priority')
        }),
        ('Publishing', {
            'fields': ('is_active', 'is_published', 'expires_at', 'target_all_students')
        }),
    )
    
    readonly_fields = ('created_by', 'created_at')
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new notice
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


class ComplaintAdmin(admin.ModelAdmin):
    """Admin configuration for Complaint model"""
    
    list_display = ('subject', 'submitted_by', 'category', 'priority', 'status', 'assigned_to', 'created_at')
    list_filter = ('category', 'priority', 'status', 'created_at')
    search_fields = ('subject', 'description', 'submitted_by__username', 'location')
    list_editable = ('status', 'assigned_to')
    
    fieldsets = (
        ('Complaint Details', {
            'fields': ('submitted_by', 'category', 'priority', 'subject', 'description', 'location')
        }),
        ('Status & Assignment', {
            'fields': ('status', 'assigned_to', 'assigned_date', 'resolution_notes', 'resolved_date')
        }),
    )
    
    readonly_fields = ('submitted_by', 'created_at', 'updated_at')
    
    actions = ['assign_to_me', 'mark_in_progress', 'mark_resolved']
    
    def assign_to_me(self, request, queryset):
        queryset.update(assigned_to=request.user, status='in_progress')
        self.message_user(request, f"{queryset.count()} complaints assigned to you.")
    assign_to_me.short_description = "Assign selected complaints to me"
    
    def mark_in_progress(self, request, queryset):
        queryset.update(status='in_progress')
        self.message_user(request, f"{queryset.count()} complaints marked as in progress.")
    mark_in_progress.short_description = "Mark as in progress"
    
    def mark_resolved(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='resolved', resolved_date=timezone.now())
        self.message_user(request, f"{queryset.count()} complaints marked as resolved.")
    mark_resolved.short_description = "Mark as resolved"


# Register all models
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(StudentProfile, StudentProfileAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(RoomApplication, RoomApplicationAdmin)
admin.site.register(RoomAllocation, RoomAllocationAdmin)
admin.site.register(Notice, NoticeAdmin)
admin.site.register(Complaint, ComplaintAdmin)

# Customize admin site header and title
admin.site.site_header = "BAU Hostel Management System"
admin.site.site_title = "HMS Admin Portal"
admin.site.index_title = "Welcome to BAU Hostel Management System"

# Custom AdminSite for role-based access
class StaffAdminSite(admin.AdminSite):
    """Custom admin site for staff users"""
    site_header = "HMS Staff Panel"
    site_title = "Staff Management"
    index_title = "Staff Dashboard"
    
    def has_permission(self, request):
        """Override to allow staff users"""
        return request.user.is_active and request.user.is_staff

# Create staff admin site instance
staff_admin_site = StaffAdminSite(name='staff_admin')

# Function to check if user is staff (not superuser)
def is_staff_user(user):
    return user.is_staff and not user.is_superuser

# Custom admin mixin for staff permissions
class StaffAdminMixin:
    """Mixin to customize admin behavior for staff users"""
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if is_staff_user(request.user):
            # Staff users see all data, but with limited actions
            return qs
        return qs
    
    def has_add_permission(self, request):
        if is_staff_user(request.user):
            # Check specific permission
            return request.user.has_perm(f'{self.model._meta.app_label}.add_{self.model._meta.model_name}')
        return super().has_add_permission(request)
    
    def has_change_permission(self, request, obj=None):
        if is_staff_user(request.user):
            return request.user.has_perm(f'{self.model._meta.app_label}.change_{self.model._meta.model_name}')
        return super().has_change_permission(request, obj)
    
    def has_delete_permission(self, request, obj=None):
        if is_staff_user(request.user):
            return request.user.has_perm(f'{self.model._meta.app_label}.delete_{self.model._meta.model_name}')
        return super().has_delete_permission(request, obj)

# Update existing admin classes to include staff mixin
class StaffRoomApplicationAdmin(StaffAdminMixin, RoomApplicationAdmin):
    """Enhanced Room Application admin for staff"""
    pass

class StaffRoomAllocationAdmin(StaffAdminMixin, RoomAllocationAdmin):
    """Enhanced Room Allocation admin for staff"""
    pass

class StaffRoomAdmin(StaffAdminMixin, RoomAdmin):
    """Enhanced Room admin for staff"""
    pass

class StaffComplaintAdmin(StaffAdminMixin, ComplaintAdmin):
    """Enhanced Complaint admin for staff"""
    pass

class StaffNoticeAdmin(StaffAdminMixin, NoticeAdmin):
    """Enhanced Notice admin for staff"""
    pass

# Register models with both regular admin and staff admin
# (Staff will use the same admin but with different permissions)
pass
