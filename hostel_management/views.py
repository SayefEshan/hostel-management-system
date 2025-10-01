from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout
from django.contrib import messages
from django.views import View
from django.urls import reverse_lazy
from django.db.models import Q, F, Sum
from django.db import models
from django.http import Http404
from .models import CustomUser, StudentProfile, Room, RoomApplication, RoomAllocation, Notice, Complaint
from .forms import CustomUserCreationForm, StudentProfileForm, RoomApplicationForm, ComplaintForm
from datetime import date

class RegisterView(CreateView):
    """User registration view"""
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'hostel_management/auth/register.html'
    success_url = reverse_lazy('hostel_management:dashboard')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, 'Registration successful! Welcome to the Hostel Management System.')
        return response

class DashboardView(LoginRequiredMixin, TemplateView):
    """Main dashboard view for all user types"""
    template_name = 'hostel_management/dashboard/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Common context for all users
        context['total_rooms'] = Room.objects.count()
        context['available_rooms'] = Room.objects.filter(is_available=True, current_occupancy__lt=F('capacity')).count()
        
        if user.user_type == 'student':
            if hasattr(user, 'student_profile'):
                profile = user.student_profile
                context['student_profile'] = profile
                context['is_allocated'] = profile.is_allocated
                
                # Get current room allocation
                current_allocation = RoomAllocation.objects.filter(
                    student=profile, is_active=True
                ).first()
                context['current_allocation'] = current_allocation
                
                # Get pending applications
                pending_applications = RoomApplication.objects.filter(
                    student=profile, status='pending'
                ).count()
                context['pending_applications'] = pending_applications
                
                # Get recent complaints
                recent_complaints = Complaint.objects.filter(
                    submitted_by=user, status__in=['submitted', 'in_progress']
                ).count()
                context['open_complaints'] = recent_complaints
        
        elif user.user_type in ['staff', 'provost', 'admin']:
            # Add staff-specific dashboard data
            context['total_students'] = StudentProfile.objects.count()
            context['allocated_students'] = StudentProfile.objects.filter(is_allocated=True).count()
            
            # Pending applications requiring attention
            context['pending_applications'] = RoomApplication.objects.filter(status='pending').count()
            
            # Open complaints requiring attention
            context['open_complaints'] = Complaint.objects.filter(
                status__in=['submitted', 'in_progress']
            ).count()
            
            # Occupancy rate
            total_capacity = Room.objects.aggregate(
                total=models.Sum('capacity')
            )['total'] or 0
            total_occupied = Room.objects.aggregate(
                occupied=models.Sum('current_occupancy')
            )['occupied'] or 0
            
            context['total_capacity'] = total_capacity
            context['total_occupied'] = total_occupied
            context['occupancy_rate'] = round(
                (total_occupied / total_capacity * 100) if total_capacity > 0 else 0, 1
            )
        
        return context

class RoomListView(LoginRequiredMixin, ListView):
    """List all available rooms"""
    model = Room
    template_name = 'hostel_management/rooms/room_list.html'
    context_object_name = 'rooms'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Room.objects.filter(is_available=True)
        
        # Add filtering
        search = self.request.GET.get('search')
        room_type = self.request.GET.get('room_type')
        block = self.request.GET.get('block')
        
        if search:
            queryset = queryset.filter(
                Q(room_number__icontains=search) | 
                Q(block__icontains=search)
            )
        
        if room_type:
            queryset = queryset.filter(room_type=room_type)
            
        if block:
            queryset = queryset.filter(block=block)
        
        return queryset.order_by('block', 'floor', 'room_number')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room_types'] = Room.ROOM_TYPE_CHOICES
        context['blocks'] = Room.objects.values_list('block', flat=True).distinct()
        context['search'] = self.request.GET.get('search', '')
        context['selected_room_type'] = self.request.GET.get('room_type', '')
        context['selected_block'] = self.request.GET.get('block', '')
        return context

class RoomDetailView(LoginRequiredMixin, DetailView):
    """Room detail view"""
    model = Room
    template_name = 'hostel_management/rooms/room_detail.html'
    context_object_name = 'room'

