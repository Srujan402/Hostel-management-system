from django.contrib import admin
from .models import (
    UserRole, Student, Room, Fee, Attendance, 
    Complaint, Visitor, RoomAllocation
)


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'created_at']
    list_filter = ['role', 'created_at']


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'floor', 'capacity', 'occupied_beds', 'status', 'rent']
    list_filter = ['status', 'floor']
    search_fields = ['room_number']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['get_name', 'roll_number', 'phone', 'room', 'is_active']
    list_filter = ['is_active', 'gender', 'city']
    search_fields = ['roll_number', 'user__first_name', 'user__last_name']
    
    def get_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_name.short_description = 'Name'


@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ['get_student_name', 'month', 'amount', 'amount_paid', 'status', 'due_date']
    list_filter = ['status', 'month']
    search_fields = ['student__user__first_name', 'student__roll_number']
    
    def get_student_name(self, obj):
        return f"{obj.student.user.first_name} {obj.student.user.last_name}"
    get_student_name.short_description = 'Student'


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['get_student_name', 'date', 'present']
    list_filter = ['present', 'date']
    search_fields = ['student__user__first_name', 'student__roll_number']
    
    def get_student_name(self, obj):
        return f"{obj.student.user.first_name} {obj.student.user.last_name}"
    get_student_name.short_description = 'Student'


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['title', 'get_student_name', 'priority', 'status', 'submitted_date']
    list_filter = ['status', 'priority']
    search_fields = ['title', 'student__user__first_name']
    
    def get_student_name(self, obj):
        return f"{obj.student.user.first_name} {obj.student.user.last_name}"
    get_student_name.short_description = 'Student'


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ['visitor_name', 'get_student_name', 'relationship', 'check_in_date']
    list_filter = ['check_in_date', 'relationship']
    search_fields = ['visitor_name', 'student__user__first_name']
    
    def get_student_name(self, obj):
        return f"{obj.student.user.first_name} {obj.student.user.last_name}"
    get_student_name.short_description = 'Student'


@admin.register(RoomAllocation)
class RoomAllocationAdmin(admin.ModelAdmin):
    list_display = ['get_student_name', 'room', 'allocated_date', 'deallocated_date', 'is_active']
    list_filter = ['is_active', 'allocated_date']
    search_fields = ['student__user__first_name', 'room__room_number']
    
    def get_student_name(self, obj):
        return f"{obj.student.user.first_name} {obj.student.user.last_name}"
    get_student_name.short_description = 'Student'
