#!/usr/bin/env python
"""
Hostel Management System - Automatic Database Setup Script
Run this script to automatically fix all database errors
Usage: python auto_setup.py
"""

import os
import sys
import django
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hostel_config.settings')
django.setup()

# Now we can import Django modules
from django.core.management import call_command
from django.contrib.auth.models import User
from core.models import UserRole, Student, Room

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 50)
    print(f"  {title}")
    print("=" * 50)

def setup_database():
    """Run all database setup steps"""
    
    print_section("HOSTEL MANAGEMENT SYSTEM - SETUP")
    
    # Step 1: Run Migrations
    print_section("Step 1: Running Database Migrations")
    print("Creating database tables...")
    try:
        call_command('migrate', verbosity=1)
        print("✓ Migrations completed successfully!")
    except Exception as e:
        print(f"✗ Migration failed: {e}")
        return False
    
    # Step 2: Create Sample Rooms
    print_section("Step 2: Creating Sample Rooms")
    try:
        rooms_data = [
            {'room_number': '101', 'floor': 1, 'capacity': 2, 'rent': 5000},
            {'room_number': '102', 'floor': 1, 'capacity': 2, 'rent': 5000},
            {'room_number': '103', 'floor': 1, 'capacity': 3, 'rent': 7500},
            {'room_number': '201', 'floor': 2, 'capacity': 2, 'rent': 5500},
            {'room_number': '202', 'floor': 2, 'capacity': 3, 'rent': 8000},
        ]
        
        for room_data in rooms_data:
            room, created = Room.objects.get_or_create(
                room_number=room_data['room_number'],
                defaults=room_data
            )
            if created:
                print(f"  ✓ Created room: {room.room_number}")
        
        print(f"✓ Total rooms: {Room.objects.count()}")
    except Exception as e:
        print(f"✗ Room creation failed: {e}")
        return False
    
    # Step 3: Create Admin User
    print_section("Step 3: Creating Admin User")
    try:
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@hostel.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            print("  ✓ Created admin user: admin")
        else:
            print("  ℹ Admin user already exists")
        
        # Create role
        role, created = UserRole.objects.get_or_create(
            user=admin_user,
            defaults={'role': 'admin'}
        )
        
        print("✓ Admin user ready (admin/admin123)")
    except Exception as e:
        print(f"✗ Admin user creation failed: {e}")
        return False
    
    # Step 4: Create Student User
    print_section("Step 4: Creating Student User")
    try:
        student_user, created = User.objects.get_or_create(
            username='student1',
            defaults={
                'email': 'student1@hostel.com',
                'first_name': 'John',
                'last_name': 'Doe',
            }
        )
        
        if created:
            student_user.set_password('student123')
            student_user.save()
            print("  ✓ Created student user: student1")
        else:
            print("  ℹ Student user already exists")
        
        # Create role
        role, created = UserRole.objects.get_or_create(
            user=student_user,
            defaults={'role': 'student'}
        )
        
        # Create student profile
        if not hasattr(student_user, 'student_profile'):
            from datetime import datetime
            Student.objects.create(
                user=student_user,
                roll_number='STU001',
                phone='9876543210',
                gender='M',
                date_of_birth='2002-05-15',
                address='123 Main Street',
                city='Bengaluru',
                state='Karnataka',
                pincode='560001',
                guardian_name='Mr. Ramesh Doe',
                guardian_phone='9876543211',
                emergency_contact='9876543212'
            )
            print("  ✓ Created student profile")
        
        print("✓ Student user ready (student1/student123)")
    except Exception as e:
        print(f"✗ Student user creation failed: {e}")
        return False
    
    # Step 5: Create Technician User
    print_section("Step 5: Creating Technician User")
    try:
        tech_user, created = User.objects.get_or_create(
            username='technician1',
            defaults={
                'email': 'technician1@hostel.com',
                'first_name': 'Tech',
                'last_name': 'Support',
            }
        )
        
        if created:
            tech_user.set_password('tech123')
            tech_user.save()
            print("  ✓ Created technician user: technician1")
        else:
            print("  ℹ Technician user already exists")
        
        # Create role
        role, created = UserRole.objects.get_or_create(
            user=tech_user,
            defaults={'role': 'technician'}
        )
        
        print("✓ Technician user ready (technician1/tech123)")
    except Exception as e:
        print(f"✗ Technician user creation failed: {e}")
        return False
    
    # Success!
    print_section("SETUP COMPLETE!")
    print("""
✓ Database initialized successfully!
✓ All tables created
✓ Sample users created
✓ Sample rooms created

LOGIN CREDENTIALS:
  Admin:      admin / admin123
  Student:    student1 / student123
  Technician: technician1 / tech123

NEXT STEPS:
  1. Start the server: python manage.py runserver
  2. Open browser: http://localhost:8000
  3. Login with above credentials
  4. Start using the system!

TROUBLESHOOTING:
  If you see any errors above, please check:
  1. Virtual environment is activated
  2. All dependencies are installed: pip install -r requirements.txt
  3. You're in the correct directory
    """)
    
    return True

if __name__ == '__main__':
    try:
        success = setup_database()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
