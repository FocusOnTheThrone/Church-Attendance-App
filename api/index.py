import os
import sys
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Get the WSGI application
application = get_wsgi_application()

# Vercel serverless function handler
def handler(request):
    return HttpResponse(application(request.environ, lambda status, headers: [
        ('b' + str(status), headers)
    ])(request.get_data()))
