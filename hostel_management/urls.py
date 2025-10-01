from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'hostel_management'

urlpatterns = [
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='hostel_management/auth/login.html'), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    
    # Dashboard URLs
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard_alt'),
    
    # Room Management URLs
    path('rooms/', views.RoomListView.as_view(), name='room_list'),
    path('rooms/<int:pk>/', views.RoomDetailView.as_view(), name='room_detail'),
    path('rooms/apply/<int:room_id>/', views.RoomApplicationView.as_view(), name='room_apply'),
    path('my-applications/', views.MyApplicationsView.as_view(), name='my_applications'),
    
    # Notice Board URLs
    path('notices/', views.NoticeListView.as_view(), name='notice_list'),
    path('notices/<int:pk>/', views.NoticeDetailView.as_view(), name='notice_detail'),
    
    # Complaint Management URLs
    path('complaints/', views.ComplaintListView.as_view(), name='complaint_list'),
    path('complaints/create/', views.ComplaintCreateView.as_view(), name='complaint_create'),
    path('complaints/<int:pk>/', views.ComplaintDetailView.as_view(), name='complaint_detail'),
    
    # Profile URLs
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
]