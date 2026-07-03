# Hostel Management System - API Documentation

## Overview
This document provides comprehensive API documentation for the Hostel Management System. The system provides both web interface and API endpoints for accessing functionality.

## Base URL
```
http://localhost:8000/api/
```

## Authentication
The system uses Django's session-based authentication. Ensure you are logged in before accessing protected endpoints.

## Response Format
All responses are in JSON format.

### Success Response
```json
{
    "status": "success",
    "message": "Operation completed successfully",
    "data": {
        // Response data here
    }
}
```

### Error Response
```json
{
    "status": "error",
    "message": "Error description",
    "errors": {
        // Field-specific errors
    }
}
```

---

## Endpoints

### Authentication

#### Login
```
POST /api/auth/login/
Content-Type: application/json

{
    "username": "admin",
    "password": "password123"
}

Response:
{
    "status": "success",
    "token": "user_session_token",
    "user": {
        "id": 1,
        "username": "admin",
        "email": "admin@hostel.com",
        "role": "admin"
    }
}
```

#### Logout
```
POST /api/auth/logout/

Response:
{
    "status": "success",
    "message": "Logged out successfully"
}
```

#### Get Current User
```
GET /api/auth/user/

Response:
{
    "status": "success",
    "data": {
        "id": 1,
        "username": "admin",
        "first_name": "Admin",
        "last_name": "User",
        "email": "admin@hostel.com",
        "role": "admin"
    }
}
```

---

### Students

#### List All Students
```
GET /api/students/
Query Parameters:
  - search: Filter by name or roll number
  - gender: Filter by gender (M/F/O)
  - city: Filter by city
  - page: Page number for pagination

Response:
{
    "status": "success",
    "count": 50,
    "next": "/api/students/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "user": {
                "id": 1,
                "first_name": "John",
                "last_name": "Doe",
                "email": "john@hostel.com",
                "username": "student1"
            },
            "roll_number": "STU001",
            "phone": "9876543210",
            "gender": "M",
            "date_of_birth": "2002-05-15",
            "city": "Bangalore",
            "state": "Karnataka",
            "pincode": "560001",
            "room": {
                "id": 1,
                "room_number": "101",
                "floor": 1
            },
            "is_active": true
        }
    ]
}
```

#### Get Student Details
```
GET /api/students/{id}/

Response:
{
    "status": "success",
    "data": {
        "id": 1,
        "user": {...},
        "roll_number": "STU001",
        // ... all student fields
        "complaints": [...],
        "fees": [...],
        "attendance": [...]
    }
}
```

#### Create Student
```
POST /api/students/
Content-Type: application/json

{
    "user": {
        "username": "student1",
        "email": "student1@hostel.com",
        "first_name": "John",
        "last_name": "Doe",
        "password": "password123"
    },
    "roll_number": "STU001",
    "phone": "9876543210",
    "gender": "M",
    "date_of_birth": "2002-05-15",
    "address": "123 Main Street",
    "city": "Bangalore",
    "state": "Karnataka",
    "pincode": "560001",
    "guardian_name": "Mr. Ramesh Doe",
    "guardian_phone": "9876543211"
}

Response: 201 Created
{
    "status": "success",
    "message": "Student created successfully",
    "data": {
        "id": 1,
        // ... student data
    }
}
```

#### Update Student
```
PUT /api/students/{id}/
Content-Type: application/json

{
    "phone": "9876543210",
    "address": "123 Main Street"
}

Response: 200 OK
```

#### Delete Student
```
DELETE /api/students/{id}/

Response: 204 No Content
```

---

### Rooms

#### List All Rooms
```
GET /api/rooms/
Query Parameters:
  - status: Filter by status (available/occupied/maintenance)
  - floor: Filter by floor number

Response:
{
    "status": "success",
    "results": [
        {
            "id": 1,
            "room_number": "101",
            "floor": 1,
            "capacity": 2,
            "occupied_beds": 1,
            "available_beds": 1,
            "status": "available",
            "rent": 5000,
            "students": [...]
        }
    ]
}
```

