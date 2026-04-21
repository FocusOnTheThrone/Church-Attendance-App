@echo off
title Deploy to Vercel
color 0A

echo ========================================
echo   Church Attendance App Deployment
echo ========================================
echo.

echo Step 1: Activating virtual environment...
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
    echo Virtual environment activated
) else (
    echo ERROR: Virtual environment not found!
    pause
    exit /b 1
)

echo.
echo Step 2: Checking Django installation...
python -m django --version
if errorlevel 1 (
    echo ERROR: Django not installed!
    pause
    exit /b 1
)

echo.
echo Step 3: Running Django system check...
python manage.py check
if errorlevel 1 (
    echo ERROR: Django system check failed!
    pause
    exit /b 1
)

echo.
echo Step 4: Collecting static files...
python manage.py collectstatic --noinput
if errorlevel 1 (
    echo ERROR: Static file collection failed!
    pause
    exit /b 1
)

echo.
echo Step 5: Creating migrations...
python manage.py makemigrations --noinput

echo.
echo Step 6: Applying migrations...
python manage.py migrate --noinput

echo.
echo ========================================
echo   Ready for Vercel Deployment!
echo ========================================
echo.
echo Next steps:
echo 1. Install Vercel CLI: npm i -g vercel
echo 2. Login to Vercel: vercel login
echo 3. Push to GitHub: git push origin main
echo 4. Deploy on Vercel: vercel --prod
echo 5. Set environment variables in Vercel dashboard
echo.
echo Required Environment Variables:
echo - SECRET_KEY (generate new one)
echo - DATABASE_URL (from Vercel PostgreSQL)
echo - DEBUG=False
echo - ALLOWED_HOSTS=your-domain.vercel.app
echo.
echo Generate SECRET_KEY with:
echo python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
echo.
pause
