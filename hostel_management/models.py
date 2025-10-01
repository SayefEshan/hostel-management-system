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


class RoomApplication(models.Model):
    """
    Room application model for students to apply for rooms
    """
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    )
    
    # Application details
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='room_applications')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='applications')
    
    # Application info
    application_date = models.DateTimeField(auto_now_add=True)
    preferences = models.TextField(blank=True, help_text='Any specific preferences or requests')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Admin fields
    reviewed_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_applications')
    reviewed_date = models.DateTimeField(null=True, blank=True)
    admin_notes = models.TextField(blank=True, help_text='Admin notes for this application')
    
    # Priority scoring (can be auto-calculated based on criteria)
    priority_score = models.PositiveIntegerField(default=0, help_text='Higher score = higher priority')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Auto-update room occupancy when application is approved
        if self.pk:  # Existing application
            old_status = RoomApplication.objects.filter(pk=self.pk).first()
            if old_status and old_status.status != self.status:
                if self.status == 'approved':
                    # Approve application and allocate room
                    self.room.current_occupancy += 1
                    self.room.save()
                    # Mark student as allocated
                    self.student.is_allocated = True
                    self.student.save()
                elif old_status.status == 'approved' and self.status in ['rejected', 'withdrawn']:
                    # Remove allocation
                    self.room.current_occupancy = max(0, self.room.current_occupancy - 1)
                    self.room.save()
                    # Check if student has other approved applications
                    other_approved = RoomApplication.objects.filter(
                        student=self.student, status='approved'
                    ).exclude(pk=self.pk).exists()
                    if not other_approved:
                        self.student.is_allocated = False
                        self.student.save()
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # Update room occupancy if deleting approved application
        if self.status == 'approved':
            self.room.current_occupancy = max(0, self.room.current_occupancy - 1)
            self.room.save()
            # Check if student has other approved applications
            other_approved = RoomApplication.objects.filter(
                student=self.student, status='approved'
            ).exclude(pk=self.pk).exists()
            if not other_approved:
                self.student.is_allocated = False
                self.student.save()
        super().delete(*args, **kwargs)
    
    def __str__(self):
        return f"{self.student.student_id} - Room {self.room.room_number} ({self.status})"
    
    class Meta:
        ordering = ['-priority_score', '-application_date']
        unique_together = ['student', 'room']  # Prevent duplicate applications
        verbose_name = 'Room Application'
        verbose_name_plural = 'Room Applications'


class RoomAllocation(models.Model):
    """
    Direct room allocation model for admin to assign students to rooms
    """
    
    # Allocation details
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='room_allocations')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='allocations')
    
    # Allocation info
    allocated_date = models.DateTimeField(auto_now_add=True)
    allocated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='made_allocations')
    
    # Status
    is_active = models.BooleanField(default=True)
    checkout_date = models.DateTimeField(null=True, blank=True)
    checkout_reason = models.TextField(blank=True)
    
    # Notes
    allocation_notes = models.TextField(blank=True, help_text='Notes about this allocation')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Update room occupancy and student status
        if not self.pk:  # New allocation
            if self.is_active:
                self.room.current_occupancy += 1
                self.room.save()
                self.student.is_allocated = True
                self.student.save()
        else:  # Existing allocation
            old_allocation = RoomAllocation.objects.filter(pk=self.pk).first()
            if old_allocation and old_allocation.is_active != self.is_active:
                if not self.is_active:  # Deactivating
                    self.room.current_occupancy = max(0, self.room.current_occupancy - 1)
                    self.room.save()
                    # Check if student has other active allocations
                    other_active = RoomAllocation.objects.filter(
                        student=self.student, is_active=True
                    ).exclude(pk=self.pk).exists()
                    if not other_active:
                        self.student.is_allocated = False
                        self.student.save()
                elif self.is_active:  # Activating
                    self.room.current_occupancy += 1
                    self.room.save()
                    self.student.is_allocated = True
                    self.student.save()
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # Update room occupancy if deleting active allocation
        if self.is_active:
            self.room.current_occupancy = max(0, self.room.current_occupancy - 1)
            self.room.save()
            # Check if student has other active allocations
            other_active = RoomAllocation.objects.filter(
                student=self.student, is_active=True
            ).exclude(pk=self.pk).exists()
            if not other_active:
                self.student.is_allocated = False
                self.student.save()
        super().delete(*args, **kwargs)
    
    def __str__(self):
        status = "Active" if self.is_active else "Inactive"
        return f"{self.student.student_id} - Room {self.room.room_number} ({status})"
    
    class Meta:
        ordering = ['-allocated_date']
        verbose_name = 'Room Allocation'
        verbose_name_plural = 'Room Allocations'


class Notice(models.Model):
    """
    Notice model for hostel announcements and notifications
    """
    
    CATEGORY_CHOICES = (
        ('general', 'General'),
        ('important', 'Important'),
        ('urgent', 'Urgent'),
        ('academic', 'Academic'),
        ('maintenance', 'Maintenance'),
    )
    
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    )
    
    # Notice content
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    
    # Publishing info
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_notices')
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True, help_text='Notice will be hidden after this date')
    
    # Status
    is_active = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)
    
    # Target audience (can be extended later)
    target_all_students = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.title} ({self.category})"
    
    @property
    def is_expired(self):
        """Check if notice is expired"""
        if self.expires_at:
            from django.utils import timezone
            return timezone.now() > self.expires_at
        return False
    
    class Meta:
        ordering = ['-priority', '-created_at']
        verbose_name = 'Notice'
        verbose_name_plural = 'Notices'


class Complaint(models.Model):
    """
    Complaint model for students to submit complaints and track resolution
    """
    
    CATEGORY_CHOICES = (
        ('maintenance', 'Maintenance'),
        ('security', 'Security'),
        ('facilities', 'Facilities'),
        ('cleanliness', 'Cleanliness'),
        ('noise', 'Noise'),
        ('other', 'Other'),
    )
    
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    )
    
    STATUS_CHOICES = (
        ('submitted', 'Submitted'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
        ('rejected', 'Rejected'),
    )
    
    # Complaint details
    submitted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='submitted_complaints')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    subject = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100, blank=True, help_text='Room number or specific location')
    
    # Status tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    
    # Assignment and resolution
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_complaints')
    assigned_date = models.DateTimeField(null=True, blank=True)
    resolution_notes = models.TextField(blank=True)
    resolved_date = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.subject} ({self.status})"
    
    @property
    def days_since_submission(self):
        """Calculate days since complaint was submitted"""
        from django.utils import timezone
        return (timezone.now() - self.created_at).days
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Complaint'
        verbose_name_plural = 'Complaints'
