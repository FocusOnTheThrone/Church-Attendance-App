# Church Attendance App Deployment Script for PowerShell
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Church Attendance App Deployment" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Step 1: Activate virtual environment
Write-Host "Step 1: Activating virtual environment..." -ForegroundColor Yellow
if (Test-Path ".venv\Scripts\Activate.ps1") {
    & .venv\Scripts\Activate.ps1
    Write-Host "Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "ERROR: Virtual environment not found!" -ForegroundColor Red
    Read-Host "Press Enter to exit..."
    exit 1
}

Write-Host ""

# Step 2: Check Django installation
Write-Host "Step 2: Checking Django installation..." -ForegroundColor Yellow
try {
    $djangoVersion = python -m django --version
    Write-Host "Django version: $djangoVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Django not installed!" -ForegroundColor Red
    Read-Host "Press Enter to exit..."
    exit 1
}

Write-Host ""

# Step 3: Run Django system check
Write-Host "Step 3: Running Django system check..." -ForegroundColor Yellow
try {
    $checkResult = python manage.py check
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Django system check passed" -ForegroundColor Green
    } else {
        Write-Host "ERROR: Django system check failed!" -ForegroundColor Red
        Read-Host "Press Enter to exit..."
        exit 1
    }
} catch {
    Write-Host "ERROR: Django system check failed!" -ForegroundColor Red
    Read-Host "Press Enter to exit..."
    exit 1
}

Write-Host ""

# Step 4: Collect static files
Write-Host "Step 4: Collecting static files..." -ForegroundColor Yellow
try {
    $collectResult = python manage.py collectstatic --noinput
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Static files collected successfully" -ForegroundColor Green
    } else {
        Write-Host "ERROR: Static file collection failed!" -ForegroundColor Red
        Read-Host "Press Enter to exit..."
        exit 1
    }
} catch {
    Write-Host "ERROR: Static file collection failed!" -ForegroundColor Red
    Read-Host "Press Enter to exit..."
    exit 1
}

Write-Host ""

# Step 5: Create migrations
Write-Host "Step 5: Creating migrations..." -ForegroundColor Yellow
try {
    python manage.py makemigrations --noinput
    Write-Host "✓ Migrations created" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Migration creation failed!" -ForegroundColor Red
    Read-Host "Press Enter to exit..."
    exit 1
}

Write-Host ""

# Step 6: Apply migrations
Write-Host "Step 6: Applying migrations..." -ForegroundColor Yellow
try {
    python manage.py migrate --noinput
    Write-Host "✓ Migrations applied successfully" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Migration application failed!" -ForegroundColor Red
    Read-Host "Press Enter to exit..."
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Ready for Vercel Deployment!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Install Vercel CLI: npm i -g vercel" -ForegroundColor White
Write-Host "2. Login to Vercel: vercel login" -ForegroundColor White
Write-Host "3. Push to GitHub: git push origin main" -ForegroundColor White
Write-Host "4. Deploy on Vercel: vercel --prod" -ForegroundColor White
Write-Host "5. Set environment variables in Vercel dashboard" -ForegroundColor White
Write-Host ""

Write-Host "Required Environment Variables:" -ForegroundColor Yellow
Write-Host "- SECRET_KEY (generate new one)" -ForegroundColor White
Write-Host "- DATABASE_URL (from Vercel PostgreSQL)" -ForegroundColor White
Write-Host "- DEBUG=False" -ForegroundColor White
Write-Host "- ALLOWED_HOSTS=your-domain.vercel.app" -ForegroundColor White
Write-Host ""

Write-Host "Generate SECRET_KEY with:" -ForegroundColor Cyan
Write-Host 'python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"' -ForegroundColor White
Write-Host ""

Write-Host "Press Enter to continue..." -ForegroundColor Gray
Read-Host
