from datetime import datetime, timedelta
from django.db.models import Sum, Count, Q
from .models import Fee, Student, Complaint, Room, Attendance


class AnalyticsHelper:
    """Helper class for analytics and statistics"""
    
    @staticmethod
    def get_total_revenue():
        """Get total revenue from paid fees"""
        return Fee.objects.filter(status='paid').aggregate(
            total=Sum('amount_paid')
        )['total'] or 0
    
    @staticmethod
    def get_pending_revenue():
        """Get total pending fees"""
        return Fee.objects.filter(
            status__in=['pending', 'overdue']
        ).aggregate(total=Sum('amount'))['total'] or 0
    
    @staticmethod
    def get_student_statistics():
        """Get student related statistics"""
        return {
            'total_students': Student.objects.filter(is_active=True).count(),
            'students_without_room': Student.objects.filter(is_active=True, room__isnull=True).count(),
            'students_with_room': Student.objects.filter(is_active=True, room__isnull=False).count(),
        }
    
    @staticmethod
    def get_room_statistics():
        """Get room related statistics"""
        rooms = Room.objects.all()
        return {
            'total_rooms': rooms.count(),
            'occupied_rooms': rooms.filter(status='occupied').count(),
            'available_rooms': rooms.filter(status='available').count(),
            'maintenance_rooms': rooms.filter(status='maintenance').count(),
            'total_capacity': sum(room.capacity for room in rooms),
            'total_occupied': sum(room.occupied_beds for room in rooms),
        }
    
    @staticmethod
    def get_complaint_statistics():
        """Get complaint related statistics"""
        complaints = Complaint.objects.all()
        return {
            'total_complaints': complaints.count(),
            'pending_complaints': complaints.filter(status='submitted').count(),
            'in_progress_complaints': complaints.filter(status='in_progress').count(),
            'resolved_complaints': complaints.filter(status='resolved').count(),
            'urgent_complaints': complaints.filter(priority='urgent').count(),
        }
    
    @staticmethod
    def get_fee_statistics():
        """Get fee related statistics"""
        fees = Fee.objects.all()
        return {
            'total_fees': fees.count(),
            'paid_fees': fees.filter(status='paid').count(),
            'pending_fees': fees.filter(status='pending').count(),
            'overdue_fees': fees.filter(status='overdue').count(),
            'partially_paid_fees': fees.filter(status='partially_paid').count(),
        }
    
    @staticmethod
    def get_attendance_statistics(days=30):
        """Get attendance statistics for last N days"""
        date_threshold = datetime.now().date() - timedelta(days=days)
        attendance_records = Attendance.objects.filter(date__gte=date_threshold)
        
        total = attendance_records.count()
        present = attendance_records.filter(present=True).count()
        absent = total - present
        
        return {
            'total_records': total,
            'present': present,
            'absent': absent,
            'attendance_percentage': (present / total * 100) if total > 0 else 0,
        }
    
    @staticmethod
    def get_overdue_fees():
        """Get list of overdue fees"""
        today = datetime.now().date()
        return Fee.objects.filter(
            status__in=['pending', 'partially_paid'],
            due_date__lt=today
        ).select_related('student', 'student__user').order_by('-due_date')
    
    @staticmethod
    def get_monthly_revenue(year, month):
        """Get revenue for specific month"""
        fees = Fee.objects.filter(
            status='paid',
            payment_date__year=year,
            payment_date__month=month
        )
        return fees.aggregate(total=Sum('amount_paid'))['total'] or 0
    
    @staticmethod
    def get_student_complaint_count(student_id):
        """Get complaint count for a student"""
        return Complaint.objects.filter(student_id=student_id).count()
    
    @staticmethod
    def get_room_occupancy_rate():
        """Get overall room occupancy rate"""
        rooms = Room.objects.all()
        total_capacity = sum(room.capacity for room in rooms) or 1
        total_occupied = sum(room.occupied_beds for room in rooms)
        
        return (total_occupied / total_capacity * 100) if total_capacity > 0 else 0
    
    @staticmethod
    def get_upcoming_due_dates(days=7):
        """Get fees due in next N days"""
        today = datetime.now().date()
        future_date = today + timedelta(days=days)
        
        return Fee.objects.filter(
            status__in=['pending', 'partially_paid'],
            due_date__range=[today, future_date]
        ).select_related('student', 'student__user').order_by('due_date')
    
    @staticmethod
    def get_complaint_resolution_time():
        """Get average complaint resolution time"""
        resolved = Complaint.objects.filter(status='resolved', resolved_date__isnull=False)
        
        if not resolved.exists():
            return None
        
        total_time = timedelta()
        for complaint in resolved:
            resolution_time = complaint.resolved_date - complaint.submitted_date
            total_time += resolution_time
        
        avg_time = total_time / resolved.count()
        return avg_time


