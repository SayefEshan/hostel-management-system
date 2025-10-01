from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from hostel_management.models import CustomUser


class Command(BaseCommand):
    help = 'Assign staff roles to users based on their user_type'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Assign role to specific username'
        )
        parser.add_argument(
            '--role',
            type=str,
            choices=['staff', 'provost', 'admin_assistant'],
            help='Specific role to assign'
        )
        parser.add_argument(
            '--auto',
            action='store_true',
            help='Automatically assign roles based on user_type'
        )

    def handle(self, *args, **options):
        if options['username'] and options['role']:
            # Assign specific role to specific user
            self._assign_specific_role(options['username'], options['role'])
        elif options['auto']:
            # Auto-assign roles based on user_type
            self._auto_assign_roles()
        else:
            # Interactive mode
            self._interactive_assignment()

    def _assign_specific_role(self, username, role):
        """Assign a specific role to a specific user"""
        try:
            user = CustomUser.objects.get(username=username)
            
            # Role mapping
            role_mapping = {
                'staff': 'Hostel Staff',
                'provost': 'Provost',
                'admin_assistant': 'Admin Assistant'
            }
            
            group_name = role_mapping[role]
            group = Group.objects.get(name=group_name)
            
            # Make user staff and add to group
            user.is_staff = True
            user.save()
            user.groups.add(group)
            
            self.stdout.write(
                self.style.SUCCESS(f'✓ Assigned {group_name} role to {username}')
            )
            
        except CustomUser.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'✗ User {username} not found')
            )
        except Group.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'✗ Group {role_mapping[role]} not found. Run setup_staff_permissions first.')
            )

    def _auto_assign_roles(self):
        """Automatically assign roles based on user_type"""
        self.stdout.write('Auto-assigning roles based on user_type...')
        
        # Get groups
        try:
            hostel_staff_group = Group.objects.get(name='Hostel Staff')
            provost_group = Group.objects.get(name='Provost')
            admin_assistant_group = Group.objects.get(name='Admin Assistant')
        except Group.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('Groups not found. Run setup_staff_permissions first.')
            )
            return
        
        # Assign roles based on user_type
        staff_users = CustomUser.objects.filter(user_type='staff')
        provost_users = CustomUser.objects.filter(user_type='provost')
        
        # Staff users get Hostel Staff role
        for user in staff_users:
            user.is_staff = True
            user.save()
            user.groups.add(hostel_staff_group)
            self.stdout.write(f'✓ Assigned Hostel Staff role to {user.username}')
        
        # Provost users get Provost role
        for user in provost_users:
            user.is_staff = True
            user.save()
            user.groups.add(provost_group)
            self.stdout.write(f'✓ Assigned Provost role to {user.username}')
        
        # Admin users keep superuser status
        admin_users = CustomUser.objects.filter(user_type='admin')
        for user in admin_users:
            if not user.is_superuser:
                user.is_staff = True
                user.is_superuser = True
                user.save()
                self.stdout.write(f'✓ Granted superuser access to {user.username}')
        
        self.stdout.write(
            self.style.SUCCESS(f'Auto-assigned roles to {staff_users.count() + provost_users.count()} users')
        )

    def _interactive_assignment(self):
        """Interactive role assignment"""
        self.stdout.write('Interactive Staff Role Assignment')
        self.stdout.write('=================================')
        
        # List all non-student users
        staff_users = CustomUser.objects.exclude(user_type='student')
        
        if not staff_users.exists():
            self.stdout.write('No staff users found.')
            return
        
        self.stdout.write('\nAvailable staff users:')
        for i, user in enumerate(staff_users, 1):
            current_groups = ', '.join([g.name for g in user.groups.all()])
            staff_status = '(Staff Access)' if user.is_staff else '(No Admin Access)'
            self.stdout.write(
                f'{i}. {user.username} ({user.get_user_type_display()}) '
                f'{staff_status} - Groups: {current_groups or "None"}'
            )
        
        self.stdout.write('\nAvailable roles:')
        self.stdout.write('1. Hostel Staff - Can manage applications, allocations, complaints')
        self.stdout.write('2. Provost - Full management access except user administration')
        self.stdout.write('3. Admin Assistant - Limited access for notices and viewing')
        self.stdout.write('4. Remove Admin Access')
        
        try:
            user_choice = input('\nEnter user number (or "q" to quit): ')
            if user_choice.lower() == 'q':
                return
            
            user_index = int(user_choice) - 1
            selected_user = list(staff_users)[user_index]
            
            role_choice = input('Enter role number (1-4): ')
            
            if role_choice == '1':
                self._assign_user_to_group(selected_user, 'Hostel Staff')
            elif role_choice == '2':
                self._assign_user_to_group(selected_user, 'Provost')
            elif role_choice == '3':
                self._assign_user_to_group(selected_user, 'Admin Assistant')
            elif role_choice == '4':
                self._remove_admin_access(selected_user)
            else:
                self.stdout.write('Invalid choice.')
                
        except (ValueError, IndexError):
            self.stdout.write('Invalid selection.')
        except KeyboardInterrupt:
            self.stdout.write('\nOperation cancelled.')

    def _assign_user_to_group(self, user, group_name):
        """Assign user to a specific group"""
        try:
            group = Group.objects.get(name=group_name)
            
            # Clear existing groups and add new one
            user.groups.clear()
            user.groups.add(group)
            user.is_staff = True
            user.save()
            
            self.stdout.write(
                self.style.SUCCESS(f'✓ Assigned {group_name} role to {user.username}')
            )
            
        except Group.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'✗ Group {group_name} not found')
            )

    def _remove_admin_access(self, user):
        """Remove admin access from user"""
        if user.is_superuser:
            self.stdout.write(
                self.style.WARNING(f'Cannot remove admin access from superuser {user.username}')
            )
            return
        
        user.groups.clear()
        user.is_staff = False
        user.save()
        
        self.stdout.write(
            self.style.SUCCESS(f'✓ Removed admin access from {user.username}')
        )