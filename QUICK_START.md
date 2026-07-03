# Quick Start Guide

## For Windows Users (30 seconds)

1. **Extract the ZIP file**
2. **Double-click `setup.bat`**
3. **Open browser to `http://localhost:8000`**

That's it! The setup script handles everything:
- Creates virtual environment
- Installs dependencies
- Creates database
- Creates demo users
- Starts the development server

### Default Login Credentials:
- **Admin**: admin / admin123
- **Student**: student1 / student123
- **Technician**: technician1 / tech123

---

## For Linux/Mac Users (30 seconds)

1. **Extract the ZIP file**
2. **Open Terminal and run:**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```
3. **Open browser to `http://localhost:8000`**

---

## Manual Setup (2 minutes)

### Step 1: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Setup Database
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 4: Create Demo Data
```bash
python manage.py shell < setup_demo_data.py
```

### Step 5: Run Server
```bash
python manage.py runserver
```

---

## First Time Usage

### As Admin:
1. Login with `admin` / `admin123`
2. Go to "Students" to add students
3. Go to "Rooms" to create rooms
4. Allocate rooms to students
5. Generate monthly fees
6. View complaints

### As Student:
1. Login with `student1` / `student123`
2. View your profile and room details
3. Check your fees
4. Submit complaints
5. Record visitor entries

### As Technician:
1. Login with `technician1` / `tech123`
2. View assigned complaints
3. Update complaint status
4. Add resolution details

---

## Common Tasks

### Generate More Sample Data
```bash
python manage.py generate_sample_data --students 100 --rooms 50
```

### Create Admin Account
```bash
python manage.py createsuperuser
# Follow prompts to create new admin user
```

### View Database Admin Panel
```
http://localhost:8000/admin/
```

### Export Data to CSV
- Go to Reports (Admin panel)
- Click "Export Students" or "Export Fees"

---

## Troubleshooting

### Port 8000 is already in use?
```bash
python manage.py runserver 8001
```
Then access: `http://localhost:8001`

### Module import error?
```bash
pip install -r requirements.txt
```

### Database errors?
```bash
python manage.py migrate --run-syncdb
```

### Forgot admin password?
```bash
python manage.py changepassword admin
```

---

## File Organization

```
hostel_management_system/
├── manage.py              ← Run Django commands
├── setup.bat              ← Windows auto-setup
├── setup.sh               ← Linux/Mac auto-setup
├── requirements.txt       ← Python dependencies
├── README.md              ← Full documentation
├── DEPLOYMENT.md          ← Production guide
├── API_DOCUMENTATION.md   ← API reference
├── db.sqlite3             ← Database (created after setup)
├── hostel_config/         ← Django configuration
├── core/                  ← Main application
│   ├── models.py          ← Database models
│   ├── views.py           ← Business logic
│   ├── forms.py           ← Input forms
│   └── utils.py           ← Helper functions
└── templates/             ← HTML templates
    ├── base.html          ← Main template
    ├── login.html         ← Login page
    ├── admin/             ← Admin templates
    ├── student/           ← Student templates
    └── technician/        ← Technician templates
```

---

## Next Steps

1. **Explore the Dashboard**
   - Admin: View statistics and manage operations
   - Student: Check your room and fees
   - Technician: See assigned complaints

2. **Add Data**
   - Create rooms
   - Add students
   - Allocate rooms
   - Generate fees

3. **Test Features**
   - Submit complaints
   - Record payments
   - Add visitors
   - View reports

4. **Customize**
   - Update hostel name in templates
   - Customize fees
   - Add more rooms
   - Invite other users

---

## Getting Help

### Documentation:
- Full guide: `README.md`
- Deployment: `DEPLOYMENT.md`
- API docs: `API_DOCUMENTATION.md`

### Django Admin Panel:
- Access at: `http://localhost:8000/admin/`
- Can directly manage database from here

### Support:
- Check Django documentation: https://docs.djangoproject.com/
- Review code comments for implementation details

---

## Key Features You'll Love ❤️

✅ **Role-Based Access Control** - Different views for Admin, Student, Technician
✅ **Student Management** - Complete student profiles and history
✅ **Room Allocation** - Smart room assignment and tracking
✅ **Fee Tracking** - Automated fee generation and payment recording
✅ **Complaint System** - Student complaints with technician assignment
✅ **Reports & Export** - CSV export for analysis
✅ **Beautiful Dashboard** - Real-time statistics and overview
✅ **Mobile Responsive** - Works on phones and tablets
✅ **Easy Setup** - Auto-setup script does everything

---

**Ready to go? Run `setup.bat` (Windows) or `setup.sh` (Linux/Mac) now!** 🚀
