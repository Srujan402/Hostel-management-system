from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Admin URLs
    path('admin/user-management/', views.user_management, name='user_management'),
    path('admin/user/add/', views.add_user, name='add_user'),
    
    path('admin/students/', views.student_list, name='student_list'),
    path('admin/student/add/', views.add_student, name='add_student'),
    path('admin/student/<int:pk>/edit/', views.edit_student, name='edit_student'),
    
    path('admin/rooms/', views.room_list, name='room_list'),
    path('admin/room/add/', views.add_room, name='add_room'),
    path('admin/room/<int:pk>/allocate/', views.allocate_room, name='allocate_room'),
    
    path('admin/fees/', views.fee_list, name='fee_list'),
    path('admin/fees/generate/', views.generate_fees, name='generate_fees'),
    path('admin/fee/<int:pk>/payment/', views.record_payment, name='record_payment'),
    
    path('admin/complaints/', views.complaint_list, name='complaint_list'),
    path('admin/complaint/<int:pk>/assign/', views.assign_complaint, name='assign_complaint'),
    
    path('admin/reports/', views.reports, name='reports'),
    path('admin/export/students/', views.export_students_csv, name='export_students'),
    path('admin/export/fees/', views.export_fees_csv, name='export_fees'),
    
    # Student URLs
    path('student/profile/', views.student_profile, name='student_profile'),
    path('student/fees/', views.my_fees, name='my_fees'),
    path('student/complaints/', views.my_complaints, name='my_complaints'),
    path('student/complaint/submit/', views.submit_complaint, name='submit_complaint'),
    path('student/visitors/', views.my_visitors, name='my_visitors'),
    path('student/visitor/request/', views.request_visitor, name='request_visitor'),
    
    # Technician URLs
    path('technician/complaints/', views.tech_my_complaints, name='tech_complaints'),
    path('technician/complaint/<int:pk>/update/', views.update_complaint, name='update_complaint'),
    path('reports/students/', views.student_statistics, name='student_statistics'),
    path('reports/finance/', views.financial_report, name='financial_report'),
    
]