class EmailHelper:
    """Helper class for sending emails"""
    
    @staticmethod
    def send_fee_reminder(student):
        """Send fee reminder email to student"""
        # Placeholder for email functionality
        pass
    
    @staticmethod
    def send_complaint_update(complaint):
        """Send complaint update email"""
        # Placeholder for email functionality
        pass
    
    @staticmethod
    def send_visitor_approval(visitor):
        """Send visitor approval email"""
        # Placeholder for email functionality
        pass


class ReportGenerator:
    """Helper class for generating reports"""
    
    @staticmethod
    def generate_student_report(filters=None):
        """Generate student report with optional filters"""
        students = Student.objects.filter(is_active=True).select_related('user', 'room')
        
        if filters:
            if 'city' in filters:
                students = students.filter(city=filters['city'])
            if 'gender' in filters:
                students = students.filter(gender=filters['gender'])
        
        return students
    
    @staticmethod
    def generate_fee_report(start_date=None, end_date=None):
        """Generate fee report for date range"""
        fees = Fee.objects.select_related('student', 'student__user')
        
        if start_date:
            fees = fees.filter(created_at__gte=start_date)
        if end_date:
            fees = fees.filter(created_at__lte=end_date)
        
        return fees
    
    @staticmethod
    def generate_complaint_report(status=None, priority=None):
        """Generate complaint report with filters"""
        complaints = Complaint.objects.select_related('student', 'student__user', 'technician')
        
        if status:
            complaints = complaints.filter(status=status)
        if priority:
            complaints = complaints.filter(priority=priority)
        
        return complaints
    
    @staticmethod
    def generate_occupancy_report():
        """Generate room occupancy report"""
        rooms = Room.objects.prefetch_related('students').all()
        
        report_data = []
        for room in rooms:
            report_data.append({
                'room_number': room.room_number,
                'floor': room.floor,
                'capacity': room.capacity,
                'occupied': room.occupied_beds,
                'available': room.available_beds,
                'occupancy_rate': (room.occupied_beds / room.capacity * 100) if room.capacity > 0 else 0,
                'students': list(room.students.all())
            })
        
        return report_data


class ValidationHelper:
    """Helper class for validations"""
    
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_phone(phone):
        """Validate phone number"""
        import re
        pattern = r'^[0-9]{10}$'
        return re.match(pattern, phone) is not None
    
    @staticmethod
    def validate_room_capacity(room_id, students_to_add=1):
        """Validate if room has capacity"""
        room = Room.objects.get(id=room_id)
        return room.available_beds >= students_to_add
    
    @staticmethod
    def validate_fee_amount(student_id, month):
        """Validate if fee already exists for student-month"""
        return not Fee.objects.filter(student_id=student_id, month=month).exists()


def get_user_dashboard_data(user):
    """Get dashboard data based on user role"""
    if hasattr(user, 'role'):
        role = user.role.role
        
        if role == 'admin':
            return {
                'students': AnalyticsHelper.get_student_statistics(),
                'rooms': AnalyticsHelper.get_room_statistics(),
                'complaints': AnalyticsHelper.get_complaint_statistics(),
                'fees': AnalyticsHelper.get_fee_statistics(),
                'revenue': {
                    'total': AnalyticsHelper.get_total_revenue(),
                    'pending': AnalyticsHelper.get_pending_revenue(),
                },
                'overdue_fees': AnalyticsHelper.get_overdue_fees()[:10],
            }
        
        elif role == 'student':
            try:
                student = user.student_profile
                return {
                    'student': student,
                    'complaints': Complaint.objects.filter(student=student),
                    'fees': Fee.objects.filter(student=student),
                    'visitors': student.visitors.all(),
                }
            except:
                return {}
        
        elif role == 'technician':
            return {
                'assigned_complaints': Complaint.objects.filter(technician=user),
                'pending_complaints': Complaint.objects.filter(
                    technician=user,
                    status__in=['submitted', 'in_progress']
                ),
            }
    
    return {}
