"""
Minimal WSGI entry point for Vercel deployment
Eliminates all complex imports and potential failure points
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'minimal_settings')

# Get the WSGI application
application = get_wsgi_application()
