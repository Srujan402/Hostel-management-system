@echo off
REM Hostel Management System Setup Script for Windows

echo.
echo ====================================
echo Hostel Management System Setup
echo ====================================
echo.

REM Create virtual environment
echo [1/5] Creating virtual environment...
python -m venv venv
call venv\Scripts\activate

REM Install dependencies
echo [2/5] Installing dependencies...
pip install -r requirements.txt

REM Run migrations
echo [3/5] Creating database...
python manage.py makemigrations
python manage.py migrate

REM Create superuser
echo [4/5] Creating demo data...
echo.
echo Creating demo users...
python manage.py shell < setup_demo_data.py

REM Run server
echo [5/5] Starting Django development server...
echo.
echo ====================================
echo Setup completed successfully!
echo ====================================
echo.
echo Django server is running at: http://localhost:8000
echo Login with:
echo   Admin: admin / admin123
echo   Student: student1 / student123
echo   Technician: technician1 / tech123
echo.
echo Press Ctrl+C to stop the server
echo.

python manage.py runserver
