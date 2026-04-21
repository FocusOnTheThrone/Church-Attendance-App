# Django Church Attendance App Starter Script
Write-Host "Starting Django Church Attendance App..." -ForegroundColor Green
Write-Host ""

# Navigate to project directory
Set-Location "f:\Cursor AI\Church Attendance App"
Write-Host "Project directory: $(Get-Location)" -ForegroundColor Yellow

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .venv\Scripts\Activate.ps1

# Check Django installation
Write-Host "Checking Django installation..." -ForegroundColor Yellow
python -m django --version

# Check project health
Write-Host "Checking project health..." -ForegroundColor Yellow
python manage.py check

# Start Django server
Write-Host "Starting Django server..." -ForegroundColor Green
Write-Host "Access your app at: http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host "Admin panel at: http://127.0.0.1:8000/staff-dashboard/" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

python manage.py runserver 0.0.0.0:8000
