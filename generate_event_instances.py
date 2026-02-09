#!/usr/bin/env python
"""
Generate 5 new service instances for each service type and populate each
with 15-40 random attendance records to test charts.
Run with: python generate_event_instances.py
"""
import os
import sys
import random
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from attendance.models import Service, Attendance, Person
from django.contrib.auth import get_user_model

User = get_user_model()

# Choose a system user to be created_by (pick first superuser or any user)
creator = User.objects.filter(is_superuser=True).first() or User.objects.first()

SERVICE_TYPES = [st[0] for st in Service.SERVICE_TYPE_CHOICES]

print(f"Using creator: {creator}")

persons = list(Person.objects.all())
if len(persons) < 20:
    print("Warning: fewer than 20 people in the register; generated attendances may be smaller.")

created_services = []
created_attendances = 0

for stype in SERVICE_TYPES:
    # create 5 instances per service type on consecutive dates in the past
    for i in range(5):
        instance_date = date.today() - timedelta(days=7 * (i + 1) + random.randint(0,6))
        title = f"Auto Test {i+1}"
        # ensure uniqueness: use try/except when creating
        service, created = Service.objects.get_or_create(
            date=instance_date,
            service_type=stype,
            title=title,
            defaults={
                'created_by': creator,
            }
        )
        created_services.append(service)

        # Select a random sample of people (min 15, max 40 or number of people)
        max_people = min(len(persons), 40)
        if max_people < 15:
            sample_size = max_people
        else:
            sample_size = random.randint(15, max_people)
        sample = random.sample(persons, sample_size)

        attendances = []
        for p in sample:
            # skip if attendance already exists for this person+service
            if Attendance.objects.filter(service=service, person=p).exists():
                continue
            # category distribution: mostly members, some visitors, few healed
            r = random.random()
            if r < 0.75:
                category = Attendance.MEMBER
            elif r < 0.95:
                category = Attendance.VISITOR
            else:
                category = Attendance.HEALED

            # determine is_first_time_visitor (has any past attendance?)
            has_attended_before = Attendance.objects.filter(person=p).exists()
            is_first = not has_attended_before and category == Attendance.VISITOR

            att = Attendance(
                service=service,
                person=p,
                category=category,
                present=True,
                is_first_time_visitor=is_first,
                is_healed_this_service=(category == Attendance.HEALED),
                notes="Auto-generated for chart testing" if random.random() < 0.2 else "",
            )
            attendances.append(att)

        # Bulk create attendances
        Attendance.objects.bulk_create(attendances)
        created_attendances += len(attendances)
        print(f"Service {service} - added {len(attendances)} attendances")

print(f"Done: created/ensured {len(created_services)} services, {created_attendances} attendance records.")
