#!/bin/bash

# Hostel Management System - Database Error Auto-Fix
# Run this script if you get "no such table: core_userrole" error

echo ""
echo "===================================="
echo "Hostel Management System - Auto Fix"
echo "===================================="
echo ""

# Check if virtual environment exists
if [ ! -f "venv/bin/activate" ]; then
    echo "[ERROR] Virtual environment not found!"
    echo "Please extract the project and run setup.sh first."
    read -p "Press Enter to exit..."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

echo "[1/4] Running database migrations..."
python manage.py migrate

if [ $? -ne 0 ]; then
    echo "[ERROR] Migration failed!"
    read -p "Press Enter to exit..."
    exit 1
fi

echo ""
echo "[2/4] Creating sample data..."
python manage.py shell < setup_demo_data.py

if [ $? -ne 0 ]; then
    echo "[ERROR] Sample data creation failed!"
    read -p "Press Enter to exit..."
    exit 1
fi

echo ""
echo "[3/4] Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "===================================="
echo "[4/4] Starting Django server..."
echo "===================================="
echo ""
echo "Server is running at: http://localhost:8000"
echo ""
echo "Login with:"
echo "  Username: admin"
echo "  Password: admin123"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python manage.py runserver
