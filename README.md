# BAU Hostel Management System

A comprehensive Django-based web application for managing student hostel operations at Bangladesh Agricultural University (BAU). This system streamlines room allocation, application processing, complaint handling, and administrative tasks for hostel management.

## 🏢 Project Overview

The BAU Hostel Management System is designed to digitize and automate hostel operations, providing different interfaces for students, staff, and administrators. The system handles room applications, allocations, complaints, notices, and provides comprehensive administrative tools.

## 🛠️ Technical Stack

- **Backend**: Django 5.2.4
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Authentication**: Django's built-in authentication with custom user model
- **Admin Interface**: Enhanced Django admin with custom styling
- **Permissions**: Django groups and permissions system

## 📦 Installation & Setup

### Prerequisites

- Python 3.8+ 
- pip (Python package manager)
- Virtual environment (recommended)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/SayefEshan/hostel-management-system
   cd bau_hostel_management
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install django==5.2.4
   ```

4. **Database setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Set up staff permissions and sample data**
   ```bash
   # Set up staff groups and permissions
   python manage.py setup_staff_permissions
   
   # Create sample data for testing (recommended)
   python manage.py seed_data
   
   # Assign staff roles automatically
   python manage.py assign_staff_roles --auto
   ```

7. **Collect static files**
   ```bash
   python manage.py collectstatic --noinput
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - Main application: http://localhost:8000/
   - Admin panel: http://localhost:8000/admin/

## 🔐 Default User Accounts

After running `python manage.py seed_data`, you'll have these test accounts:

### Admin Access
- **Username**: `admin`
- **Password**: `admin123`
- **Role**: System Administrator (Full Access)

### Staff Access
- **Username**: `staff1`
- **Password**: `staff123`
- **Role**: Hostel Staff (Limited Admin Access)

### Student Access
- **Username**: `student1`, `student2`, `student3`, `student4`, `student5`
- **Password**: `student123`
- **Role**: Students (Application and Profile Access)

### Provost Access
- **Username**: `provost1`
- **Password**: `provost123`
- **Role**: Provost (Enhanced Admin Access)

## 📁 Project Structure

```
bau_hostel_management/
├── bau_hostel_management/          # Django project settings
│   ├── settings.py                 # Configuration
│   ├── urls.py                     # URL routing
│   └── wsgi.py                     # WSGI config
├── hostel_management/              # Main Django app
│   ├── models.py                   # Database models
│   ├── views.py                    # Business logic
│   ├── admin.py                    # Admin configuration
│   ├── forms.py                    # Form definitions
│   ├── urls.py                     # App URL patterns
│   ├── management/commands/        # Custom management commands
│   └── templates/                  # HTML templates
├── static/                         # Static files (CSS, JS, images)
├── media/                          # User uploads
├── staticfiles/                    # Collected static files
└── manage.py                       # Django management script
```

## 🚀 Key Management Commands

### Permission Management
```bash
# Set up staff groups and permissions
python manage.py setup_staff_permissions

# Assign roles to users
python manage.py assign_staff_roles --auto              # Auto-assign based on user_type
python manage.py assign_staff_roles --username staff1 --role staff  # Assign specific role
python manage.py assign_staff_roles                     # Interactive mode
```

### Database Operations
```bash
# Create and apply migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Access Django shell
python manage.py shell
```

### Sample Data Management
```bash
# Create comprehensive sample data (recommended for testing)
python manage.py seed_data

# Clear all data and reseed
python manage.py seed_data --clear

# Create only users and profiles (minimal setup)
python manage.py seed_data --users-only

# Alternative: Load from fixtures (static data)
python manage.py loaddata hostel_management/fixtures/sample_data.json
```

### Static Files
```bash
# Collect static files for production
python manage.py collectstatic

# Run development server
python manage.py runserver 0.0.0.0:8000
```

## 🌐 Production Deployment

### Environment Variables
Create a `.env` file for production settings:
```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DATABASE_URL=postgresql://user:password@localhost/dbname
```

### Database Configuration
For production, update `settings.py` to use PostgreSQL:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hostel_management_db',
        'USER': 'hostel_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🔧 Development Guidelines

### Adding New Features
1. Create models in `models.py`
2. Add admin configuration in `admin.py`
3. Create forms in `forms.py`
4. Implement views in `views.py`
5. Add URL patterns in `urls.py`
6. Create templates in `templates/hostel_management/`

### Custom Permissions
Use the management commands to set up role-based permissions:
- Staff permissions are configured in `setup_staff_permissions.py`
- Role assignments use Django's built-in groups and permissions

## 📊 Current System Status

### Implemented Features ✅
- User authentication and authorization
- Room management and allocation
- Application processing workflow
- Complaint handling system
- Notice management
- Staff admin interface with role-based permissions
- Responsive design with modern UI
- Custom Django admin styling

### Planned Improvements 🚧
- Real-time room availability updates
- Email notification system
- Advanced reporting and analytics
- Mobile application API
- Payment integration
- Automated room allocation algorithms
