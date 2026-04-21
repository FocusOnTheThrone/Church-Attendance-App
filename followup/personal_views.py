from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, F
from datetime import datetime, timedelta
from django.template import defaultfilters

from attendance.models import Person, Attendance, Service
from followup.models import FollowUpRecord, FollowUpCase

# Service type choices for filter
SERVICE_TYPE_CHOICES = [
    ('all', 'All Services'),
    ('sunday_service', 'Sunday Service'),
    ('midweek_service', 'Midweek Service'),
    ('prayer_meeting', 'Prayer Meeting'),
    ('youth_service', 'Youth Service'),
    ('children_service', 'Children Service'),
    ('special_event', 'Special Event'),
]

# Create a dictionary for easy lookup
SERVICE_TYPE_DICT = dict(SERVICE_TYPE_CHOICES)


def _get_org(request):
    if request.user.is_authenticated and hasattr(request.user, 'organization'):
        return request.user.organization
    return None


@login_required
def personal_report(request, person_id):
    """
    Comprehensive personal report showing attendance history, follow-ups, and statistics.
    """
    org = _get_org(request)
    filter_kwargs = {"id": person_id}
    if org:
        filter_kwargs["organization"] = org
    person = get_object_or_404(Person, **filter_kwargs)
    
    # Get filter parameters
    service_type_filter = request.GET.get('service_type', 'sunday_service')
    
    # Get all attendance records for this person with optional service type filter
    attendances_queryset = Attendance.objects.filter(person=person)
    if service_type_filter != 'all':
        attendances_queryset = attendances_queryset.filter(service__service_type=service_type_filter)
    
    attendances = attendances_queryset.select_related('service').order_by('-service__date')
    
    # Get all follow-up records for this person
    followup_records = FollowUpRecord.objects.filter(
        person=person
    ).select_related('service', 'contacted_by', 'followup_case').order_by('-follow_up_date')
    
    # Get follow-up cases
    followup_cases = FollowUpCase.objects.filter(
        person=person
    ).order_by('-created_at')
    
    # Calculate attendance statistics
    svc_qs = Service.objects.all()
    if org:
        svc_qs = svc_qs.filter(organization=org)
    total_services = svc_qs.count()
    attended_services = attendances.count()
    attendance_rate = (attended_services / total_services * 100) if total_services > 0 else 0
    
    # Calculate attendance by service type
    attendance_by_type = attendances.values('service__service_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Calculate attendance by month (last 12 months)
    twelve_months_ago = datetime.now() - timedelta(days=365)
    monthly_attendance = attendances.filter(
        service__date__gte=twelve_months_ago
    ).extra({
        'month': "strftime(service__date, '%%Y-%%m')"
    }).values('month').annotate(
        count=Count('id')
    ).order_by('month')
    
    # Calculate consecutive absences
    consecutive_absences = calculate_consecutive_absences(person, org)
    
    # Follow-up statistics
    successful_followups = followup_records.filter(is_completed=True).count()
    total_followups = followup_records.count()
    followup_success_rate = (successful_followups / total_followups * 100) if total_followups > 0 else 0
    
    # Group attendances and follow-ups by service
    service_timeline = []
    all_services = Service.objects.all()
    if org:
        all_services = all_services.filter(organization=org)
    if service_type_filter != 'all':
        all_services = all_services.filter(service_type=service_type_filter)
    all_services = all_services.order_by('-date')
    
    for service in all_services:
        attendance = attendances.filter(service=service).first()
        followup = followup_records.filter(service=service).first()
        
        service_timeline.append({
            'service': service,
            'attended': attendance is not None,
            'attendance': attendance,
            'followup': followup,
            'date': service.date,
        })
    
    context = {
        'person': person,
        'attendances': attendances,
        'followup_records': followup_records,
        'followup_cases': followup_cases,
        'service_timeline': service_timeline,
        'service_type_filter': service_type_filter,
        'service_type_choices': SERVICE_TYPE_CHOICES,
        'current_filter_label': SERVICE_TYPE_DICT.get(service_type_filter, 'All Services'),
        'stats': {
            'total_services': total_services,
            'attended_services': attended_services,
            'attendance_rate': round(attendance_rate, 1),
            'attendance_by_type': attendance_by_type,
            'monthly_attendance': monthly_attendance,
            'consecutive_absences': consecutive_absences,
            'successful_followups': successful_followups,
            'total_followups': total_followups,
            'followup_success_rate': round(followup_success_rate, 1),
        }
    }
    
    return render(request, 'followup/personal_report.html', context)


def calculate_consecutive_absences(person, org=None):
    """
    Calculate consecutive absences from the most recent service backwards.
    """
    consecutive = 0
    services = Service.objects.all()
    if org:
        services = services.filter(organization=org)
    services = services.order_by('-date')
    
    for service in services:
        attended = Attendance.objects.filter(person=person, service=service).exists()
        if attended:
            break
        else:
            consecutive += 1
    
    return consecutive
