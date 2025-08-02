from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, StudentProfile
from datetime import date


@receiver(post_save, sender=CustomUser)
def create_student_profile(sender, instance, created, **kwargs):
    """
    Automatically create a StudentProfile when a student user is created
    """
    if created and instance.user_type == 'student':
        # Create a temporary student ID (you can change this logic later)
        temp_student_id = f"TEMP{instance.id:04d}"

        StudentProfile.objects.create(
            user=instance,
            student_id=temp_student_id,
            department="Not Set",
            faculty="Not Set",
            academic_level="Undergraduate",
            academic_year=date.today().year,
            semester=1,
            emergency_contact="Not Set",
            emergency_contact_name="Not Set",
            date_of_enrollment=date.today()
        )


@receiver(post_save, sender=CustomUser)
def save_student_profile(sender, instance, **kwargs):
    """
    Save the StudentProfile when the user is saved
    """
    if instance.user_type == 'student' and hasattr(instance, 'student_profile'):
        instance.student_profile.save()
