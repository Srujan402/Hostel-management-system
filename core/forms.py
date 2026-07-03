from django import forms
from django.contrib.auth.models import User
from core.models import Student, Room, Fee, Attendance, Complaint, Visitor


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'roll_number', 'phone', 'gender', 'date_of_birth',
            'address', 'city', 'state', 'pincode',
            'guardian_name', 'guardian_phone', 'emergency_contact'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number', 'floor', 'capacity', 'rent']
        widgets = {
            'rent': forms.NumberInput(attrs={'step': '0.01'}),
        }


class FeeForm(forms.ModelForm):
    class Meta:
        model = Fee
        fields = ['student', 'amount', 'due_date', 'month', 'notes']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'date', 'present', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['title', 'description', 'priority']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class ComplaintUpdateForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['status', 'resolution_details']
        widgets = {
            'resolution_details': forms.Textarea(attrs={'rows': 4}),
        }


class VisitorForm(forms.ModelForm):
    class Meta:
        model = Visitor
        fields = [
            'visitor_name', 'phone', 'relationship',
            'id_proof_type', 'id_proof_number', 'purpose', 'check_in_date'
        ]
        widgets = {
            'check_in_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class PaymentForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0,
        widget=forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'Enter payment amount'})
    )
    payment_method = forms.ChoiceField(
        choices=[
            ('cash', 'Cash'),
            ('cheque', 'Cheque'),
            ('online', 'Online Transfer'),
            ('upi', 'UPI'),
        ],
        widget=forms.RadioSelect
    )
    notes = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2}),
        required=False
    )


class StudentSearchForm(forms.Form):
    search_query = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search by name, roll number, email...',
            'class': 'form-control'
        }),
        required=False
    )
    gender = forms.ChoiceField(
        choices=[('', 'All Genders'), ('M', 'Male'), ('F', 'Female'), ('O', 'Other')],
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    city = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Filter by city...',
            'class': 'form-control'
        }),
        required=False
    )


class FeeSearchForm(forms.Form):
    month = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'placeholder': 'Filter by month...',
            'class': 'form-control'
        }),
        required=False
    )
    status = forms.ChoiceField(
        choices=[
            ('', 'All Status'),
            ('pending', 'Pending'),
            ('paid', 'Paid'),
            ('overdue', 'Overdue'),
            ('partially_paid', 'Partially Paid'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )


class DateRangeForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
