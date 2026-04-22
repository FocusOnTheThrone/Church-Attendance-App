"""
Production WSGI entry point for Vercel deployment
Handles Django initialization without .env file dependency
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set Django settings for production
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vercel_production')

# Initialize Django
from django.core.management import execute_from_command_line

# Run migrations automatically if needed
try:
    execute_from_command_line(['manage.py', 'migrate', '--noinput'])
except Exception:
    pass  # Migrations may have already run

# Get the WSGI application
application = get_wsgi_application()
