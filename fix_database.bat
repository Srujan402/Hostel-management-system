@echo off
REM Hostel Management System - Database Error Auto-Fix
REM Run this script if you get "no such table: core_userrole" error

echo.
echo ====================================
echo Hostel Management System - Auto Fix
echo ====================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found!
    echo Please extract the project and run setup.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

echo [1/4] Running database migrations...
python manage.py migrate

if errorlevel 1 (
    echo [ERROR] Migration failed!
    pause
    exit /b 1
)

echo.
echo [2/4] Creating sample data...
python manage.py shell < setup_demo_data.py

if errorlevel 1 (
    echo [ERROR] Sample data creation failed!
    pause
    exit /b 1
)

echo.
echo [3/4] Collecting static files...
python manage.py collectstatic --noinput

echo.
echo ====================================
echo [4/4] Starting Django server...
echo ====================================
echo.
echo Server is running at: http://localhost:8000
echo.
echo Login with:
echo   Username: admin
echo   Password: admin123
echo.
echo Press Ctrl+C to stop the server
echo.

python manage.py runserver
