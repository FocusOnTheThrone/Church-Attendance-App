from datetime import date, timedelta
import json

from django.db.models import Case, Q, Value, When

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.dateparse import parse_date
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from attendance.forms import PersonForm, VisitorForm
from attendance.models import Attendance, Person, Service
from followup.models import FollowUpCase
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest

# Service types for the events page (must match Service.SERVICE_TYPE_CHOICES)
SERVICE_TYPES = [
    ("evangelism", "Evangelism"),
    ("crusade", "Crusade"),
    ("prayers", "Prayers"),
    ("home_fellowship", "Home Fellowship"),
    ("worship_practice", "Worship Practice"),
    ("midweek_services", "Midweek Services"),
    ("worship_extravaganza", "Worship Extravaganza"),
    ("keshas", "Keshas"),
    ("saturday_preparations", "Saturday Preparations"),
    ("sunday_service", "Sunday Service"),
    ("others", "Others"),
]

# Weekday rules: Monday=0 ... Sunday=6
WEEKDAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

SERVICE_DAY_RULES = {
    "evangelism": list(range(7)),
    "crusade": list(range(7)),
    "prayers": [0, 1, 2, 3, 4, 5],  # all days except Sunday
    "home_fellowship": list(range(7)),
    "worship_practice": list(range(7)),
    "worship_extravaganza": [5],  # Saturday only
    "saturday_preparations": [5],
    "sunday_service": [6],
    "midweek_services": [0, 1, 2, 3, 4],
    "keshas": list(range(7)),
    "others": list(range(7)),
}


def _get_date_range_from_query_params(request):
    """
    Read week_start / week_end from query params.

    If not provided, default to last 7 days (today and previous 6 days).
    """
    # DRF Request objects use .query_params; plain Django requests use .GET
    params = getattr(request, "query_params", request.GET)

    week_start_str = params.get("week_start")
    week_end_str = params.get("week_end")

    if week_start_str and week_end_str:
        week_start = parse_date(week_start_str)
        week_end = parse_date(week_end_str)
    else:
        week_end = date.today()
        week_start = week_end - timedelta(days=6)

    return week_start, week_end


class WeeklySummaryView(APIView):
    """
    Return a simple weekly summary of attendance.

    If no dates are provided, use the last 7 days.
    You can override via query params:
    - week_start=YYYY-MM-DD
    - week_end=YYYY-MM-DD
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        week_start, week_end = _get_date_range_from_query_params(request)

        # Compute metrics directly from Attendance
        qs = Attendance.objects.filter(
            service__date__gte=week_start,
            service__date__lte=week_end,
        )

        total_attendance = qs.count()
        visitors_count = qs.filter(category=Attendance.VISITOR).count()
        healed_count = qs.filter(category=Attendance.HEALED).count()

        # Follow-up count (open + in progress) as of the end date of the range
        follow_up_count = FollowUpCase.objects.filter(
            status__in=[FollowUpCase.STATUS_OPEN, FollowUpCase.STATUS_IN_PROGRESS],
            created_at__date__lte=week_end,
        ).count()

        data = {
            "week_start": week_start,
            "week_end": week_end,
            "total_attendance": total_attendance,
            "visitors_count": visitors_count,
            "healed_count": healed_count,
            "follow_up_count": follow_up_count,
        }

        return Response(data)


class WeeklyReportTextView(APIView):
    """
    Generate a WhatsApp-ready weekly report message.

    Query params:
    - week_start=YYYY-MM-DD
    - week_end=YYYY-MM-DD
    (defaults to last 7 days)
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        week_start, week_end = _get_date_range_from_query_params(request)

        qs = Attendance.objects.filter(
            service__date__gte=week_start,
            service__date__lte=week_end,
        )

        total_attendance = qs.count()
        visitors_count = qs.filter(category=Attendance.VISITOR).count()
        healed_count = qs.filter(category=Attendance.HEALED).count()

        follow_up_count = FollowUpCase.objects.filter(
            status__in=[FollowUpCase.STATUS_OPEN, FollowUpCase.STATUS_IN_PROGRESS],
            created_at__date__lte=week_end,
        ).count()

        message_lines = [
            "WEEKLY CHURCH REPORT",
            f"Period: {week_start} to {week_end}",
            "",
            f"Total attendance: {total_attendance}",
            f"Visitors: {visitors_count}",
            f"Healed-of-the-LORD: {healed_count}",
            f"Follow-up (open/in progress): {follow_up_count}",
            "",
            "Generated automatically by the attendance system.",
        ]

        return Response(
            {
                "week_start": week_start,
                "week_end": week_end,
                "total_attendance": total_attendance,
                "visitors_count": visitors_count,
                "healed_count": healed_count,
                "follow_up_count": follow_up_count,
                "message": "\n".join(message_lines),
            }
        )


