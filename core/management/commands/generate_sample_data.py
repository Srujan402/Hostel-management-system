from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import UserRole, Student, Room, Fee, Complaint, Visitor
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Generate sample data for hostel management system'

    def add_arguments(self, parser):
        parser.add_argument('--students', type=int, default=20, help='Number of students to create')
        parser.add_argument('--rooms', type=int, default=10, help='Number of rooms to create')

    def handle(self, *args, **options):
        num_students = options['students']
        num_rooms = options['rooms']

        self.stdout.write('Generating sample data...')

        # Create rooms
        rooms = []
        for i in range(num_rooms):
            room = Room.objects.create(
                room_number=f'{(i//5)+1}{(i%5)+1:02d}',
                floor=(i // 5) + 1,
                capacity=random.choice([2, 3]),
                rent=random.choice([5000, 5500, 6000, 6500, 7000, 7500, 8000])
            )
            rooms.append(room)
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {num_rooms} rooms'))

        # Create students
        first_names = ['Rajesh', 'Priya', 'Arjun', 'Sneha', 'Vikram', 'Isha', 'Amir', 'Neha', 'Rohan', 'Divya']
        last_names = ['Kumar', 'Singh', 'Patel', 'Sharma', 'Gupta', 'Khan', 'Verma', 'Nair', 'Rao', 'Joshi']
        cities = ['Bangalore', 'Delhi', 'Mumbai', 'Chennai', 'Hyderabad', 'Pune', 'Kolkata', 'Kochi']

        for i in range(num_students):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            username = f'student{i+1:03d}'
            email = f'{username}@hostel.com'
            
            user = User.objects.create_user(
                username=username,
                email=email,
                password='password123',
                first_name=first_name,
                last_name=last_name
            )
            
            UserRole.objects.create(user=user, role='student')
            
            student = Student.objects.create(
                user=user,
                roll_number=f'STU{i+1:04d}',
                phone=f'98{random.randint(100000000, 999999999):09d}',
                gender=random.choice(['M', 'F', 'O']),
                date_of_birth=datetime.now().date() - timedelta(days=random.randint(6570, 7300)),
                address=f'{random.randint(1, 999)} Main Street',
                city=random.choice(cities),
                state='Any',
                pincode=f'{random.randint(100000, 999999)}',
                guardian_name=f'{random.choice(first_names)} {random.choice(last_names)}',
                guardian_phone=f'98{random.randint(100000000, 999999999):09d}',
                emergency_contact=f'98{random.randint(100000000, 999999999):09d}'
            )
            
            # Allocate room
            room = random.choice(rooms)
            if room.available_beds > 0:
                student.room = room
                student.save()
                room.occupied_beds += 1
                if room.occupied_beds >= room.capacity:
                    room.status = 'occupied'
                room.save()
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {num_students} students'))

        # Create fees
        months = ['January 2024', 'February 2024', 'March 2024', 'April 2024']
        students = Student.objects.filter(is_active=True)
        
        for student in students:
            for month in months:
                if student.room:
                    Fee.objects.get_or_create(
                        student=student,
                        month=month,
                        defaults={
                            'amount': student.room.rent,
                            'due_date': datetime.now().date() + timedelta(days=7),
                            'status': random.choice(['pending', 'paid', 'overdue']),
                            'amount_paid': student.room.rent if random.random() > 0.5 else 0
                        }
                    )
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created fees for students'))

        # Create complaints
        complaint_titles = [
            'Water problem in room',
            'Broken furniture',
            'Electrical issue',
            'Cleaning needed',
            'Noise complaint',
            'Maintenance issue',
            'Hygienic concern'
        ]
        
        for student in students[:int(num_students * 0.3)]:
            for _ in range(random.randint(1, 3)):
                Complaint.objects.create(
                    student=student,
                    title=random.choice(complaint_titles),
                    description='Sample complaint description',
                    priority=random.choice(['low', 'medium', 'high']),
                    status=random.choice(['submitted', 'in_progress', 'resolved'])
                )
        
        self.stdout.write(self.style.SUCCESS('✓ Created complaints'))

        self.stdout.write(self.style.SUCCESS('\n✓ Sample data generation completed successfully!'))
