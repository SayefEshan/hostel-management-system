from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from hostel_management.models import (
    CustomUser, StudentProfile, Room, RoomApplication, 
    RoomAllocation, Notice, Complaint
)


class Command(BaseCommand):
    help = 'Set up staff groups and permissions for hostel management'

    def handle(self, *args, **options):
        self.stdout.write('Setting up staff groups and permissions...')
        
        # Create groups
        hostel_staff_group, created = Group.objects.get_or_create(name='Hostel Staff')
        provost_group, created = Group.objects.get_or_create(name='Provost')
        admin_assistant_group, created = Group.objects.get_or_create(name='Admin Assistant')
        
        # Get content types
        room_ct = ContentType.objects.get_for_model(Room)
        room_app_ct = ContentType.objects.get_for_model(RoomApplication)
        room_alloc_ct = ContentType.objects.get_for_model(RoomAllocation)
        notice_ct = ContentType.objects.get_for_model(Notice)
        complaint_ct = ContentType.objects.get_for_model(Complaint)
        student_profile_ct = ContentType.objects.get_for_model(StudentProfile)
        
        # Basic staff permissions (Hostel Staff)
        basic_staff_permissions = [
            # Room Applications - full access
            ('view_roomapplication', room_app_ct),
            ('change_roomapplication', room_app_ct),
            
            # Room Allocations - full access
            ('view_roomallocation', room_alloc_ct),
            ('add_roomallocation', room_alloc_ct),
            ('change_roomallocation', room_alloc_ct),
            ('delete_roomallocation', room_alloc_ct),
            
            # Rooms - view and change only
            ('view_room', room_ct),
            ('change_room', room_ct),
            
            # Complaints - view and change
            ('view_complaint', complaint_ct),
            ('change_complaint', complaint_ct),
            
            # Student Profiles - view only
            ('view_studentprofile', student_profile_ct),
            
            # Notices - view only
            ('view_notice', notice_ct),
        ]
        
        # Provost permissions (includes all staff permissions plus more)
        provost_permissions = basic_staff_permissions + [
            # Rooms - full access
            ('add_room', room_ct),
            ('delete_room', room_ct),
            
            # Notices - full access
            ('add_notice', notice_ct),
            ('change_notice', notice_ct),
            ('delete_notice', notice_ct),
            
            # Room Applications - can delete
            ('delete_roomapplication', room_app_ct),
            
            # Student Profiles - can change
            ('change_studentprofile', student_profile_ct),
        ]
        
        # Admin Assistant permissions (limited access)
        admin_assistant_permissions = [
            # Room Applications - view only
            ('view_roomapplication', room_app_ct),
            
            # Rooms - view only
            ('view_room', room_ct),
            
            # Student Profiles - view only
            ('view_studentprofile', student_profile_ct),
            
            # Notices - can add and change
            ('view_notice', notice_ct),
            ('add_notice', notice_ct),
            ('change_notice', notice_ct),
            
            # Complaints - view only
            ('view_complaint', complaint_ct),
        ]
        
        # Assign permissions to groups
        self._assign_permissions_to_group(hostel_staff_group, basic_staff_permissions)
        self._assign_permissions_to_group(provost_group, provost_permissions)
        self._assign_permissions_to_group(admin_assistant_group, admin_assistant_permissions)
        
        self.stdout.write(
            self.style.SUCCESS('Successfully set up staff groups and permissions!')
        )
        
        # Display summary
        self.stdout.write('\nGroup Permissions Summary:')
        self.stdout.write(f'• Hostel Staff: {len(basic_staff_permissions)} permissions')
        self.stdout.write(f'• Provost: {len(provost_permissions)} permissions')
        self.stdout.write(f'• Admin Assistant: {len(admin_assistant_permissions)} permissions')
        
        self.stdout.write('\nTo assign users to groups:')
        self.stdout.write('• Use Django admin or run: python manage.py assign_staff_roles')
        
    def _assign_permissions_to_group(self, group, permissions):
        """Helper method to assign permissions to a group"""
        for perm_codename, content_type in permissions:
            try:
                permission = Permission.objects.get(
                    codename=perm_codename,
                    content_type=content_type
                )
                group.permissions.add(permission)
                self.stdout.write(f'  ✓ Added {perm_codename} to {group.name}')
            except Permission.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'  ⚠ Permission {perm_codename} not found')
                )