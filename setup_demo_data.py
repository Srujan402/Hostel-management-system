from django.contrib.auth.models import User
from core.models import UserRole, Student, Room
from datetime import datetime

# Create Admin User
admin = User.objects.create_user(
    username='admin',
    email='admin@hostel.com',
    password='admin123',
    first_name='Admin',
    last_name='User'
)
UserRole.objects.create(user=admin, role='admin')
print("✓ Admin user created (admin/admin123)")

# Create Student User
student_user = User.objects.create_user(
    username='student1',
    email='student1@hostel.com',
    password='student123',
    first_name='John',
    last_name='Doe'
)
UserRole.objects.create(user=student_user, role='student')

# Create Student Profile
student = Student.objects.create(
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
print("✓ Student user created (student1/student123)")

# Create Technician User
tech_user = User.objects.create_user(
    username='technician1',
    email='tech@hostel.com',
    password='tech123',
    first_name='Tech',
    last_name='Support'
)
UserRole.objects.create(user=tech_user, role='technician')
print("✓ Technician user created (technician1/tech123)")

# Create Sample Rooms
rooms_data = [
    {'room_number': '101', 'floor': 1, 'capacity': 2, 'rent': 5000},
    {'room_number': '102', 'floor': 1, 'capacity': 2, 'rent': 5000},
    {'room_number': '103', 'floor': 1, 'capacity': 3, 'rent': 7500},
    {'room_number': '201', 'floor': 2, 'capacity': 2, 'rent': 5500},
    {'room_number': '202', 'floor': 2, 'capacity': 3, 'rent': 8000},
]

for room_data in rooms_data:
    Room.objects.create(**room_data)

print(f"✓ Created {len(rooms_data)} sample rooms")

# Allocate room to student
room = Room.objects.first()
student.room = room
student.save()

room.occupied_beds = 1
room.status = 'available'
room.save()

print("✓ Room allocated to student")

print("\n✓ Demo data created successfully!")
print("\nYou can now login with:")
print("  Admin: admin / admin123")
print("  Student: student1 / student123")
print("  Technician: technician1 / tech123")
