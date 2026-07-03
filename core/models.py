from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from datetime import datetime


class UserRole(models.Model):
    """User role management"""
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('student', 'Student'),
        ('technician', 'Technician'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='role')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"


class Room(models.Model):
    """Room model"""
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Under Maintenance'),
    ]
    
    room_number = models.CharField(max_length=50, unique=True)
    floor = models.IntegerField(validators=[MinValueValidator(1)])
    capacity = models.IntegerField(validators=[MinValueValidator(1)])
    occupied_beds = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    rent = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Room {self.room_number}"
    
    @property
    def available_beds(self):
        return self.capacity - self.occupied_beds


class Student(models.Model):
    """Student model"""
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    roll_number = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    guardian_name = models.CharField(max_length=100)
    guardian_phone = models.CharField(max_length=15)
    emergency_contact = models.CharField(max_length=15)
    admission_date = models.DateField(auto_now_add=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.roll_number})"


class Fee(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('online', 'Online'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    month = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
        blank=True,
        null=True
    )

    status = models.CharField(max_length=20)
    due_date = models.DateField()

    def __str__(self):
        return f"{self.student}"


class Attendance(models.Model):
    """Attendance model"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance')
    date = models.DateField()
    present = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('student', 'date')
    
    def __str__(self):
        return f"{self.student} - {self.date}"


class Complaint(models.Model):
    """Complaint model"""
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='complaints')
    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    technician = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_complaints',
        limit_choices_to={'role__role': 'technician'}
    )
    resolution_details = models.TextField(blank=True)
    submitted_date = models.DateTimeField(auto_now_add=True)
    resolved_date = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.student}"


class Visitor(models.Model):
    """Visitor management model"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='visitors')
    visitor_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    relationship = models.CharField(max_length=100)
    id_proof_type = models.CharField(max_length=50)
    id_proof_number = models.CharField(max_length=100)
    purpose = models.CharField(max_length=200)
    check_in_date = models.DateTimeField()
    check_out_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.visitor_name} - {self.student}"


class RoomAllocation(models.Model):
    """Room allocation history"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='room_allocations')
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    allocated_date = models.DateField()
    deallocated_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student} - {self.room}"