#### Create Room
```
POST /api/rooms/
Content-Type: application/json

{
    "room_number": "101",
    "floor": 1,
    "capacity": 2,
    "rent": 5000
}

Response: 201 Created
```

#### Allocate Student to Room
```
POST /api/rooms/{id}/allocate/
Content-Type: application/json

{
    "student_id": 1
}

Response: 200 OK
{
    "status": "success",
    "message": "Student allocated to room successfully"
}
```

---

### Fees

#### List Fees
```
GET /api/fees/
Query Parameters:
  - status: Filter by status
  - student_id: Filter by student
  - month: Filter by month

Response:
{
    "status": "success",
    "results": [
        {
            "id": 1,
            "student": {...},
            "amount": 5000,
            "amount_paid": 2500,
            "remaining_amount": 2500,
            "status": "partially_paid",
            "due_date": "2024-05-30",
            "month": "May 2024"
        }
    ]
}
```

#### Record Payment
```
POST /api/fees/{id}/payment/
Content-Type: application/json

{
    "amount": 2500,
    "payment_method": "online",
    "notes": "Online transfer via bank"
}

Response: 200 OK
{
    "status": "success",
    "message": "Payment recorded successfully"
}
```

#### Generate Monthly Fees
```
POST /api/fees/generate/
Content-Type: application/json

{
    "month": "June 2024"
}

Response: 200 OK
{
    "status": "success",
    "message": "Fees generated for 45 students",
    "count": 45
}
```

---

### Complaints

#### List Complaints
```
GET /api/complaints/
Query Parameters:
  - status: Filter by status
  - priority: Filter by priority
  - student_id: Filter by student

Response:
{
    "status": "success",
    "results": [
        {
            "id": 1,
            "student": {...},
            "title": "Water problem in room",
            "description": "No water supply since morning",
            "priority": "high",
            "status": "in_progress",
            "technician": {...},
            "submitted_date": "2024-05-06T10:30:00Z"
        }
    ]
}
```

#### Submit Complaint
```
POST /api/complaints/
Content-Type: application/json

{
    "title": "Broken furniture",
    "description": "Chair in room 101 is broken",
    "priority": "medium"
}

Response: 201 Created
```

#### Update Complaint Status
```
PATCH /api/complaints/{id}/
Content-Type: application/json

{
    "status": "resolved",
    "resolution_details": "Chair has been repaired"
}

Response: 200 OK
```

#### Assign Complaint to Technician
```
POST /api/complaints/{id}/assign/
Content-Type: application/json

{
    "technician_id": 5
}

Response: 200 OK
```

---

### Attendance

#### List Attendance
```
GET /api/attendance/
Query Parameters:
  - student_id: Filter by student
  - date: Filter by date (YYYY-MM-DD)
  - month: Filter by month

Response:
{
    "status": "success",
    "results": [
        {
            "id": 1,
            "student": {...},
            "date": "2024-05-06",
            "present": true,
            "notes": ""
        }
    ]
}
```

#### Mark Attendance
```
POST /api/attendance/
Content-Type: application/json

{
    "student_id": 1,
    "date": "2024-05-06",
    "present": true,
    "notes": "Present"
}

Response: 201 Created
```

---

### Visitors

#### List Visitors
```
GET /api/visitors/
Query Parameters:
  - student_id: Filter by student
  - check_in_date: Filter by date

Response:
{
    "status": "success",
    "results": [
        {
            "id": 1,
            "student": {...},
            "visitor_name": "Mr. Ramesh Doe",
            "phone": "9876543211",
            "relationship": "Father",
            "check_in_date": "2024-05-06T10:00:00Z",
            "check_out_date": "2024-05-06T14:00:00Z",
            "purpose": "Monthly visit"
        }
    ]
}
```

