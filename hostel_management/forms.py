from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, StudentProfile, RoomApplication, Complaint

class CustomUserCreationForm(UserCreationForm):
    """Custom user registration form"""
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')
    phone = forms.CharField(max_length=15, required=False, help_text='Optional.')
    
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'user_type', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        
        # Set default user type to student
        self.fields['user_type'].initial = 'student'
        
        # Make user_type read-only for regular registration (students only)
        self.fields['user_type'].widget = forms.HiddenInput()

class StudentProfileForm(forms.ModelForm):
    """Form for editing student profile"""
    
    class Meta:
        model = StudentProfile
        fields = [
            'student_id', 'department', 'faculty', 'academic_level', 
            'academic_year', 'semester', 'emergency_contact', 
            'emergency_contact_name', 'date_of_enrollment'
        ]
        widgets = {
            'date_of_enrollment': forms.DateInput(attrs={'type': 'date'}),
            'academic_year': forms.NumberInput(attrs={'min': 2020, 'max': 2030}),
            'semester': forms.NumberInput(attrs={'min': 1, 'max': 8}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        
        # Add help text
        self.fields['student_id'].help_text = 'Your university student ID'
        self.fields['emergency_contact'].help_text = 'Phone number for emergency contact'

class RoomApplicationForm(forms.ModelForm):
    """Form for room application"""
    
    class Meta:
        model = RoomApplication
        fields = ['preferences']
        widgets = {
            'preferences': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.student = kwargs.pop('student', None)
        self.room = kwargs.pop('room', None)
        super().__init__(*args, **kwargs)
        self.fields['preferences'].help_text = 'Any specific preferences or requests (optional)'
    
    def clean(self):
        cleaned_data = super().clean()
        
        if self.student and self.room:
            # Check if student already has a pending application for this room
            existing_app = RoomApplication.objects.filter(
                student=self.student,
                room=self.room,
                status='pending'
            ).exists()
            
            if existing_app:
                raise forms.ValidationError(
                    'You already have a pending application for this room.'
                )
            
            # Check if student already has an approved application
            approved_app = RoomApplication.objects.filter(
                student=self.student,
                status='approved'
            ).exists()
            
            if approved_app:
                raise forms.ValidationError(
                    'You already have an approved room application. Please contact admin to modify your allocation.'
                )
            
            # Check if room is full
            if self.room.is_full:
                raise forms.ValidationError(
                    'This room is currently full. Please choose another room.'
                )
        
        return cleaned_data

class ComplaintForm(forms.ModelForm):
    """Form for creating complaints"""
    
    class Meta:
        model = Complaint
        fields = ['category', 'priority', 'subject', 'description', 'location']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }