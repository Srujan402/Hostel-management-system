# Hostel Management System

A comprehensive web-based Hostel Management System built with Python, Django, and SQLite. This system automates and streamlines hostel operations including student management, room allocation, fee management, complaint handling, and visitor tracking.

## Features

### Admin Module
- **User Management**: Create and manage users with different roles (Admin, Student, Technician)
- **Student Management**: Add, update, and delete student records
- **Room Management**: Create rooms, define capacity, allocate and deallocate rooms
- **Fee Management**: Generate monthly fees, track payments, view payment history
- **Attendance Monitoring**: View and manage student attendance records
- **Complaint Management**: View complaints, assign to technicians, track resolution status
- **Visitor Management**: Monitor visitor logs and hostel security
- **Reports**: Generate and export reports (students, rooms, fees, attendance)

### Student Module
- **Profile Management**: View and update personal information
- **Room Details**: View allocated room information
- **Fee Management**: View fee details, payment status, and make payments
- **Attendance**: View personal attendance records
- **Complaint Management**: Submit complaints and track status
- **Visitor Entry**: Request and record visitor details

### Technician Module
- **Login & Profile**: Secure login and profile management
- **Complaint Handling**: View assigned complaints, update status and add resolution details
- **Work Tracking**: Maintain history of completed tasks

## System Requirements

### Minimum Requirements
- Operating System: Windows 10 or above / Linux / macOS
- RAM: 4GB
- Hard Disk: 20GB
- Python: 3.8 or above

### Hardware Used
- Processor: i3 or above
- RAM: 8GB or above
- Hard Disk: 512GB
- Monitor, Keyboard, Mouse

## Technology Stack
- **Frontend**: HTML, CSS, Bootstrap 5
- **Backend**: Python (Django 4.2)
- **Database**: SQLite
- **Tools**: Django ORM, Django Admin

## Installation Guide

### Step 1: Clone or Extract Project
```bash
# If you have the zip file, extract it to a directory
unzip hostel_management_system.zip
cd hostel_management_system
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Create Database
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Superuser (Admin)
```bash
python manage.py createsuperuser
# Follow the prompts to create an admin account
```

### Step 6: Create Demo Data
```bash
python manage.py shell

# Run the following commands in the Django shell
from django.contrib.auth.models import User
from core.models import UserRole, Student, Room, Fee, Complaint
from datetime import datetime

# Create demo accounts
# Admin account
admin = User.objects.create_user(
    username='admin',
    email='admin@hostel.com',
    password='admin123',
    first_name='Admin',
    last_name='User'
)
UserRole.objects.create(user=admin, role='admin')

# Student account
student_user = User.objects.create_user(
    username='student1',
    email='student1@hostel.com',
    password='student123',
    first_name='John',
    last_name='Doe'
)
UserRole.objects.create(user=student_user, role='student')

# Technician account
tech_user = User.objects.create_user(
    username='technician1',
    email='tech@hostel.com',
    password='tech123',
    first_name='Tech',
    last_name='Support'
)
UserRole.objects.create(user=tech_user, role='technician')

# Create a sample room
Room.objects.create(
    room_number='101',
    floor=1,
    capacity=2,
    rent=5000
)

exit()
```

### Step 7: Run Development Server
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

## Default Login Credentials

### Admin Account
- Username: `admin`
- Password: `admin123`
- Access: Full system access

### Student Account
- Username: `student1`
- Password: `student123`
- Access: Student portal features

### Technician Account
- Username: `technician1`
- Password: `tech123`
- Access: Complaint management

## Project Structure

```
hostel_management_system/
├── manage.py                      # Django management script
├── requirements.txt               # Python dependencies
├── db.sqlite3                     # SQLite database
├── hostel_config/                 # Main project configuration
│   ├── settings.py               # Django settings
│   ├── urls.py                   # URL routing
│   ├── wsgi.py                   # WSGI configuration
│   └── __init__.py
├── core/                          # Main app
│   ├── models.py                 # Database models
│   ├── views.py                  # View functions
│   ├── urls.py                   # App URL routing
│   ├── admin.py                  # Django admin configuration
│   ├── apps.py                   # App configuration
│   └── __init__.py
├── templates/                     # HTML templates
│   ├── base.html                 # Base template
│   ├── login.html                # Login page
│   ├── admin/                    # Admin templates
│   │   ├── dashboard.html
│   │   ├── student_list.html
│   │   ├── room_list.html
│   │   └── ...
│   ├── student/                  # Student templates
│   │   ├── dashboard.html
│   │   ├── my_fees.html
│   │   └── ...
│   └── technician/               # Technician templates
│       ├── dashboard.html
│       └── ...
└── static/                        # Static files (CSS, JS, images)
```

## Key Models

### UserRole
Manages user roles (Admin, Student, Technician)

### Student
Stores student information including personal details, contact info, and room allocation

### Room
Manages hostel rooms with capacity, occupancy, and rental information

### Fee
Tracks student fees, payments, and payment status

### Attendance
Records student attendance

### Complaint
Manages student complaints and issue resolution

### Visitor
Tracks visitor logs and hostel security

### RoomAllocation
Maintains history of room allocations for students

## Main Views and URLs

### Authentication
- `/` - Login page
- `/logout/` - Logout

### Admin URLs
- `/dashboard/` - Admin dashboard
- `/admin/students/` - Student list
- `/admin/student/add/` - Add new student
- `/admin/rooms/` - Room list
- `/admin/room/add/` - Add new room
- `/admin/fees/` - Fee management
- `/admin/complaints/` - Complaint management
- `/admin/reports/` - Reports

### Student URLs
- `/student/profile/` - Student profile
- `/student/fees/` - View fees
- `/student/complaints/` - View complaints
- `/student/visitor/request/` - Request visitor

### Technician URLs
- `/technician/complaints/` - View assigned complaints
- `/technician/complaint/<id>/update/` - Update complaint status

## Features Implemented

✅ User authentication and role-based access control
✅ Student profile management
✅ Room allocation and management
✅ Fee generation and tracking
✅ Complaint submission and resolution tracking
✅ Visitor management
✅ Attendance tracking
✅ Report generation and export
✅ Admin dashboard with statistics
✅ Student dashboard
✅ Technician complaint management
✅ CSV export for data
✅ Real-time room availability tracking
✅ Payment status tracking

## How to Use

### For Administrators
1. Login with admin credentials
2. Navigate to Students to add and manage student records
3. Navigate to Rooms to create and allocate rooms
4. Generate monthly fees for students
5. Track and manage complaints
6. Generate reports and export data

### For Students
1. Login with student credentials
2. View and update personal profile
3. Check allocated room and details
4. View fees and payment status
5. Submit complaints
6. Request visitor entry

### For Technicians
1. Login with technician credentials
2. View assigned complaints
3. Update complaint status
4. Add resolution details
5. Track completed work

## Security Features
- User authentication with password hashing
- Role-based access control (RBAC)
- CSRF protection
- SQL injection prevention through ORM
- Secure session management

## Future Enhancements
- Email notifications for fee reminders
- SMS alerts for important announcements
- Online payment integration
- Mobile application
- Advanced reporting and analytics
- Biometric attendance system
- QR code based visitor management
- Document management system

## Troubleshooting

### Port 8000 already in use
```bash
python manage.py runserver 8001
```

### Database errors
```bash
python manage.py migrate --run-syncdb
```

### Create fresh database
```bash
# Delete db.sqlite3
# Run migrations again
python manage.py makemigrations
python manage.py migrate
```

## Support
For issues or questions, please contact the system administrator or check the Django documentation at https://docs.djangoproject.com/

## License
This project is provided as-is for educational and institutional use.

## Version
Version 1.0 - Initial Release

---

**Developed by**: Hostel Management System Team
**Institution**: Vivekanand Institute of Management, Kalaburagi
**Date**: 2024
