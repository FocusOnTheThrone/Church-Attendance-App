#!/usr/bin/env python
"""
Run a quick test of the attendance analysis view using Django test client.
Saves HTML output to analysis_test_output.html and prints status.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from attendance.models import Service

User = get_user_model()
client = Client()

# Login by force (no password needed)
admin = User.objects.filter(is_superuser=True).first()
if admin is None:
    print('No superuser found; cannot test')
    sys.exit(1)
client.force_login(admin)

service = Service.objects.first()
if not service:
    print('No Service instances found')
    sys.exit(1)

url = f"/events/{service.service_type}/{service.id}/analysis/"
print('Requesting', url)
# Provide HTTP_HOST to avoid DisallowedHost in tests
resp = client.get(url, HTTP_HOST='127.0.0.1')
print('Status code:', resp.status_code)
open('analysis_test_output.html','wb').write(resp.content)
print('Wrote analysis_test_output.html')
if resp.status_code != 200:
    print(resp.content.decode('utf-8'))
else:
    print('OK')
