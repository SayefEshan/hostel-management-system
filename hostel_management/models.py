from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    """
    Custom User model that extends Django's built-in User model.
    This allows us to add custom fields for different user types.
    """

    # User type choices
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('staff', 'Hostel Staff'),
        ('provost', 'Provost'),
        ('admin', 'System Admin'),
    )

    # Add custom fields
    user_type = models.CharField(
        max_length=10, choices=USER_TYPE_CHOICES, default='student')
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"


class StudentProfile(models.Model):
    """
    Student Profile model to store additional student-specific information.
    This is linked to CustomUser with a OneToOne relationship.
    """

    # Link to CustomUser
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='student_profile')

    # Student specific fields
    student_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    faculty = models.CharField(max_length=100)
    # Undergraduate, Graduate, etc.
    academic_level = models.CharField(max_length=50)
    academic_year = models.PositiveIntegerField()
    semester = models.PositiveIntegerField()
    emergency_contact = models.CharField(max_length=15)
    emergency_contact_name = models.CharField(max_length=100)
    date_of_enrollment = models.DateField()

    # Room allocation status (we'll link to Room model later)
    is_allocated = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student_id} - {self.user.get_full_name()}"

    class Meta:
        verbose_name = 'Student Profile'
        verbose_name_plural = 'Student Profiles'


class Room(models.Model):
    """
    Room model to store hostel room information
    """

    ROOM_TYPE_CHOICES = (
        ('single', 'Single Room'),
        ('double', 'Double Room'),
        ('triple', 'Triple Room'),
        ('dormitory', 'Dormitory'),
    )

    # Room basic info
    room_number = models.CharField(max_length=10, unique=True)
    block = models.CharField(max_length=50)  # e.g., "Block A", "Block B"
    floor = models.PositiveIntegerField()
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES)

    # Capacity info
    capacity = models.PositiveIntegerField()
    current_occupancy = models.PositiveIntegerField(default=0)

    # Facilities (we'll keep it simple for now)
    has_attached_bathroom = models.BooleanField(default=False)
    has_ac = models.BooleanField(default=False)

    # Status
    is_available = models.BooleanField(default=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Room {self.room_number} - {self.block}"

    @property
    def available_beds(self):
        """Calculate available beds in the room"""
        return self.capacity - self.current_occupancy

    @property
    def is_full(self):
        """Check if room is full"""
        return self.current_occupancy >= self.capacity

    class Meta:
        ordering = ['block', 'floor', 'room_number']
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'