class RoomApplicationView(LoginRequiredMixin, CreateView):
    """Room application view for students"""
    form_class = RoomApplicationForm
    template_name = 'hostel_management/rooms/room_apply.html'
    success_url = reverse_lazy('hostel_management:my_applications')
    
    def dispatch(self, request, *args, **kwargs):
        # Only students can apply for rooms
        if request.user.user_type != 'student':
            messages.error(request, 'Only students can apply for rooms.')
            return redirect('hostel_management:dashboard')
        
        # Check if student has profile
        if not hasattr(request.user, 'student_profile'):
            messages.error(request, 'Please complete your student profile first.')
            return redirect('hostel_management:profile_edit')
            
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room'] = get_object_or_404(Room, id=self.kwargs['room_id'])
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['student'] = self.request.user.student_profile
        kwargs['room'] = get_object_or_404(Room, id=self.kwargs['room_id'])
        return kwargs
    
    def form_valid(self, form):
        room = get_object_or_404(Room, id=self.kwargs['room_id'])
        
        # Check if student profile is complete
        student_profile = self.request.user.student_profile
        if (student_profile.department == "Not Set" or 
            student_profile.emergency_contact == "Not Set"):
            messages.error(self.request, 'Please complete your profile before applying for rooms.')
            return redirect('hostel_management:profile_edit')
        
        form.instance.student = student_profile
        form.instance.room = room
        
        # Calculate priority score based on academic year and level
        priority_score = 50  # Base score
        if student_profile.academic_level == 'PhD':
            priority_score += 30
        elif student_profile.academic_level == 'Postgraduate':
            priority_score += 20
        elif student_profile.academic_level == 'Graduate':
            priority_score += 10
        
        # Add points for higher academic years
        priority_score += min(student_profile.academic_year - 2020, 20)
        
        form.instance.priority_score = priority_score
        
        messages.success(
            self.request, 
            f'Your application for Room {room.room_number} has been submitted successfully. '
            f'Your priority score is {priority_score}. You will be notified about the decision.'
        )
        return super().form_valid(form)

class MyApplicationsView(LoginRequiredMixin, ListView):
    """View for students to see their room applications"""
    template_name = 'hostel_management/rooms/my_applications.html'
    context_object_name = 'applications'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.user_type != 'student':
            messages.error(request, 'Access denied.')
            return redirect('hostel_management:dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        return RoomApplication.objects.filter(student=self.request.user.student_profile)

class NoticeListView(LoginRequiredMixin, ListView):
    """List all notices"""
    template_name = 'hostel_management/notices/notice_list.html'
    context_object_name = 'notices'
    paginate_by = 10
    
    def get_queryset(self):
        from django.utils import timezone
        return Notice.objects.filter(
            is_published=True,
            is_active=True
        ).filter(
            Q(expires_at__isnull=True) | Q(expires_at__gt=timezone.now())
        )

class NoticeDetailView(LoginRequiredMixin, DetailView):
    """Notice detail view"""
    model = Notice
    template_name = 'hostel_management/notices/notice_detail.html'
    context_object_name = 'notice'

class ComplaintListView(LoginRequiredMixin, ListView):
    """List user's complaints"""
    template_name = 'hostel_management/complaints/complaint_list.html'
    context_object_name = 'complaints'
    paginate_by = 10
    
    def get_queryset(self):
        return Complaint.objects.filter(submitted_by=self.request.user)

class ComplaintCreateView(LoginRequiredMixin, CreateView):
    """Create new complaint"""
    form_class = ComplaintForm
    template_name = 'hostel_management/complaints/complaint_create.html'
    success_url = reverse_lazy('hostel_management:complaint_list')
    
    def form_valid(self, form):
        form.instance.submitted_by = self.request.user
        messages.success(self.request, 'Your complaint has been submitted successfully.')
        return super().form_valid(form)

class ComplaintDetailView(LoginRequiredMixin, DetailView):
    """Complaint detail view"""
    model = Complaint
    template_name = 'hostel_management/complaints/complaint_detail.html'
    context_object_name = 'complaint'
    
    def get_queryset(self):
        # Users can only see their own complaints, staff can see all
        if self.request.user.user_type in ['staff', 'provost', 'admin']:
            return Complaint.objects.all()
        return Complaint.objects.filter(submitted_by=self.request.user)

class ProfileView(LoginRequiredMixin, TemplateView):
    """User profile view"""
    template_name = 'hostel_management/profile/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        
        if user.user_type == 'student' and hasattr(user, 'student_profile'):
            context['student_profile'] = user.student_profile
        
        return context

class ProfileEditView(LoginRequiredMixin, UpdateView):
    """Edit user profile"""
    template_name = 'hostel_management/profile/profile_edit.html'
    success_url = reverse_lazy('hostel_management:profile')
    
    def get_object(self):
        if self.request.user.user_type == 'student':
            if hasattr(self.request.user, 'student_profile'):
                return self.request.user.student_profile
            else:
                raise Http404("Student profile not found")
        return self.request.user
    
    def get_form_class(self):
        if self.request.user.user_type == 'student':
            return StudentProfileForm
        # Add other user type forms as needed
        return StudentProfileForm
    
    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully.')
        return super().form_valid(form)


class CustomLogoutView(View):
    """Custom logout view that handles both GET and POST requests"""
    
    def get(self, request, *args, **kwargs):
        return self.logout_user(request)
    
    def post(self, request, *args, **kwargs):
        return self.logout_user(request)
    
    def logout_user(self, request):
        if request.user.is_authenticated:
            messages.success(request, 'You have been successfully logged out.')
            logout(request)
        return redirect('hostel_management:login')