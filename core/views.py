from dateutil.relativedelta import relativedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q, Sum, Count
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from datetime import date, date, datetime, timedelta
import csv
from decimal import Decimal
from .models import (
    UserRole, Student, Room, Fee, Attendance, Complaint, Visitor, RoomAllocation
)


def is_admin(user):
    """Check if user is admin"""
    return hasattr(user, 'role') and user.role.role == 'admin'


def is_student(user):
    """Check if user is student"""
    return hasattr(user, 'role') and user.role.role == 'student'


def is_technician(user):
    """Check if user is technician"""
    return hasattr(user, 'role') and user.role.role == 'technician'


# ==================== Authentication Views ====================

def login_view(request):
    """User login view"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')


def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


@login_required(login_url='login')
def dashboard(request):
    """Dashboard view based on user role"""
    if not hasattr(request.user, 'role'):
        messages.error(request, 'User role not assigned.')
        return redirect('login')
    
    user_role = request.user.role.role
    
    if user_role == 'admin':
        return admin_dashboard(request)
    elif user_role == 'student':
        return student_dashboard(request)
    elif user_role == 'technician':
        return technician_dashboard(request)
    else:
        return redirect('login')


# ==================== Admin Dashboard ====================

@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Admin dashboard with statistics"""
    total_students = Student.objects.filter(is_active=True).count()
    total_rooms = Room.objects.count()
    available_rooms = Room.objects.filter(status='available').count()
    total_complaints = Complaint.objects.count()
    pending_complaints = Complaint.objects.filter(status__in=['submitted', 'in_progress']).count()
    
    # Revenue statistics
    total_revenue = Fee.objects.filter(status='paid').aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    pending_fees = Fee.objects.filter(status__in=['pending', 'overdue']).aggregate(Sum('amount'))['amount__sum'] or 0
    
    context = {
        'total_students': total_students,
        'total_rooms': total_rooms,
        'available_rooms': available_rooms,
        'total_complaints': total_complaints,
        'pending_complaints': pending_complaints,
        'total_revenue': total_revenue,
        'pending_fees': pending_fees,
    }
    
    return render(request, 'admin/dashboard.html', context)


# ==================== User Management ====================

