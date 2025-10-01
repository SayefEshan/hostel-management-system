from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from datetime import datetime, date
from hostel_management.models import (
    CustomUser, StudentProfile, Room, RoomApplication, 
    RoomAllocation, Notice, Complaint
)


class Command(BaseCommand):
    help = 'Seed the database with sample data for testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding'
        )
        parser.add_argument(
            '--users-only',
            action='store_true',
            help='Only create users and profiles'
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.clear_data()
        
        if options['users_only']:
            self.create_users()
            self.create_student_profiles()
        else:
            self.create_users()
            self.create_student_profiles()
            self.create_rooms()
            self.create_room_allocations()
            self.create_room_applications()
            self.create_notices()
            self.create_complaints()
        
        self.stdout.write(
            self.style.SUCCESS('Successfully seeded database with sample data!')
        )

    def clear_data(self):
        """Clear all existing data"""
        self.stdout.write('Clearing existing data...')
        
        Complaint.objects.all().delete()
        Notice.objects.all().delete()
        RoomApplication.objects.all().delete()
        RoomAllocation.objects.all().delete()
        Room.objects.all().delete()
        StudentProfile.objects.all().delete()
        CustomUser.objects.all().delete()
        
        self.stdout.write(self.style.WARNING('All data cleared!'))

    def create_users(self):
        """Create sample users"""
        self.stdout.write('Creating users...')
        
        users_data = [
            {
                'username': 'admin',
                'email': 'admin@bau.edu.bd',
                'first_name': 'System',
                'last_name': 'Administrator',
                'user_type': 'admin',
                'phone': '+880-1700-000001',
                'is_staff': True,
                'is_superuser': True,
                'password': 'admin123'
            },
            {
                'username': 'staff1',
                'email': 'staff1@bau.edu.bd',
                'first_name': 'Mohammad',
                'last_name': 'Rahman',
                'user_type': 'staff',
                'phone': '+880-1700-000002',
                'is_staff': True,
                'is_superuser': False,
                'password': 'staff123'
            },
            {
                'username': 'provost1',
                'email': 'provost@bau.edu.bd',
                'first_name': 'Dr. Abdul',
                'last_name': 'Karim',
                'user_type': 'provost',
                'phone': '+880-1700-000003',
                'is_staff': True,
                'is_superuser': False,
                'password': 'provost123'
            },
            {
                'username': 'student1',
                'email': 'student1@bau.edu.bd',
                'first_name': 'Ahmed',
                'last_name': 'Hassan',
                'user_type': 'student',
                'phone': '+880-1700-000004',
                'is_staff': False,
                'is_superuser': False,
                'password': 'student123'
            },
            {
                'username': 'student2',
                'email': 'student2@bau.edu.bd',
                'first_name': 'Fatima',
                'last_name': 'Khan',
                'user_type': 'student',
                'phone': '+880-1700-000005',
                'is_staff': False,
                'is_superuser': False,
                'password': 'student123'
            },
            {
                'username': 'student3',
                'email': 'student3@bau.edu.bd',
                'first_name': 'Rahim',
                'last_name': 'Uddin',
                'user_type': 'student',
                'phone': '+880-1700-000006',
                'is_staff': False,
                'is_superuser': False,
                'password': 'student123'
            },
            {
                'username': 'student4',
                'email': 'student4@bau.edu.bd',
                'first_name': 'Sarah',
                'last_name': 'Ali',
                'user_type': 'student',
                'phone': '+880-1700-000007',
                'is_staff': False,
                'is_superuser': False,
                'password': 'student123'
            },
            {
                'username': 'student5',
                'email': 'student5@bau.edu.bd',
                'first_name': 'Omar',
                'last_name': 'Sheikh',
                'user_type': 'student',
                'phone': '+880-1700-000008',
                'is_staff': False,
                'is_superuser': False,
                'password': 'student123'
            }
        ]
        
        for user_data in users_data:
            password = user_data.pop('password')
            user, created = CustomUser.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    **user_data,
                    'password': make_password(password)
                }
            )
            if created:
                self.stdout.write(f'  ✓ Created user: {user.username}')
            else:
                self.stdout.write(f'  → User already exists: {user.username}')

    def create_student_profiles(self):
        """Create student profiles"""
        self.stdout.write('Creating student profiles...')
        
        students_data = [
            {
                'username': 'student1',
                'student_id': 'BAU-CS-2023-001',
                'department': 'Computer Science',
                'faculty': 'Engineering',
                'academic_level': 'Graduate',
                'academic_year': 2023,
                'semester': 'Fall',
                'date_of_enrollment': date(2023, 1, 15),
                'emergency_contact': '+880-1700-111001',
                'emergency_contact_name': 'Hassan Ahmed (Father)',
                'is_allocated': False
            },
            {
                'username': 'student2',
                'student_id': 'BAU-BIO-2022-015',
                'department': 'Biology',
                'faculty': 'Life Sciences',
                'academic_level': 'Graduate',
                'academic_year': 2022,
                'semester': 'Spring',
                'date_of_enrollment': date(2022, 9, 1),
                'emergency_contact': '+880-1700-111002',
                'emergency_contact_name': 'Khan Mohammad (Father)',
                'is_allocated': True
            },
            {
                'username': 'student3',
                'student_id': 'BAU-AGR-2021-032',
                'department': 'Agriculture',
                'faculty': 'Agriculture',
                'academic_level': 'Postgraduate',
                'academic_year': 2021,
                'semester': 'Fall',
                'date_of_enrollment': date(2021, 1, 10),
                'emergency_contact': '+880-1700-111003',
                'emergency_contact_name': 'Uddin Ali (Father)',
                'is_allocated': False
            },
            {
                'username': 'student4',
                'student_id': 'BAU-ENG-2023-045',
                'department': 'English',
                'faculty': 'Arts',
                'academic_level': 'Graduate',
                'academic_year': 2023,
                'semester': 'Spring',
                'date_of_enrollment': date(2023, 9, 1),
                'emergency_contact': '+880-1700-111004',
                'emergency_contact_name': 'Ali Mohammad (Father)',
                'is_allocated': False
            },
            {
                'username': 'student5',
                'student_id': 'BAU-PHY-2022-078',
                'department': 'Physics',
                'faculty': 'Science',
                'academic_level': 'PhD',
                'academic_year': 2022,
                'semester': 'Fall',
                'date_of_enrollment': date(2022, 1, 15),
                'emergency_contact': '+880-1700-111005',
                'emergency_contact_name': 'Sheikh Rahman (Father)',
                'is_allocated': False
            }
        ]
        
        for profile_data in students_data:
            username = profile_data.pop('username')
            try:
                user = CustomUser.objects.get(username=username)
                profile, created = StudentProfile.objects.get_or_create(
                    user=user,
                    defaults=profile_data
                )
                if created:
                    self.stdout.write(f'  ✓ Created profile for: {username}')
                else:
                    self.stdout.write(f'  → Profile already exists for: {username}')
            except CustomUser.DoesNotExist:
                self.stdout.write(f'  ✗ User {username} not found')

    def create_rooms(self):
        """Create sample rooms"""
        self.stdout.write('Creating rooms...')
        
        rooms_data = [
            # Block A - Ground Floor
            {'room_number': '101', 'block': 'A', 'floor': 1, 'room_type': 'single', 'capacity': 1, 'current_occupancy': 0, 'has_attached_bathroom': True, 'has_ac': False},
            {'room_number': '102', 'block': 'A', 'floor': 1, 'room_type': 'double', 'capacity': 2, 'current_occupancy': 1, 'has_attached_bathroom': True, 'has_ac': False},
            {'room_number': '103', 'block': 'A', 'floor': 1, 'room_type': 'triple', 'capacity': 3, 'current_occupancy': 0, 'has_attached_bathroom': False, 'has_ac': False},
            {'room_number': '104', 'block': 'A', 'floor': 1, 'room_type': 'double', 'capacity': 2, 'current_occupancy': 0, 'has_attached_bathroom': True, 'has_ac': False},
            {'room_number': '105', 'block': 'A', 'floor': 1, 'room_type': 'single', 'capacity': 1, 'current_occupancy': 0, 'has_attached_bathroom': True, 'has_ac': True},
            
            # Block A - Second Floor
            {'room_number': '201', 'block': 'A', 'floor': 2, 'room_type': 'single', 'capacity': 1, 'current_occupancy': 0, 'has_attached_bathroom': True, 'has_ac': True},
            {'room_number': '202', 'block': 'A', 'floor': 2, 'room_type': 'double', 'capacity': 2, 'current_occupancy': 0, 'has_attached_bathroom': True, 'has_ac': True},
            {'room_number': '203', 'block': 'A', 'floor': 2, 'room_type': 'triple', 'capacity': 3, 'current_occupancy': 2, 'has_attached_bathroom': False, 'has_ac': False},
            
            # Block B - Ground Floor
            {'room_number': '101', 'block': 'B', 'floor': 1, 'room_type': 'single', 'capacity': 1, 'current_occupancy': 0, 'has_attached_bathroom': True, 'has_ac': True},
            {'room_number': '102', 'block': 'B', 'floor': 1, 'room_type': 'double', 'capacity': 2, 'current_occupancy': 2, 'has_attached_bathroom': True, 'has_ac': True, 'is_available': False},
            {'room_number': '103', 'block': 'B', 'floor': 1, 'room_type': 'single', 'capacity': 1, 'current_occupancy': 0, 'has_attached_bathroom': True, 'has_ac': False},
            {'room_number': '104', 'block': 'B', 'floor': 1, 'room_type': 'triple', 'capacity': 3, 'current_occupancy': 1, 'has_attached_bathroom': False, 'has_ac': False},
            
            # Block C - Premium Rooms
            {'room_number': '301', 'block': 'C', 'floor': 3, 'room_type': 'single', 'capacity': 1, 'current_occupancy': 0, 'has_attached_bathroom': True, 'has_ac': True},
            {'room_number': '302', 'block': 'C', 'floor': 3, 'room_type': 'single', 'capacity': 1, 'current_occupancy': 0, 'has_attached_bathroom': True, 'has_ac': True},
            {'room_number': '303', 'block': 'C', 'floor': 3, 'room_type': 'double', 'capacity': 2, 'current_occupancy': 0, 'has_attached_bathroom': True, 'has_ac': True}
        ]
        
        for room_data in rooms_data:
            # Set default values
            room_data.setdefault('is_available', True)
            
            room, created = Room.objects.get_or_create(
                room_number=room_data['room_number'],
                block=room_data['block'],
                defaults=room_data
            )
            if created:
                self.stdout.write(f"  ✓ Created room: {room.block}-{room.room_number}")
            else:
                self.stdout.write(f"  → Room already exists: {room.block}-{room.room_number}")

    def create_room_allocations(self):
        """Create sample room allocations"""
        self.stdout.write('Creating room allocations...')
        
        try:
            # Allocate student2 to room A-102
            student2 = CustomUser.objects.get(username='student2').student_profile
            room_a102 = Room.objects.get(room_number='102', block='A')
            staff1 = CustomUser.objects.get(username='staff1')
            
            allocation, created = RoomAllocation.objects.get_or_create(
                student=student2,
                room=room_a102,
                is_active=True,
                defaults={
                    'allocated_by': staff1,
                    'allocation_notes': 'Allocated based on academic performance'
                }
            )
            if created:
                self.stdout.write(f"  ✓ Allocated {student2.user.username} to room {room_a102.block}-{room_a102.room_number}")
            
        except Exception as e:
            self.stdout.write(f"  ✗ Error creating allocations: {e}")

    def create_room_applications(self):
        """Create sample room applications"""
        self.stdout.write('Creating room applications...')
        
        applications_data = [
            {
                'student_username': 'student1',
                'room_number': '101',
                'room_block': 'A',
                'status': 'pending',
                'priority_score': 75,
                'preferences': 'Prefer quiet environment for studies'
            },
            {
                'student_username': 'student3',
                'room_number': '301',
                'room_block': 'C',
                'status': 'approved',
                'priority_score': 85,
                'preferences': 'Need AC for health reasons',
                'reviewed_by_username': 'staff1',
                'admin_notes': 'Approved due to high priority score and medical needs'
            },
            {
                'student_username': 'student4',
                'room_number': '201',
                'room_block': 'A',
                'status': 'pending',
                'priority_score': 60,
                'preferences': 'Prefer upper floors'
            },
            {
                'student_username': 'student5',
                'room_number': '302',
                'room_block': 'C',
                'status': 'rejected',
                'priority_score': 90,
                'preferences': 'PhD student, need quiet space',
                'reviewed_by_username': 'provost1',
                'admin_notes': 'Room reserved for faculty guest'
            }
        ]
        
        for app_data in applications_data:
            try:
                student = CustomUser.objects.get(username=app_data['student_username']).student_profile
                room = Room.objects.get(
                    room_number=app_data['room_number'],
                    block=app_data['room_block']
                )
                
                app_defaults = {
                    'status': app_data['status'],
                    'priority_score': app_data['priority_score'],
                    'preferences': app_data['preferences']
                }
                
                if 'reviewed_by_username' in app_data:
                    reviewed_by = CustomUser.objects.get(username=app_data['reviewed_by_username'])
                    app_defaults['reviewed_by'] = reviewed_by
                    app_defaults['reviewed_date'] = timezone.now()
                
                if 'admin_notes' in app_data:
                    app_defaults['admin_notes'] = app_data['admin_notes']
                
                application, created = RoomApplication.objects.get_or_create(
                    student=student,
                    room=room,
                    defaults=app_defaults
                )
                
                if created:
                    self.stdout.write(f"  ✓ Created application: {student.user.username} → {room.block}-{room.room_number}")
                
            except Exception as e:
                self.stdout.write(f"  ✗ Error creating application: {e}")

    def create_notices(self):
        """Create sample notices"""
        self.stdout.write('Creating notices...')
        
        notices_data = [
            {
                'title': 'Welcome to BAU Hostel Management System',
                'content': '''Dear Students,

Welcome to the newly launched BAU Hostel Management System. This digital platform will help you:

• Apply for rooms online
• Track your application status
• File complaints and suggestions
• Stay updated with hostel notices

For any technical issues, please contact the IT support team.

Best regards,
Hostel Administration''',
                'category': 'general',
                'priority': 'medium',
                'created_by_username': 'staff1',
                'target_all_students': True
            },
            {
                'title': 'Room Application Deadline - Spring 2024',
                'content': '''Important Notice:

The deadline for Spring 2024 room applications is March 15, 2024.

Key Points:
• Applications must be submitted through the online portal
• Late applications will not be accepted
• Preference will be given to senior students
• Room allocation results will be announced on March 20, 2024

For queries, contact the hostel office during working hours.

Hostel Administration Team''',
                'category': 'urgent',
                'priority': 'high',
                'created_by_username': 'provost1',
                'target_all_students': True,
                'expires_at': timezone.now().replace(month=3, day=20, hour=23, minute=59, second=59)
            },
            {
                'title': 'Maintenance Schedule - Block A',
                'content': '''Scheduled Maintenance Notice:

Block A will undergo electrical maintenance on the following dates:
• March 10, 2024 (9:00 AM - 5:00 PM)
• March 11, 2024 (9:00 AM - 3:00 PM)

During this time:
• Power may be interrupted intermittently
• WiFi services may be affected
• Hot water will not be available

We apologize for any inconvenience caused.

Maintenance Team''',
                'category': 'maintenance',
                'priority': 'medium',
                'created_by_username': 'staff1',
                'target_all_students': False
            }
        ]
        
        for notice_data in notices_data:
            try:
                created_by_username = notice_data.pop('created_by_username')
                created_by = CustomUser.objects.get(username=created_by_username)
                
                notice, created = Notice.objects.get_or_create(
                    title=notice_data['title'],
                    defaults={
                        **notice_data,
                        'created_by': created_by,
                        'is_active': True,
                        'is_published': True
                    }
                )
                
                if created:
                    self.stdout.write(f"  ✓ Created notice: {notice.title}")
                
            except Exception as e:
                self.stdout.write(f"  ✗ Error creating notice: {e}")

    def create_complaints(self):
        """Create sample complaints"""
        self.stdout.write('Creating complaints...')
        
        complaints_data = [
            {
                'submitted_by_username': 'student1',
                'category': 'maintenance',
                'priority': 'medium',
                'subject': 'WiFi Connection Issues in Block A',
                'description': 'The WiFi connection in Block A, first floor has been very slow for the past week. Students are unable to attend online classes properly. Please resolve this issue urgently.',
                'location': 'Block A, Floor 1',
                'status': 'submitted'
            },
            {
                'submitted_by_username': 'student2',
                'category': 'facilities',
                'priority': 'low',
                'subject': 'Request for Study Room Extension Hours',
                'description': 'Currently the study room closes at 10 PM. During exam periods, students need to study late. Please consider extending the hours until 12 AM during exam weeks.',
                'location': 'Common Study Room',
                'status': 'in_progress',
                'assigned_to_username': 'staff1'
            },
            {
                'submitted_by_username': 'student4',
                'category': 'security',
                'priority': 'high',
                'subject': 'Broken Lock in Room A-203',
                'description': 'The door lock in room A-203 is broken and cannot be secured properly. This is a security concern for the students living there.',
                'location': 'Block A, Room 203',
                'status': 'submitted'
            }
        ]
        
        for complaint_data in complaints_data:
            try:
                submitted_by_username = complaint_data.pop('submitted_by_username')
                submitted_by = CustomUser.objects.get(username=submitted_by_username)
                
                defaults = {
                    **complaint_data,
                    'submitted_by': submitted_by
                }
                
                if 'assigned_to_username' in complaint_data:
                    assigned_to_username = complaint_data.pop('assigned_to_username')
                    assigned_to = CustomUser.objects.get(username=assigned_to_username)
                    defaults['assigned_to'] = assigned_to
                    defaults['assigned_date'] = timezone.now()
                
                complaint, created = Complaint.objects.get_or_create(
                    subject=complaint_data['subject'],
                    submitted_by=submitted_by,
                    defaults=defaults
                )
                
                if created:
                    self.stdout.write(f"  ✓ Created complaint: {complaint.subject}")
                
            except Exception as e:
                self.stdout.write(f"  ✗ Error creating complaint: {e}")