#### Record Visitor Entry
```
POST /api/visitors/
Content-Type: application/json

{
    "student_id": 1,
    "visitor_name": "Mr. Ramesh Doe",
    "phone": "9876543211",
    "relationship": "Father",
    "id_proof_type": "Aadhar",
    "id_proof_number": "1234-5678-9012",
    "purpose": "Monthly visit",
    "check_in_date": "2024-05-06T10:00:00Z"
}

Response: 201 Created
```

---

### Dashboard/Analytics

#### Get Dashboard Data
```
GET /api/dashboard/

Response (for Admin):
{
    "status": "success",
    "data": {
        "total_students": 50,
        "total_rooms": 25,
        "available_rooms": 10,
        "occupied_rooms": 15,
        "total_complaints": 15,
        "pending_complaints": 5,
        "total_revenue": 250000,
        "pending_revenue": 75000,
        "overdue_fees": [...]
    }
}
```

#### Get Analytics
```
GET /api/analytics/?type=monthly_revenue&year=2024&month=5

Response:
{
    "status": "success",
    "data": {
        "month": "May 2024",
        "revenue": 250000,
        "fees_generated": 50,
        "fees_paid": 35,
        "fees_pending": 15
    }
}
```

---

### Reports

#### Export Students CSV
```
GET /api/reports/students/csv/

Response: application/csv
```

#### Export Fees CSV
```
GET /api/reports/fees/csv/

Response: application/csv
```

#### Generate Custom Report
```
POST /api/reports/generate/
Content-Type: application/json

{
    "report_type": "fee_summary",
    "start_date": "2024-01-01",
    "end_date": "2024-05-31",
    "format": "pdf"
}

Response: PDF File Download
```

---

## Error Codes

| Code | Description |
|------|-------------|
| 200 | OK - Request successful |
| 201 | Created - Resource created |
| 204 | No Content - Successful deletion |
| 400 | Bad Request - Invalid data |
| 401 | Unauthorized - Not logged in |
| 403 | Forbidden - Permission denied |
| 404 | Not Found - Resource not found |
| 409 | Conflict - Data conflict |
| 500 | Server Error - Internal error |

---

## Rate Limiting

The API implements rate limiting:
- 1000 requests per hour for authenticated users
- 100 requests per hour for unauthenticated users

Rate limit headers:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1620000000
```

---

## Pagination

Paginated endpoints support:
- `?page=1` - Page number
- `?page_size=20` - Results per page

---

## Filtering

Endpoints support filtering with query parameters:
```
GET /api/students/?gender=M&city=Bangalore&page=1
```

---

## Ordering

Supported orderings:
```
GET /api/students/?ordering=-created_at,first_name
```

---

## Examples

### cURL Examples

**Login:**
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password123"}'
```

**Get Students:**
```bash
curl -X GET http://localhost:8000/api/students/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Create Student:**
```bash
curl -X POST http://localhost:8000/api/students/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d @student.json
```

### Python Example

```python
import requests

API_BASE = 'http://localhost:8000/api/'

# Login
response = requests.post(f'{API_BASE}auth/login/', json={
    'username': 'admin',
    'password': 'password123'
})
token = response.json()['token']

headers = {'Authorization': f'Bearer {token}'}

# Get students
students = requests.get(f'{API_BASE}students/', headers=headers)
print(students.json())
```

### JavaScript Example

```javascript
const API_BASE = 'http://localhost:8000/api/';

// Login
const loginResponse = await fetch(`${API_BASE}auth/login/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: 'admin', password: 'password123' })
});

const { token } = await loginResponse.json();

// Get students
const studentsResponse = await fetch(`${API_BASE}students/`, {
    headers: { 'Authorization': `Bearer ${token}` }
});

const students = await studentsResponse.json();
console.log(students);
```

---

## Changelog

### Version 1.0 (May 2024)
- Initial API release
- Basic CRUD endpoints for all resources
- Authentication and authorization
- Analytics and reporting endpoints

---

**Last Updated**: May 2024
**Maintained by**: Hostel Management System Team
