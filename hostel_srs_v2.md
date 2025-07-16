# Software Requirements Specification (SRS)

## Hostel Management System

**Version:** 2.0  
**Date:** July 16, 2025  
**Prepared by:** Development Team  
**Document Status:** Final Draft  
**Technology Stack:** Python Django with Built-in Templates

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Overall Description](#2-overall-description)
3. [System Features](#3-system-features)
4. [Technical Requirements](#4-technical-requirements)
5. [Implementation Guidelines](#5-implementation-guidelines)
6. [Future Enhancements](#6-future-enhancements)

---

## 1. Introduction

### 1.1 Purpose

The Hostel Management System (HMS) is a Django-based web application designed to digitize and streamline hostel operations at educational institutions. This system replaces manual paper-based processes with an efficient digital solution that can be easily deployed and maintained by university IT staff.

**Key Problems Solved:**
- Eliminates paper-based room allocation processes
- Reduces complaint resolution time through digital tracking
- Centralizes communication between administration and students
- Provides transparent stipend management
- Maintains organized visitor logs for security

### 1.2 Project Scope

**Phase 1 (Core Implementation):**
- Student registration and profile management
- Room allocation and management
- Basic complaint submission and tracking
- Notice board system

**Phase 2 (Enhanced Features):**
- Stipend management system
- Lost and found tracking
- Visitor log management
- Advanced reporting and analytics

**Phase 3 (Future Scalability):**
- Mobile app integration via Django REST API
- Advanced notification systems
- Integration with university databases
- Multi-hostel support

### 1.3 Target Users

**Primary Users:**
- **Students (Main Users):** 200-500 concurrent users
- **Hostel Office Staff:** 5-10 administrative users
- **Provost/Warden:** 1-2 approval authority users

**Secondary Users:**
- **University Administration:** Reporting and oversight
- **Security Personnel:** Visitor management
- **IT Support:** System maintenance

### 1.4 Technology Justification

**Django Framework Benefits:**
- Rapid development with built-in admin interface
- Secure authentication and authorization system
- Scalable architecture for future growth
- Excellent documentation and community support
- Built-in ORM for database management
- Template system eliminating need for separate frontend

### 1.5 System Overview

The HMS provides a centralized web portal accessible through university network or internet, featuring:
- Role-based dashboards for different user types
- Real-time data updates and notifications
- Responsive design for desktop and mobile access
- Automated workflows for common processes
- Comprehensive audit trails for all activities

---

## 2. Overall Description

### 2.1 Product Perspective

The HMS operates as a standalone Django application that can integrate with existing university infrastructure. It's designed to be:

**Self-Contained:** Can function independently without external dependencies
**Scalable:** Architecture supports growth from single hostel to multiple facilities
**Maintainable:** Clean code structure following Django best practices
**Secure:** Implements university-grade security standards

### 2.2 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Web Browser Interface                    │
│                  (Django Templates + CSS)                   │
├─────────────────────────────────────────────────────────────┤
│                     Django Application                      │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│  │   Models    │ │    Views    │ │  Templates  │           │
│  │ (Database)  │ │ (Logic)     │ │ (Frontend)  │           │
│  └─────────────┘ └─────────────┘ └─────────────┘           │
├─────────────────────────────────────────────────────────────┤
│                  Database Layer (SQLite/PostgreSQL)         │
└─────────────────────────────────────────────────────────────┘
```

### 2.3 User Roles and Permissions

**Student Role:**
- View personal profile and room assignment
- Apply for room allocation
- Submit and track complaints
- View notices and announcements
- Access lost and found postings

**Hostel Office Staff:**
- Manage student information
- Process room allocations
- Handle complaint resolution
- Post notices and announcements
- Manage stipend transactions

**Provost/Warden:**
- Approve room allocations
- Oversee complaint resolution
- Access comprehensive reports
- Manage critical system settings

**System Administrator:**
- Full system access via Django admin
- User management and role assignments
- System configuration and maintenance
- Database backup and recovery

### 2.4 Operating Environment

**Server Requirements:**
- Python 3.8+ with Django 4.2+
- SQLite (development) / PostgreSQL (production)
- 2GB RAM minimum, 4GB recommended
- 20GB storage space minimum

**Client Requirements:**
- Modern web browser (Chrome, Firefox, Safari, Edge)
- JavaScript enabled
- Internet connection (for external deployment)
- No additional software installation required

### 2.5 Design Constraints

**Technical Constraints:**
- Must use Django framework and built-in templates
- Single-server deployment for initial version
- Database must support concurrent access
- Session-based authentication (no external OAuth initially)

**Operational Constraints:**
- 24/7 availability during academic year
- Data backup requirements
- User training and support documentation
- Compliance with university data policies

---

## 3. System Features

### 3.1 User Authentication and Authorization

#### 3.1.1 Feature Description
Django's built-in authentication system with custom user profiles and role-based access control.

#### 3.1.2 Functional Requirements

**REQ-AUTH-001:** System shall provide secure login using username/password
- Django's built-in authentication system
- Password strength validation
- Session management with timeout
- Account lockout after failed attempts

**REQ-AUTH-002:** System shall support multiple user roles
- Custom user groups: Student, Staff, Provost, Admin
- Permission-based access control
- Role assignment through Django admin interface

**REQ-AUTH-003:** System shall provide user profile management
- Personal information updates
- Password change functionality
- Profile picture upload (optional)
- Emergency contact information

#### 3.1.3 Technical Implementation
```python
# Django Models Structure
class CustomUser(AbstractUser):
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    phone = models.CharField(max_length=15)
    emergency_contact = models.CharField(max_length=15)
    
class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    academic_year = models.PositiveIntegerField()
```

### 3.2 Student Information Management

#### 3.2.1 Feature Description
Comprehensive student data management with integration capabilities for university databases.

#### 3.2.2 Functional Requirements

**REQ-SIM-001:** System shall maintain student records
- Personal information (name, ID, contact details)
- Academic information (department, year, semester)
- Hostel-related data (room assignment, application history)
- Emergency contact information

**REQ-SIM-002:** System shall provide student verification
- Student ID validation against university database
- Email verification for account activation
- Document upload for verification purposes

**REQ-SIM-003:** System shall display student dashboard
- Current room assignment status
- Recent complaint history
- Unread notices count
- Quick action buttons for common tasks

#### 3.2.3 Implementation Priority
**Phase 1:** Basic student profile management  
**Phase 2:** Advanced verification and document handling  
**Phase 3:** Integration with university systems

### 3.3 Room Management System

#### 3.3.1 Feature Description
Dynamic room allocation system with real-time availability tracking and application processing.

#### 3.3.2 Functional Requirements

**REQ-RM-001:** System shall manage room inventory
- Room number, capacity, and facilities
- Real-time occupancy status
- Room type categorization (single, double, shared)
- Facility details (attached bathroom, AC, furniture)

**REQ-RM-002:** System shall handle room applications
- Student application submission with preferences
- Application queue management
- Automated notification system
- Approval workflow for provost

**REQ-RM-003:** System shall track room allocation
- Current resident information
- Allocation history and transfers
- Vacancy notification system
- Waiting list management

#### 3.3.3 Database Schema
```python
class Room(models.Model):
    room_number = models.CharField(max_length=10, unique=True)
    capacity = models.PositiveIntegerField()
    current_occupancy = models.PositiveIntegerField(default=0)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    facilities = models.JSONField(default=dict)
    
class RoomApplication(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    application_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUS)
    priority_score = models.PositiveIntegerField(default=0)
```

### 3.4 Complaint Management System

#### 3.4.1 Feature Description
Structured complaint handling with status tracking and automated notifications.

#### 3.4.2 Functional Requirements

**REQ-CMS-001:** System shall accept complaint submissions
- Complaint category selection (maintenance, security, facilities)
- Detailed description with optional file attachments
- Priority level assignment
- Location/room specification

**REQ-CMS-002:** System shall track complaint status
- Status progression: Submitted → In Progress → Resolved → Closed
- Automated notifications to student and staff
- Time-based escalation rules
- Staff assignment and workload distribution

**REQ-CMS-003:** System shall provide complaint dashboard
- Student view: Personal complaint history and status
- Staff view: Assigned complaints and workload
- Management view: Overall statistics and performance

#### 3.4.3 Implementation Notes
- Use Django's email backend for notifications
- Implement file upload with size and type restrictions
- Create staff dashboard for complaint management
- Add basic reporting for complaint analytics

### 3.5 Notice Board System

#### 3.5.1 Feature Description
Digital notice board for official communication from hostel administration to students with file attachment support.

#### 3.5.2 Functional Requirements

**REQ-NBS-001:** System shall support notice creation and management
- Rich text editor for notice content
- File attachment support (PDF, images, documents up to 10MB)
- Category classification (General, Important, Urgent, Academic)
- Target audience selection (All students, specific blocks/floors)
- Scheduled posting with expiration dates

**REQ-NBS-002:** System shall provide notice visibility management
- Priority-based highlighting (urgent notices at top)
- Read/unread status tracking
- Email notification for urgent notices
- Archive functionality for expired notices

**REQ-NBS-003:** System shall display notices on student dashboard
- Chronological listing with search functionality
- Category-based filtering
- Attachment download capability
- Mobile-responsive notice viewing

#### 3.5.3 Database Schema
```python
class Notice(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=NOTICE_CATEGORIES)
    priority = models.CharField(max_length=10, choices=PRIORITY_LEVELS)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)

class NoticeAttachment(models.Model):
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE)
    file = models.FileField(upload_to='notices/')
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
```

#### 3.5.4 Implementation Priority
**Phase 1:** Basic notice posting and viewing  
**Phase 2:** File attachments and advanced filtering  
**Phase 3:** Email notifications and advanced targeting

### 3.6 Stipend Management System (Phase 2)

#### 3.6.1 Feature Description
Financial management system for tracking and processing student stipend payments with transaction records.

#### 3.6.2 Functional Requirements

**REQ-SM-001:** System shall manage stipend eligibility
- Student eligibility criteria configuration
- Automatic eligibility calculation based on academic performance
- Manual override capability for special cases
- Stipend amount calculation based on predefined rules

**REQ-SM-002:** System shall process stipend transactions
- Batch processing for multiple students
- Transaction reference number generation
- Payment method tracking (bank transfer, cash, etc.)
- Authorization workflow requiring staff approval

**REQ-SM-003:** System shall maintain transaction records
- Complete transaction history per student
- Monthly and yearly stipend summaries
- Budget tracking and reporting
- Audit trail for all financial activities

#### 3.6.3 Database Schema
```python
class StipendTransaction(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    reference_number = models.CharField(max_length=50, unique=True)
    processed_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    
class StipendEligibility(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    academic_year = models.PositiveIntegerField()
    semester = models.PositiveIntegerField()
    is_eligible = models.BooleanField(default=False)
    eligibility_amount = models.DecimalField(max_digits=10, decimal_places=2)
    criteria_met = models.JSONField(default=dict)
```

### 3.7 Lost and Found System

#### 3.7.1 Feature Description
Community-based system for reporting and tracking lost items within the hostel premises.

#### 3.7.2 Functional Requirements

**REQ-LF-001:** System shall handle lost item reporting
- Item description with category selection
- Location where item was last seen
- Date and time of loss
- Contact information for recovery
- Optional image upload for item identification

**REQ-LF-002:** System shall manage found item posts
- Match found items with existing lost reports
- Public posting for unmatched found items
- Contact facilitation between finder and owner
- Status tracking (Lost, Found, Claimed, Expired)

**REQ-LF-003:** System shall provide search and filtering
- Search by item description and category
- Date range filtering
- Location-based filtering
- Status-based filtering

#### 3.7.3 Database Schema
```python
class LostItem(models.Model):
    reporter = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=ITEM_CATEGORIES)
    lost_location = models.CharField(max_length=100)
    lost_date = models.DateTimeField()
    contact_info = models.CharField(max_length=100)
    image = models.ImageField(upload_to='lost_items/', blank=True)
    status = models.CharField(max_length=20, choices=ITEM_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()  # Auto-expire after 30 days
```

### 3.8 Visitor Log System (Simplified)

#### 3.8.1 Feature Description
Simplified visitor registration and tracking system for basic security management.

#### 3.8.2 Functional Requirements

**REQ-VLS-001:** System shall handle visitor registration
- Visitor name and contact number
- Host student selection
- Visit purpose (Family, Friend, Official)
- Planned visit date and time
- Expected duration of visit

**REQ-VLS-002:** System shall provide daily visitor logs
- Today's expected visitors list
- Check-in/check-out tracking
- Simple visitor status updates
- Basic visitor history per student

**REQ-VLS-003:** System shall support basic security features
- Visitor ID verification requirement
- Automatic visitor expiry after 24 hours
- Simple alert for overdue visitors
- Host notification for visitor arrival

#### 3.8.3 Database Schema
```python
class VisitorLog(models.Model):
    host_student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    visitor_name = models.CharField(max_length=100)
    visitor_phone = models.CharField(max_length=15)
    visit_purpose = models.CharField(max_length=20, choices=VISIT_PURPOSES)
    planned_visit_date = models.DateTimeField()
    expected_duration = models.PositiveIntegerField()  # in hours
    actual_checkin = models.DateTimeField(null=True, blank=True)
    actual_checkout = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=VISITOR_STATUS)
    notes = models.TextField(blank=True)
```

---

## 4. Technical Requirements

### 4.1 Technology Stack

**Backend Framework:**
- Python 3.8+ with Django 4.2+
- Django REST Framework (for future API needs)
- Django Crispy Forms (for better form rendering)
- Pillow (for image handling)
- django-widget-tweaks (for form customization)

**Database:**
- Development: SQLite (included with Django)
- Production: PostgreSQL 12+ or MySQL 8.0+
- Database migration support using Django migrations

**Frontend:**
- Django Templates with Bootstrap 5
- HTML5, CSS3, JavaScript (ES6+)
- Font Awesome for icons
- jQuery for enhanced interactivity

**File Storage:**
- Local file system (development)
- Cloud storage ready (AWS S3, Google Cloud Storage)
- Media files organized by feature modules

### 4.2 System Architecture

**MVC Architecture (Django MVT):**
```
Models (Database Layer)
├── User Management (CustomUser, StudentProfile)
├── Room Management (Room, RoomApplication, RoomAllocation)
├── Complaint System (Complaint, ComplaintStatus)
├── Notice Board (Notice, NoticeAttachment)
├── Stipend Management (StipendTransaction, StipendEligibility)
├── Lost & Found (LostItem, FoundItem)
└── Visitor Log (VisitorLog)

Views (Business Logic Layer)
├── Authentication Views
├── Dashboard Views
├── CRUD Operations Views
├── Report Generation Views
└── API Views (future)

Templates (Presentation Layer)
├── Base Templates (header, footer, navigation)
├── User-specific Dashboards
├── Form Templates
├── Report Templates
└── Mobile-responsive Layouts
```

### 4.3 Database Schema Overview

**Core Tables:**
- auth_user (Django built-in)
- hostel_customuser (extended user model)
- hostel_studentprofile
- hostel_room
- hostel_roomapplication
- hostel_complaint
- hostel_notice
- hostel_stipendtransaction
- hostel_lostitem
- hostel_visitorlog

**Relationship Structure:**
- One-to-One: CustomUser ↔ StudentProfile
- One-to-Many: Room → RoomApplication
- Many-to-Many: Student ↔ Room (through RoomAllocation)
- Foreign Keys: All feature tables → CustomUser

### 4.4 Security Requirements

**Authentication & Authorization:**
- Django's built-in authentication system
- Session-based authentication with CSRF protection
- Role-based permissions using Django groups
- Password validation with complexity requirements

**Data Protection:**
- SQL injection prevention through Django ORM
- XSS protection through template auto-escaping
- CSRF protection for all forms
- File upload validation and size restrictions

**Privacy & Compliance:**
- Personal data encryption for sensitive fields
- Audit trail for all data modifications
- Data retention policies implementation
- GDPR compliance considerations

### 4.5 Performance Requirements

**Response Time:**
- Page load: < 3 seconds on standard connection
- Database queries: < 1 second for standard operations
- File uploads: < 30 seconds for maximum file size
- Search operations: < 2 seconds for complex queries

**Scalability:**
- Support for 500 concurrent users
- Database optimization for 10,000+ records per table
- Efficient pagination for large datasets
- Caching implementation for frequently accessed data

**Availability:**
- 99% uptime during operational hours
- Graceful error handling and user feedback
- Automatic backup scheduling
- Database connection pooling

---

## 5. Implementation Guidelines

### 5.1 Development Phases

**Phase 1 (Core MVP - 4-6 weeks):**
1. User authentication and profile management
2. Basic room management and allocation
3. Simple complaint submission and tracking
4. Basic notice board functionality
5. Admin interface setup

**Phase 2 (Enhanced Features - 3-4 weeks):**
1. File attachment support for notices
2. Advanced complaint management
3. Lost and found system
4. Visitor log system
5. Basic reporting features

**Phase 3 (Advanced Features - 2-3 weeks):**
1. Stipend management system
2. Email notification system
3. Advanced search and filtering
4. Data export capabilities
5. Mobile optimization

### 5.2 Django Project Structure

```
hostel_management/
├── hostel_management/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── authentication/
│   ├── dashboard/
│   ├── rooms/
│   ├── complaints/
│   ├── notices/
│   ├── stipends/
│   ├── lost_found/
│   └── visitors/
├── templates/
│   ├── base/
│   ├── dashboard/
│   ├── rooms/
│   ├── complaints/
│   └── notices/
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── media/
│   ├── notices/
│   ├── lost_items/
│   └── profiles/
├── requirements.txt
├── manage.py
└── README.md
```

### 5.3 Database Configuration

**Development Setup:**
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**Production Setup:**
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hostel_management',
        'USER': 'hostel_user',
        'PASSWORD': 'secure_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5.4 Essential Django Packages

**requirements.txt:**
```txt
Django==4.2.5
django-crispy-forms==2.0
crispy-bootstrap5==0.7
django-widget-tweaks==1.4.12
Pillow==10.0.0
psycopg2-binary==2.9.7  # for PostgreSQL
python-decouple==3.8
django-extensions==3.2.3
reportlab==4.0.4  # for PDF generation
```

### 5.5 Deployment Considerations

**Development Environment:**
- Django development server (manage.py runserver)
- SQLite database for quick setup
- Debug mode enabled for development

**Production Environment:**
- WSGI server (Gunicorn) + Web server (Nginx)
- PostgreSQL/MySQL database
- Static file serving through web server
- SSL certificate for HTTPS
- Environment variable configuration

---

## 6. Future Enhancements

### 6.1 Mobile Application

**Django REST API Development:**
- RESTful API endpoints for all major features
- Token-based authentication for mobile apps
- API documentation using Django REST Swagger
- Rate limiting and API versioning

**Mobile App Features:**
- Native Android/iOS apps or React Native
- Push notifications for important updates
- Offline capability for viewing personal data
- QR code scanning for visitor check-in

### 6.2 Advanced Features

**Integration Capabilities:**
- University student information system integration
- Email server integration for automated notifications
- SMS gateway for urgent alerts
- Payment gateway integration for fee collection

**Analytics and Reporting:**
- Dashboard analytics with charts and graphs
- Automated report generation and scheduling
- Data export in multiple formats (PDF, Excel, CSV)
- Performance metrics and system usage statistics

**Multi-tenancy Support:**
- Multiple hostel management from single installation
- Tenant-specific customization and branding
- Centralized administration with distributed management
- Shared resources and separate data isolation

### 6.3 Scalability Enhancements

**Performance Optimization:**
- Database query optimization and indexing
- Caching implementation (Redis/Memcached)
- CDN integration for static file delivery
- Load balancing for high-traffic scenarios

**Infrastructure Improvements:**
- Docker containerization for easy deployment
- CI/CD pipeline setup for automated testing
- Monitoring and logging system integration
- Backup and disaster recovery automation

---

## 7. Conclusion

This Software Requirements Specification provides a comprehensive roadmap for developing a Django-based Hostel Management System. The phased approach ensures that core functionality can be implemented quickly while allowing for future enhancements and scalability.

The system is designed to be practical for university deployment, maintainable by IT staff, and extensible for future needs. By following Django best practices and implementing proper security measures, this HMS can serve as a reliable solution for hostel management operations.

**Key Success Factors:**
- Start with Phase 1 core features for quick deployment
- Implement proper testing throughout development
- Focus on user experience and intuitive interfaces
- Plan for scalability from the beginning
- Maintain comprehensive documentation

**Next Steps:**
1. Set up development environment and Django project
2. Implement user authentication and basic models
3. Create admin interface for initial data management
4. Develop core features following the phased approach
5. Test thoroughly before production deployment

This SRS serves as a living document that should be updated as development progresses and new requirements emerge.