class AttendanceTrendView(APIView):
    """
    Return attendance trends for the last N weeks.

    Query params:
    weeks: integer (default 12)

    Response shape:
    {
      "weeks": 12,
      "as_of": "2026-02-06",
      "results": [
        {
          "week_start": "2026-01-31",
          "week_end": "2026-02-06",
          "total_attendance": 42,
          "visitors_count": 5,
          "healed_count": 1
        },
        ...
      ]
    }
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        weeks_param = request.query_params.get("weeks", "12")
        try:
            weeks = int(weeks_param)
            if weeks < 1:
                raise ValueError
        except ValueError:
            return Response(
                {"detail": "weeks must be a positive integer."},
                status=400,
            )

        as_of = date.today()
        results = []

        # Build from oldest to newest week
        for i in range(weeks, 0, -1):
            week_end = as_of - timedelta(weeks=i - 1)
            week_start = week_end - timedelta(days=6)

            qs = Attendance.objects.filter(
                service__date__gte=week_start,
                service__date__lte=week_end,
            )

            total_attendance = qs.count()
            visitors_count = qs.filter(category=Attendance.VISITOR).count()
            healed_count = qs.filter(category=Attendance.HEALED).count()

            results.append(
                {
                    "week_start": week_start,
                    "week_end": week_end,
                    "total_attendance": total_attendance,
                    "visitors_count": visitors_count,
                    "healed_count": healed_count,
                }
            )

        return Response(
            {
                "weeks": weeks,
                "as_of": as_of,
                "results": results,
            }
        )


def _get_people_ordered_by_title():
    """Return all people ordered by title hierarchy, then name."""
    title_order = Case(
        When(title=Person.PROPHET, then=Value(1)),
        When(title=Person.GENERAL_OVERSEER, then=Value(2)),
        When(title=Person.SENIOR_ARCHBISHOP_EMERITUS, then=Value(3)),
        When(title=Person.SENIOR_ARCHBISHOP, then=Value(4)),
        When(title=Person.SENIOR_DEPUTY_ARCHBISHOP, then=Value(5)),
        When(title=Person.DEPUTY_ARCHBISHOP, then=Value(6)),
        When(title=Person.BISHOP, then=Value(7)),
        When(title=Person.OVERSEER, then=Value(8)),
        When(title=Person.SENIOR_PASTOR, then=Value(9)),
        When(title=Person.PASTOR, then=Value(10)),
        When(title=Person.SISTER, then=Value(11)),
        When(title=Person.BROTHER, then=Value(12)),
        When(title=Person.VISITOR, then=Value(13)),
        When(title=Person.EMPLOYEE, then=Value(14)),
        default=Value(99),
    )
    return Person.objects.all().annotate(title_sort=title_order).order_by("title_sort", "full_name")


@login_required
def events_page_view(request):
    """Landing page after login - list of service types to record attendance."""
    return render(request, "reports/events.html", {"service_types": SERVICE_TYPES})


def _get_age_bounds(age_group):
    """Return (min_dob, max_dob) for date_of_birth. Younger people have later DOB."""
    today = date.today()
    if age_group == Person.AGE_0_12:
        # 0-12 yrs: born between 12 yrs ago and today
        return (today - timedelta(days=12 * 365), today)
    if age_group == Person.AGE_13_19:
        # 13-19 yrs: born between 19 and 13 yrs ago
        return (today - timedelta(days=19 * 365), today - timedelta(days=13 * 365))
    if age_group == Person.AGE_20_35:
        # 20-35 yrs: born between 35 and 20 yrs ago
        return (today - timedelta(days=35 * 365), today - timedelta(days=20 * 365))
    if age_group == Person.AGE_36_PLUS:
        # 36+: born before 36 yrs ago
        return (None, today - timedelta(days=36 * 365))
    return None


@login_required
def register_view(request):
    """Full list of all members/people in the church with filters."""
    people = _get_people_ordered_by_title()
    params = request.GET
    title_filter = params.get("title", "").strip()
    gender_filter = params.get("gender", "").strip()
    member_visitor_filter = params.get("member_visitor", "").strip()
    age_filter = params.get("age", "").strip()
    fellowship_filter = params.get("fellowship", "").strip()
    occupation_filter = params.get("occupation", "").strip()
    residence_filter = params.get("residence", "").strip()

    if title_filter:
        people = people.filter(title=title_filter)
    if gender_filter:
        people = people.filter(gender=gender_filter)
    if member_visitor_filter == Person.MEMBER:
        people = people.exclude(title=Person.VISITOR)
    elif member_visitor_filter == Person.VISITOR_TYPE:
        people = people.filter(title=Person.VISITOR)
    if age_filter:
        bounds = _get_age_bounds(age_filter)
        if bounds:
            min_dob, max_dob = bounds
            if min_dob is not None and max_dob is not None:
                people = people.filter(
                    date_of_birth__isnull=False,
                    date_of_birth__gte=min_dob,
                    date_of_birth__lte=max_dob,
                )
            elif max_dob is not None:
                people = people.filter(date_of_birth__isnull=False, date_of_birth__lte=max_dob)
    if fellowship_filter:
        people = people.filter(fellowship=fellowship_filter)
    if occupation_filter:
        people = people.filter(occupation__iexact=occupation_filter)
    if residence_filter:
        people = people.filter(residence__icontains=residence_filter)

    # Distinct occupations and residences for filter dropdowns
    occupation_choices = sorted(
        {v.strip() for v in Person.objects.exclude(occupation="").values_list("occupation", flat=True) if v and v.strip()}
    )
    residence_choices = sorted(
        {v.strip() for v in Person.objects.exclude(residence="").values_list("residence", flat=True) if v and v.strip()}
    )

    context = {
        "people": people,
        "title_filter": title_filter,
        "gender_filter": gender_filter,
        "member_visitor_filter": member_visitor_filter,
        "age_filter": age_filter,
        "fellowship_filter": fellowship_filter,
        "occupation_filter": occupation_filter,
        "residence_filter": residence_filter,
        "title_choices": Person.TITLE_CHOICES,
        "gender_choices": Person.GENDER_CHOICES,
        "member_visitor_choices": Person.MEMBER_VISITOR_CHOICES,
        "age_choices": Person.AGE_CHOICES,
        "fellowship_choices": Person.FELLOWSHIP_CHOICES,
        "occupation_choices": occupation_choices,
        "residence_choices": residence_choices,
    }
    return render(request, "register.html", context)


@login_required
def add_member_view(request):
    """Add a new member to the main register."""
    next_url = request.GET.get("next") or request.POST.get("next", "events")
    if request.method == "POST":
        form = PersonForm(request.POST)
        if form.is_valid():
            person = form.save()
            messages.success(request, f"Member '{person.full_name}' added successfully.")
            return redirect(next_url if next_url else "events")
    else:
        form = PersonForm(initial={"title": Person.BROTHER})
    cancel_url = next_url if (next_url and next_url.startswith("/")) else reverse("events")
    return render(request, "add_member.html", {"form": form, "next_url": next_url, "cancel_url": cancel_url})


@login_required
def delete_person_view(request, person_id):
    """Delete a person from the register. POST only."""
    if request.method != "POST":
        return redirect("register")
    try:
        person = Person.objects.get(pk=person_id)
        name = person.full_name
        person.delete()
        messages.success(request, f"'{name}' has been removed from the register.")
    except Person.DoesNotExist:
        messages.error(request, "Person not found.")
    return redirect("register")


def _get_instance_display_name(service):
    """Display name for an event instance: Event Type - Date - Optional Title."""
    label = dict(SERVICE_TYPES).get(service.service_type, service.service_type)
    parts = [f"{label} - {service.date.strftime('%b %d, %Y')}"]
    if service.title.strip():
        parts.append(service.title.strip())
    return " - ".join(parts)


@login_required
def event_instances_view(request, service_type):
    """
    List event instances for a service type and allow creating new ones.
    Each instance is a Service with date + optional custom title.
    """
    valid_types = [st[0] for st in SERVICE_TYPES]
    if service_type not in valid_types:
        messages.error(request, "Invalid event type.")
        return redirect("events")

    service_type_label = dict(SERVICE_TYPES).get(service_type, service_type)
    instances = Service.objects.filter(service_type=service_type).order_by("-date", "-start_time")[:50]

    if request.method == "POST" and "create_instance" in request.POST:
        instance_date = parse_date(request.POST.get("instance_date"))
        custom_name = (request.POST.get("instance_title") or "").strip()
        if not instance_date:
            messages.error(request, "Please select a date.")
        else:
            # validate weekday rules
            allowed_days = SERVICE_DAY_RULES.get(service_type, list(range(7)))
            if instance_date.weekday() not in allowed_days:
                allowed_names = ", ".join([WEEKDAY_NAMES[d] for d in allowed_days])
                messages.error(request, f"{service_type_label} instances may only be created on: {allowed_names}")
            else:
                service = Service.objects.create(
                    date=instance_date,
                    service_type=service_type,
                    title=custom_name,
                    created_by=request.user,
                )
                messages.success(request, f"Event instance created: {_get_instance_display_name(service)}")
                return redirect("record_attendance", service_type=service_type, service_id=service.id)

    context = {
        "service_type": service_type,
        "service_type_label": service_type_label,
        "instances": instances,
        "today": date.today().strftime("%Y-%m-%d"),
        "allowed_days": SERVICE_DAY_RULES.get(service_type, list(range(7))),
        "allowed_days_names": ", ".join([WEEKDAY_NAMES[d] for d in SERVICE_DAY_RULES.get(service_type, list(range(7))) ]),
    }
    return render(request, "reports/event_instances.html", context)


@login_required
def record_attendance_view(request, service_type, service_id):
    """
    Record attendance for a specific event instance (Service).
    Shows main register with search + checkboxes. Supports adding visitors and per-person comments.
    """
    valid_types = [st[0] for st in SERVICE_TYPES]
    if service_type not in valid_types:
        messages.error(request, "Invalid event type.")
        return redirect("events")

    try:
        service = Service.objects.get(pk=service_id, service_type=service_type)
    except Service.DoesNotExist:
        messages.error(request, "Event instance not found.")
        return redirect("event_instances", service_type=service_type)

    service_type_label = dict(SERVICE_TYPES).get(service_type, service_type)
    service_date = service.date

    # Get all people for the register, sorted by hierarchy
    people = _get_people_ordered_by_title()

    # Already recorded for this service
    recorded_ids = set(
        Attendance.objects.filter(service=service).values_list("person_id", flat=True)
    )

    if request.method == "POST":
        # Handle "Save attendance" - record checked people and their comments
        if "save_attendance" in request.POST:
            checked_ids = set(int(x) for x in request.POST.getlist("attendees") if x.isdigit())
            # Check for comments on unchecked people - gently prompt to confirm
            people_with_notes_unchecked = []
            for p in people:
                notes_val = (request.POST.get(f"notes_{p.id}") or "").strip()
                if notes_val and p.id not in checked_ids:
                    people_with_notes_unchecked.append(p.full_name)
            if people_with_notes_unchecked:
                names = ", ".join(people_with_notes_unchecked)
                messages.warning(
                    request,
                    f"You added comments for {names}, but they aren't marked as present. "
                    "If they attended, please tick the box next to their name to include them. "
                    "If they didn't attend, you can clear the comment. "
                    "We just want to make sure the record reflects who was there.",
                )
                # Re-render with POST data preserved
                people_with_notes = [(p, (request.POST.get(f"notes_{p.id}") or "").strip()) for p in people]
                recorded_ids = checked_ids
                instance_comment = (request.POST.get("instance_comment") or "").strip()
                context = {
                    "service_type": service_type,
                    "service_type_label": service_type_label,
                    "service": service,
                    "service_date": service_date,
                    "people": people,
                    "people_with_notes": people_with_notes,
                    "recorded_ids": recorded_ids,
                    "person_form": VisitorForm(),
                    "instance_display_name": _get_instance_display_name(service),
                    "instance_comment": instance_comment,
                }
                return render(request, "record_attendance.html", context)
            for person_id in checked_ids:
                try:
                    person = Person.objects.get(pk=person_id)
                    if person.title == Person.VISITOR:
                        att_category = Attendance.VISITOR
                    else:
                        att_category = Attendance.MEMBER
                    has_attended_before = Attendance.objects.filter(person=person).exists()
                    notes = (request.POST.get(f"notes_{person_id}") or "").strip()
                    Attendance.objects.update_or_create(
                        service=service,
                        person=person,
                        defaults={
                            "category": att_category,
                            "present": True,
                            "is_first_time_visitor": not has_attended_before,
                            "notes": notes,
                        },
                    )
                except (Person.DoesNotExist, ValueError):
                    pass
            # Remove attendance for people who were unchecked
            Attendance.objects.filter(service=service).exclude(person_id__in=checked_ids).delete()
            # Save overall instance comment
            service.notes = (request.POST.get("instance_comment") or "").strip()
            service.save(update_fields=["notes", "updated_at"])
            messages.success(request, "Attendance saved successfully.")
            return redirect("record_attendance", service_type=service_type, service_id=service.id)

        # Handle "Add visitor" - add new person as visitor and record attendance
        if "add_visitor" in request.POST:
            form = VisitorForm(request.POST)
            if form.is_valid():
                person = form.save(commit=False)
                person.title = Person.VISITOR
                person.first_visit_date = service_date
                person.save()
                Attendance.objects.create(
                    service=service,
                    person=person,
                    category=Attendance.VISITOR,
                    present=True,
                    is_first_time_visitor=True,
                )
                messages.success(request, f"Visitor '{person.full_name}' added and recorded.")
                return redirect("record_attendance", service_type=service_type, service_id=service.id)
        else:
            form = VisitorForm()
    else:
        form = VisitorForm()

    recorded_notes_map = dict(
        Attendance.objects.filter(service=service).values_list("person_id", "notes")
    )
    people_with_notes = [(p, recorded_notes_map.get(p.id, "") or "") for p in people]

    context = {
        "service_type": service_type,
        "service_type_label": service_type_label,
        "service": service,
        "service_date": service_date,
        "people": people,
        "people_with_notes": people_with_notes,
        "recorded_ids": recorded_ids,
        "person_form": form,
        "instance_display_name": _get_instance_display_name(service),
        "instance_comment": service.notes or "",
    }
    return render(request, "record_attendance.html", context)


@login_required
def event_instance_report_view(request, service_type, service_id):
    """
    View report for a specific event instance: attendees and their comments.
    """
    valid_types = [st[0] for st in SERVICE_TYPES]
    if service_type not in valid_types:
        messages.error(request, "Invalid event type.")
        return redirect("events")

    try:
        service = Service.objects.get(pk=service_id, service_type=service_type)
    except Service.DoesNotExist:
        messages.error(request, "Event instance not found.")
        return redirect("event_instances", service_type=service_type)

    attendances = (
        Attendance.objects.filter(service=service)
        .select_related("person")
        .order_by("person__full_name")
    )
    # Order by title hierarchy
    title_order = Case(
        When(person__title=Person.PROPHET, then=Value(1)),
        When(person__title=Person.GENERAL_OVERSEER, then=Value(2)),
        When(person__title=Person.SENIOR_ARCHBISHOP_EMERITUS, then=Value(3)),
        When(person__title=Person.SENIOR_ARCHBISHOP, then=Value(4)),
        When(person__title=Person.SENIOR_DEPUTY_ARCHBISHOP, then=Value(5)),
        When(person__title=Person.DEPUTY_ARCHBISHOP, then=Value(6)),
        When(person__title=Person.BISHOP, then=Value(7)),
        When(person__title=Person.OVERSEER, then=Value(8)),
        When(person__title=Person.SENIOR_PASTOR, then=Value(9)),
        When(person__title=Person.PASTOR, then=Value(10)),
        When(person__title=Person.SISTER, then=Value(11)),
        When(person__title=Person.BROTHER, then=Value(12)),
        When(person__title=Person.VISITOR, then=Value(13)),
        When(person__title=Person.EMPLOYEE, then=Value(14)),
        default=Value(99),
    )
    attendances = attendances.annotate(title_sort=title_order).order_by("title_sort", "person__full_name")

    context = {
        "service": service,
        "service_type": service_type,
        "service_type_label": dict(SERVICE_TYPES).get(service_type, service_type),
        "instance_display_name": _get_instance_display_name(service),
        "attendances": attendances,
    }
    return render(request, "reports/event_instance_report.html", context)


@login_required
def attendance_analysis_view(request, service_type, service_id):
    """
    Produce attendance analysis charts for a specific Service instance.
    Charts include:
    - Gender split (pie)
    - Age group distribution (bar)
    - Gender-by-age stacked bar
    - Attendance over time for the service type (line)
    - Frequency of appearance per person (histogram / bar)
    """
    # validate service_type
    valid_types = [st[0] for st in SERVICE_TYPES]
    if service_type not in valid_types:
        messages.error(request, "Invalid event type.")
        return redirect("events")

    service = get_object_or_404(Service, pk=service_id, service_type=service_type)

    # Attendances for this instance
    attendances = Attendance.objects.filter(service=service).select_related("person")

    # Gender counts for this instance
    gender_counts = {"male": 0, "female": 0}

    # Age group buckets
    age_buckets = [
        ("0_3", "Infants (0-3)"),
        ("4_12", "Sunday School (4-12)"),
        ("13_19", "Teens (13-19)"),
        ("20_35", "Youths (20-35)"),
        ("36_60", "Adults (36-60)"),
        ("60_80", "Seniors (60-80)"),
        ("80_plus", "Elderly (80+)")
    ]
    age_counts = {k: 0 for k, _ in age_buckets}
    # gender-by-age
    gender_age = {k: {"male": 0, "female": 0} for k, _ in age_buckets}

    def compute_age(dob):
        if not dob:
            return None
        return (date.today() - dob).days // 365

    for att in attendances:
        p = att.person
        g = (p.gender or "").lower() if p.gender else None
        if g in gender_counts:
            gender_counts[g] = gender_counts.get(g, 0) + 1

        age = compute_age(p.date_of_birth)
        if age is None:
            # ignore unknown ages in age distribution
            continue
        if age <= 3:
            bucket = "0_3"
        elif age <= 12:
            bucket = "4_12"
        elif age <= 19:
            bucket = "13_19"
        elif age <= 35:
            bucket = "20_35"
        elif age <= 60:
            bucket = "36_60"
        elif age <= 80:
            bucket = "60_80"
        else:
            bucket = "80_plus"

        age_counts[bucket] += 1
        gender_age[bucket][g] = gender_age[bucket].get(g, 0) + 1

    # Attendance over time for this service_type
    instances = Service.objects.filter(service_type=service_type).order_by("date", "start_time")
    time_labels = []
    time_counts = []
    for inst in instances:
        cnt = Attendance.objects.filter(service=inst).count()
        time_labels.append(inst.date.strftime("%A, %Y-%m-%d"))
        time_counts.append(cnt)

    # Frequency of appearance per person across all instances of this service_type
    # For each person who has ever attended this service_type, count how many instances
    persons = Person.objects.filter(attendances__service__service_type=service_type).distinct()
    freq_map = {}
    for p in persons:
        c = Attendance.objects.filter(person=p, service__service_type=service_type).values("service_id").distinct().count()
        freq_map[p.full_name] = c

    # Histogram buckets (number of instances -> how many people)
    freq_counts = {}
    for name, c in freq_map.items():
        freq_counts[c] = freq_counts.get(c, 0) + 1

    # For people in this specific instance, attach their frequency
    current_person_freq = []
    for att in attendances:
        name = att.person.full_name
        current_person_freq.append({"name": name, "count": freq_map.get(name, 0)})
    
    # Sort by count (highest to lowest)
    current_person_freq.sort(key=lambda x: x["count"], reverse=True)

    # Find persons in this instance with missing or unspecified gender
    missing_persons = []
    def infer_gender_for_person(p):
        # Use title hints first
        if p.title == Person.SISTER:
            return Person.FEMALE
        if p.title == Person.BROTHER:
            return Person.MALE
        # Fallback heuristic by first name ending (very naive)
        parts = (p.full_name or "").split()
        if parts:
            fn = parts[0].lower()
            if fn.endswith(('a','e','i','y')):
                return Person.FEMALE
            else:
                return Person.MALE
        return None

    for att in attendances:
        p = att.person
        if not p.gender or p.gender not in [Person.MALE, Person.FEMALE]:
            missing_persons.append({
                'id': p.id,
                'name': p.full_name,
                'inferred': infer_gender_for_person(p),
            })

    context = {
        "service": service,
        "service_type": service_type,
        "service_type_label": dict(SERVICE_TYPES).get(service_type, service_type),
        "instance_display_name": _get_instance_display_name(service),
        "gender_counts": gender_counts,
        "age_buckets": [label for _, label in age_buckets],
        "age_counts": [age_counts[k] for k, _ in age_buckets],
        "gender_age": gender_age,
        "time_labels": time_labels,
        "time_counts": time_counts,
        "freq_map": freq_map,
        "freq_counts": freq_counts,
        "current_person_freq": current_person_freq,
        "missing_persons": missing_persons,
    }

    return render(request, "reports/event_instance_analysis.html", context)


@login_required
def set_gender(request):
    """API endpoint to set a person's gender. Expects POST with JSON or form data: person_id, gender ('male'|'female')."""
    if request.method != 'POST':
        return HttpResponseBadRequest('POST required')
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        data = request.POST
    person_id = data.get('person_id') or request.POST.get('person_id')
    gender = data.get('gender') or request.POST.get('gender')
    if not person_id or not gender:
        return HttpResponseBadRequest('person_id and gender required')
    if gender not in [Person.MALE, Person.FEMALE]:
        return HttpResponseBadRequest('invalid gender')
    try:
        person = Person.objects.get(pk=int(person_id))
    except Person.DoesNotExist:
        return HttpResponseBadRequest('person not found')
    person.gender = gender
    person.save()
    return JsonResponse({'ok': True, 'person_id': person.id, 'gender': person.gender})


@login_required
def dashboard_view(request):
    """
    Simple HTML dashboard using Django templates and Bootstrap.
    """
    week_start, week_end = _get_date_range_from_query_params(request)

    qs = Attendance.objects.filter(
        service__date__gte=week_start,
        service__date__lte=week_end,
    )

    total_attendance = qs.count()
    visitors_count = qs.filter(category=Attendance.VISITOR).count()
    healed_count = qs.filter(category=Attendance.HEALED).count()

    follow_up_count = FollowUpCase.objects.filter(
        status__in=[FollowUpCase.STATUS_OPEN, FollowUpCase.STATUS_IN_PROGRESS],
        created_at__date__lte=week_end,
    ).count()

    # For the simplified dashboard we only surface counts; charts removed.
    context = {
        "week_start": week_start,
        "week_end": week_end,
        "total_attendance": total_attendance,
        "visitors_count": visitors_count,
        "healed_count": healed_count,
        "follow_up_count": follow_up_count,
    }

    return render(request, "dashboard.html", context)

