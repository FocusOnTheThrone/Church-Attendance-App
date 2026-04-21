@echo off
echo Starting Django Church Attendance App...
echo.

cd /d "f:\Cursor AI\Church Attendance App"
echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Starting Django server...
python manage.py runserver 0.0.0.0:8000

pause