@login_required(login_url='login')
@user_passes_test(is_admin)
def user_management(request):
    """User management list view"""
    users = User.objects.all().select_related('role')
    
    context = {'users': users}
    return render(request, 'admin/user_management.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin)
def add_user(request):
    """Add new user"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        role = request.POST.get('role')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('add_user')
        
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        
        UserRole.objects.create(user=user, role=role)
        messages.success(request, 'User created successfully.')
        return redirect('user_management')
    
    context = {'roles': ['admin', 'student', 'technician']}
    return render(request, 'admin/add_user.html', context)


# ==================== Student Management ====================

@login_required(login_url='login')
@user_passes_test(is_admin)
def student_list(request):
    """List all students"""
    students = Student.objects.filter(is_active=True).select_related('user', 'room')
    search = request.GET.get('search')
    
    if search:
        students = students.filter(
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search) |
            Q(roll_number__icontains=search) |
            Q(user__username__icontains=search)
        )
    
    context = {'students': students, 'search': search}
    return render(request, 'admin/student_list.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin)
def add_student(request):
    """Add new student"""
    if request.method == 'POST':
        dob= request.POST.get('date_of_birth')
        if dob:
            dob_date = datetime.strptime(dob, '%Y-%m-%d').date()
            # 🚨 RULE: must be at least 6 years old
            age = relativedelta(date.today(), dob_date).years
            if age < 6:
                messages.error(request, "Student must be at least 6 years old for admission.")
                return redirect('add_student')
        gender = request.POST.get('gender')
        if not gender:
            messages.error(request, 'Gender is required.')
            return redirect('add_student')
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        roll_number = request.POST.get('roll_number')
        phone = request.POST.get('phone')
        date_of_birth = request.POST.get('date_of_birth')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        guardian_name = request.POST.get('guardian_name')
        guardian_phone = request.POST.get('guardian_phone')
        emergency_contact = request.POST.get('emergency_contact')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('add_student')
        
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        
        UserRole.objects.create(user=user, role='student')
        
        Student.objects.create(
            user=user,
            roll_number=roll_number,
            phone=phone,
            gender=gender,
            date_of_birth=dob,
            address=address,
            city=city,
            state=state,
            pincode=pincode,
            guardian_name=guardian_name,
            guardian_phone=guardian_phone,
            emergency_contact=emergency_contact
        )
        
        messages.success(request, 'Student added successfully.')
        return redirect('student_list')
    
    return render(request, 'admin/add_student.html')


from django.shortcuts import render, redirect, get_object_or_404
from core.models import Student

def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == "POST":
        data = request.POST

        # USER UPDATE
        student.user.first_name = data.get('first_name')
        student.user.last_name = data.get('last_name')
        student.user.email = data.get('email')
        student.user.save()

        # STUDENT UPDATE
        student.roll_number = data.get('roll_number')
        student.phone = data.get('phone')
        student.gender = data.get('gender')
        student.date_of_birth = data.get('date_of_birth')
        student.address = data.get('address')
        student.city = data.get('city')
        student.state = data.get('state')
        student.pincode = data.get('pincode')
        student.guardian_name = data.get('guardian_name')
        student.guardian_phone = data.get('guardian_phone')
        student.emergency_contact = data.get('emergency_contact')

        student.save()

        print("SAVED ROLL:", student.roll_number)  # DEBUG

        return redirect('student_list')

    return render(request, 'admin/edit_student.html', {'student': student})


# ==================== Room Management ====================

@login_required(login_url='login')
@user_passes_test(is_admin)
def room_list(request):
    """List all rooms"""
    rooms = Room.objects.all().prefetch_related('students')
    status_filter = request.GET.get('status')
    
    if status_filter:
        rooms = rooms.filter(status=status_filter)
    
    context = {'rooms': rooms, 'status_filter': status_filter}
    return render(request, 'admin/room_list.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin)
def add_room(request):
    """Add new room"""
    if request.method == 'POST':
        room_number = request.POST.get('room_number')
        floor = request.POST.get('floor')
        capacity = request.POST.get('capacity')
        rent = request.POST.get('rent')
        
        if Room.objects.filter(room_number=room_number).exists():
            messages.error(request, 'Room number already exists.')
            return redirect('add_room')
        
        Room.objects.create(
            room_number=room_number,
            floor=floor,
            capacity=capacity,
            rent=rent
        )
        
        messages.success(request, 'Room added successfully.')
        return redirect('room_list')
    
    return render(request, 'admin/add_room.html')


@login_required(login_url='login')
@user_passes_test(is_admin)
def allocate_room(request, pk):
    """Allocate room to student"""
    room = get_object_or_404(Room, pk=pk)
    students = Student.objects.filter(is_active=True, room__isnull=True)
    
    if request.method == 'POST':
        student_id = request.POST.get('student')
        student = get_object_or_404(Student, pk=student_id)
        
        # Deallocate old room if exists
        if student.room:
            old_room = student.room
            RoomAllocation.objects.filter(student=student, is_active=True).update(
                deallocated_date=datetime.now().date(),
                is_active=False
            )
            old_room.occupied_beds -= 1
            if old_room.occupied_beds == 0:
                old_room.status = 'available'
            old_room.save()
        
        # Allocate new room
        student.room = room
        student.save()
        
        room.occupied_beds += 1
        if room.occupied_beds >= room.capacity:
            room.status = 'occupied'
        else:
            room.status = 'available'
        room.save()
        
        RoomAllocation.objects.create(
            student=student,
            room=room,
            allocated_date=datetime.now().date()
        )
        
        messages.success(request, f'Room allocated to {student} successfully.')
        return redirect('room_list')
    
    context = {'room': room, 'students': students}
    return render(request, 'admin/allocate_room.html', context)


# ==================== Fee Management ====================

@login_required(login_url='login')
@user_passes_test(is_admin)
def fee_list(request):
    """List all fees"""
    fees = Fee.objects.select_related('student', 'student__user')
    status_filter = request.GET.get('status')
    
    if status_filter:
        fees = fees.filter(status=status_filter)
    
    context = {'fees': fees, 'status_filter': status_filter}
    return render(request, 'admin/fee_list.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin)
def generate_fees(request):
    """Generate monthly fees for all students"""
    if request.method == 'POST':
        month = request.POST.get('month')
        
        students = Student.objects.filter(is_active=True, room__isnull=False)
        count = 0
        
        for student in students:
            fee, created = Fee.objects.get_or_create(
                student=student,
                month=month,
                defaults={
                    'amount': student.room.rent,
                    'due_date': datetime.now().date() + timedelta(days=7),
                    'status': 'pending'
                }
            )
            if created:
                count += 1
        
        messages.success(request, f'Fees generated for {count} students.')
        return redirect('fee_list')
    
    context = {}
    return render(request, 'admin/generate_fees.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin)
def record_payment(request, pk):
    """Record fee payment"""
    fee = get_object_or_404(Fee, pk=pk)
    
    if request.method == 'POST':
        amount = Decimal(request.POST.get('amount'))
        
        fee.amount_paid += amount
        
        if fee.amount_paid >= fee.amount:
            fee.status = 'paid'
            fee.payment_date = datetime.now().date()
        elif fee.amount_paid > 0:
            fee.status = 'partially_paid'
        
        fee.save()
        messages.success(request, 'Payment recorded successfully.')
        return redirect('fee_list')
    
    context = {'fee': fee}
    return render(request, 'admin/record_payment.html', context)


# ==================== Complaint Management ====================

@login_required(login_url='login')
@user_passes_test(is_admin)
def complaint_list(request):
    """List all complaints"""
    complaints = Complaint.objects.select_related('student', 'student__user', 'technician')
    status_filter = request.GET.get('status')
    
    if status_filter:
        complaints = complaints.filter(status=status_filter)
    
    context = {'complaints': complaints, 'status_filter': status_filter}
    return render(request, 'admin/complaint_list.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin)
def assign_complaint(request, pk):
    """Assign complaint to technician"""
    complaint = get_object_or_404(Complaint, pk=pk)
    technicians = User.objects.filter(role__role='technician')
    
    if request.method == 'POST':
        technician_id = request.POST.get('technician')
        technician = get_object_or_404(User, pk=technician_id)
        
        complaint.technician = technician
        complaint.status = 'in_progress'
        complaint.save()
        
        messages.success(request, 'Complaint assigned successfully.')
        return redirect('complaint_list')
    
    context = {'complaint': complaint, 'technicians': technicians}
    return render(request, 'admin/assign_complaint.html', context)


# ==================== Student Dashboard ====================

@login_required(login_url='login')
@user_passes_test(is_student)
@login_required
def student_dashboard(request):
    student = Student.objects.get(user=request.user)

    fees = Fee.objects.filter(student=student)

    total_fees = fees.aggregate(
        total=Sum('amount')
    )['total'] or 0

    total_paid = fees.aggregate(
        total=Sum('amount_paid')
    )['total'] or 0

    total_remaining = fees.aggregate(
        total=Sum('remaining_amount')
    )['total'] or 0

    context = {
        'student': student,
        'fees': fees,
        'total_fees': total_fees,
        'total_paid': total_paid,
        'total_remaining': total_remaining,
    }

    return render(
        request,
        'student/dashboard.html',
        context
    )

@login_required(login_url='login')
@user_passes_test(is_student)
def student_profile(request):
    """Student profile view"""
    student = request.user.student_profile
    
    if request.method == 'POST':
        student.phone = request.POST.get('phone')
        student.address = request.POST.get('address')
        student.city = request.POST.get('city')
        student.state = request.POST.get('state')
        student.pincode = request.POST.get('pincode')
        student.emergency_contact = request.POST.get('emergency_contact')
        student.save()
        
        messages.success(request, 'Profile updated successfully.')
    
    context = {'student': student}
    return render(request, 'student/profile.html', context)


@login_required(login_url='login')
@user_passes_test(is_student)
def my_fees(request):
    student = Student.objects.get(user=request.user)

    fees = Fee.objects.filter(student=student).order_by('-due_date')

    total_amount = sum(f.amount for f in fees)
    total_paid = sum(f.amount_paid for f in fees)
    total_remaining = sum(f.remaining_amount for f in fees)

    context = {
        'student': student,
        'fees': fees,
        'total_amount': total_amount,
        'total_paid': total_paid,
        'total_remaining': total_remaining,
    }

    return render(
        request,
        'student/my_fees.html',
        context
    )


@login_required(login_url='login')
@user_passes_test(is_student)
def my_complaints(request):
    """Student complaints"""
    student = request.user.student_profile
    complaints = student.complaints.all().order_by('-submitted_date')
    
    context = {'complaints': complaints}
    return render(request, 'student/my_complaints.html', context)


@login_required(login_url='login')
@user_passes_test(is_student)
def submit_complaint(request):
    """Submit new complaint"""
    if request.method == 'POST':
        student = request.user.student_profile
        
        complaint = Complaint.objects.create(
            student=student,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            priority=request.POST.get('priority', 'medium')
        )
        
        messages.success(request, 'Complaint submitted successfully.')
        return redirect('my_complaints')
    
    return render(request, 'student/submit_complaint.html')


@login_required(login_url='login')
@user_passes_test(is_student)
def my_visitors(request):
    """Student visitor management"""
    student = request.user.student_profile
    visitors = student.visitors.all().order_by('-check_in_date')
    
    context = {'visitors': visitors}
    return render(request, 'student/my_visitors.html', context)


@login_required(login_url='login')
@user_passes_test(is_student)
def request_visitor(request):
    """Request visitor entry"""
    if request.method == 'POST':
        student = request.user.student_profile
        
        visitor = Visitor.objects.create(
            student=student,
            visitor_name=request.POST.get('visitor_name'),
            phone=request.POST.get('phone'),
            relationship=request.POST.get('relationship'),
            id_proof_type=request.POST.get('id_proof_type'),
            id_proof_number=request.POST.get('id_proof_number'),
            purpose=request.POST.get('purpose'),
            check_in_date=request.POST.get('check_in_date')
        )
        
        messages.success(request, 'Visitor entry recorded successfully.')
        return redirect('my_visitors')
    
    return render(request, 'student/request_visitor.html')


# ==================== Technician Dashboard ====================

@login_required(login_url='login')
@user_passes_test(is_technician)
def technician_dashboard(request):
    """Technician dashboard"""
    assigned_complaints = Complaint.objects.filter(technician=request.user)
    pending_complaints = assigned_complaints.filter(status__in=['submitted', 'in_progress']).count()
    resolved_complaints = assigned_complaints.filter(status='resolved').count()
    
    context = {
        'total_assigned': assigned_complaints.count(),
        'pending_complaints': pending_complaints,
        'resolved_complaints': resolved_complaints,
    }
    
    return render(request, 'technician/dashboard.html', context)


@login_required(login_url='login')
@user_passes_test(is_technician)
def tech_my_complaints(request):
    """Technician assigned complaints"""
    complaints = Complaint.objects.filter(technician=request.user).order_by('-submitted_date')
    
    context = {'complaints': complaints}
    return render(request, 'technician/my_complaints.html', context)


@login_required(login_url='login')
@user_passes_test(is_technician)
def update_complaint(request, pk):
    """Update complaint status"""
    complaint = get_object_or_404(Complaint, pk=pk, technician=request.user)
    
    if request.method == 'POST':
        complaint.status = request.POST.get('status')
        complaint.resolution_details = request.POST.get('resolution_details')
        
        if complaint.status == 'resolved':
            complaint.resolved_date = datetime.now()
        
        complaint.save()
        messages.success(request, 'Complaint updated successfully.')
        return redirect('my_complaints')
    
    context = {'complaint': complaint}
    return render(request, 'technician/update_complaint.html', context)


# ==================== Reports ====================

@login_required(login_url='login')
@user_passes_test(is_admin)
def reports(request):
    """Reports view"""
    context = {}
    return render(request, 'admin/reports.html', context)


@login_required(login_url='login')
@user_passes_test(is_admin)
def export_students_csv(request):
    """Export students to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Roll Number', 'Name', 'Email', 'Phone', 'Room', 'City', 'State'])
    
    students = Student.objects.filter(is_active=True).select_related('user', 'room')
    for student in students:
        writer.writerow([
            student.roll_number,
            f"{student.user.first_name} {student.user.last_name}",
            student.user.email,
            student.phone,
            student.room.room_number if student.room else 'Not Allocated',
            student.city,
            student.state,
        ])
    
    return response


@login_required(login_url='login')
@user_passes_test(is_admin)
def export_fees_csv(request):
    """Export fees to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="fees.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Student', 'Month', 'Amount', 'Paid', 'Status', 'Due Date'])
    
    fees = Fee.objects.select_related('student', 'student__user')
    for fee in fees:
        writer.writerow([
            f"{fee.student.user.first_name} {fee.student.user.last_name}",
            fee.month,
            fee.amount,
            fee.amount_paid,
            fee.status,
            fee.due_date,
        ])
    
    return response
def student_statistics(request):
    total_students = Student.objects.count()
    active_students = Student.objects.filter(is_active=True).count()

    context = {
        'total_students': total_students,
        'active_students': active_students,
    }
    return render(request, 'admin/student_statistics.html', context)


def financial_report(request):
    total_fees = Fee.objects.count()
    total_collected = Fee.objects.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0

    context = {
        'total_fees': total_fees,
        'total_collected': total_collected,
    }
    return render(request, 'admin/financial_report.html', context)
@login_required
def record_payment(request, pk):

    fee = get_object_or_404(Fee, pk=pk)

    # Calculate remaining dynamically
    remaining = fee.amount - fee.amount_paid

    if remaining < 0:
        remaining = Decimal("0")

    if request.method == "POST":

        payment_amount = request.POST.get(
            "payment_amount"
        )

        payment_method = request.POST.get(
            "payment_method"
        )

        # Validate amount
        if not payment_amount:

            messages.error(
                request,
                "Enter payment amount"
            )

            return render(
                request,
                "admin/record_payment.html",
                {
                    "fee": fee,
                    "remaining": remaining
                }
            )

        payment = Decimal(payment_amount)

        if payment <= 0:

            messages.error(
                request,
                "Amount must be greater than 0"
            )

            return render(
                request,
                "admin/record_payment.html",
                {
                    "fee": fee,
                    "remaining": remaining
                }
            )

        if payment > remaining:

            messages.error(
                request,
                f"Maximum allowed is ₹{remaining}"
            )

            return render(
                request,
                "admin/record_payment.html",
                {
                    "fee": fee,
                    "remaining": remaining
                }
            )

        # Save payment
        fee.amount_paid += payment

        fee.remaining_amount = (
            fee.amount -
            fee.amount_paid
        )

        # Save Cash / Online
        if payment_method:
            fee.payment_method = (
                payment_method.lower()
            )

        # Update status
        if fee.amount_paid >= fee.amount:

            fee.status = "paid"

            fee.remaining_amount = Decimal(
                "0"
            )

        elif fee.amount_paid > 0:

            fee.status = (
                "partially_paid"
            )

        else:

            fee.status = (
                "pending"
            )

        fee.save()

        messages.success(
            request,
            "Payment recorded successfully"
        )

        return redirect(
            "fee_list"
        )

    return render(
        request,
        "admin/record_payment.html",
        {
            "fee": fee,
            "remaining": remaining
        }
    )