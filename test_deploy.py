"""
Minimal Django test for Vercel deployment
"""
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set minimal Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

try:
    import django
    django.setup()
    print("Django setup successful")
    
    from django.http import HttpResponse
    
    def handler(request):
        return HttpResponse("Django is working!")
    
    print("Handler created successfully")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
