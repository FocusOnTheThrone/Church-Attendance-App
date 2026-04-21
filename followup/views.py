from datetime import date, timedelta

from django.db.models import Max, Q
from django.utils.dateparse import parse_date
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as http_status
import json

from attendance.models import Person, Service
from .models import FollowUpCase, FollowUpRecord
from .serializers import FollowUpCaseSerializer


class FollowUpCaseViewSet(viewsets.ModelViewSet):
    """
    CRUD API for follow-up cases. Scoped to the user's organization.
    """

    serializer_class = FollowUpCaseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = FollowUpCase.objects.select_related("person", "assigned_to")
        org = getattr(self.request.user, 'organization', None)
        if org:
            qs = qs.filter(person__organization=org)
        return qs


class FollowUpSuggestionsView(APIView):
    """
    Suggest people to follow up on because they have not come to church.

    Query params:
    - weeks: integer (default 3)
    - as_of: YYYY-MM-DD (default today)
    - include_never_attended: true/false (default false)
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        weeks_str = request.query_params.get("weeks", "3")
        as_of_str = request.query_params.get("as_of")
        include_never_attended = request.query_params.get("include_never_attended", "false").lower() == "true"

        try:
            weeks = int(weeks_str)
            if weeks < 1:
                raise ValueError
        except ValueError:
            return Response({"detail": "weeks must be a positive integer."}, status=http_status.HTTP_400_BAD_REQUEST)

        as_of = parse_date(as_of_str) if as_of_str else date.today()
        if as_of is None:
            return Response({"detail": "as_of must be in YYYY-MM-DD format."}, status=http_status.HTTP_400_BAD_REQUEST)

        cutoff = as_of - timedelta(days=weeks * 7)
        org = getattr(request.user, 'organization', None)

        # Last seen date per person (based on Attendance -> Service.date)
        people = Person.objects.annotate(last_seen=Max("attendances__service__date"))
        if org:
            people = people.filter(organization=org)

        if include_never_attended:
            people = people.filter(Q(last_seen__lt=cutoff) | Q(last_seen__isnull=True))
        else:
            people = people.filter(last_seen__lt=cutoff)

        # Exclude people who already have an open/in-progress follow-up case
        people = people.exclude(
            followup_cases__status__in=[FollowUpCase.STATUS_OPEN, FollowUpCase.STATUS_IN_PROGRESS]
        ).distinct()

        results = [
            {
                "person_id": p.id,
                "full_name": p.full_name,
                "phone": p.phone,
                "email": p.email,
                "status": p.status,
                "last_seen": p.last_seen,
            }
            for p in people.order_by("full_name")
        ]

        return Response(
            {
                "as_of": as_of,
                "weeks": weeks,
                "cutoff": cutoff,
                "count": len(results),
                "results": results,
            }
        )


class GenerateFollowUpCasesView(APIView):
    """
    Create follow-up cases for people who are absent for N weeks.

    POST body (JSON):
    - person_ids: [1,2,3] (required)
    - reason: \"absent_N_weeks\" or \"manual\" (optional)
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        person_ids = request.data.get("person_ids")
        reason = request.data.get("reason", FollowUpCase.REASON_ABSENT)

        if not isinstance(person_ids, list) or not all(isinstance(x, int) for x in person_ids):
            return Response(
                {"detail": "person_ids must be a list of integers."},
                status=http_status.HTTP_400_BAD_REQUEST,
            )

        if reason not in dict(FollowUpCase.REASON_CHOICES):
            return Response(
                {"detail": f"reason must be one of: {list(dict(FollowUpCase.REASON_CHOICES).keys())}"},
                status=http_status.HTTP_400_BAD_REQUEST,
            )

        created = 0
        skipped_existing = 0

        for pid in person_ids:
            exists = FollowUpCase.objects.filter(
                person_id=pid,
                status__in=[FollowUpCase.STATUS_OPEN, FollowUpCase.STATUS_IN_PROGRESS],
            ).exists()
            if exists:
                skipped_existing += 1
                continue

            FollowUpCase.objects.create(
                person_id=pid,
                reason=reason,
                status=FollowUpCase.STATUS_OPEN,
            )
            created += 1

        return Response(
            {"created": created, "skipped_existing": skipped_existing},
            status=http_status.HTTP_201_CREATED,
        )


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def batch_create_followup(request):
    """
    API endpoint to create multiple follow-up records at once.
    Called from dashboard when user saves follow-up checkboxes and comments.
    """
    try:
        data = json.loads(request.body)
        followups = data.get('followups', [])
        
        if not followups:
            return JsonResponse({'success': False, 'error': 'No follow-up data provided'})
        
        created_count = 0
        
        for followup_data in followups:
            person_id = followup_data.get('person_id')
            service_id = followup_data.get('service_id')
            comments = followup_data.get('comments', '')
            is_completed = followup_data.get('is_completed', False)
            
            # Validate required fields
            if not person_id or not service_id:
                continue
                
            # Get objects
            person = get_object_or_404(Person, id=person_id)
            service = get_object_or_404(Service, id=service_id)
            
            # Create or get follow-up case
            followup_case, created = FollowUpCase.objects.get_or_create(
                person=person,
                reason=FollowUpCase.REASON_ABSENT,
                defaults={'status': FollowUpCase.STATUS_OPEN}
            )
            
            # Check if follow-up record already exists for this person and service
            existing_record = FollowUpRecord.objects.filter(
                person=person,
                service=service
            ).first()
            
            if existing_record:
                # Update existing record
                existing_record.comments = comments
                existing_record.is_completed = is_completed
                existing_record.contacted_by = request.user
                existing_record.follow_up_date = timezone.now().date()
                if is_completed and not existing_record.completed_at:
                    existing_record.completed_at = timezone.now()
                existing_record.save()
                created_count += 1
            else:
                # Create new record
                FollowUpRecord.objects.create(
                    person=person,
                    service=service,
                    followup_case=followup_case,
                    contacted_by=request.user,
                    comments=comments,
                    is_completed=is_completed,
                    follow_up_date=timezone.now().date(),
                    outcome=FollowUpRecord.OUTCOME_SUCCESSFUL if is_completed else FollowUpRecord.OUTCOME_PENDING
                )
                created_count += 1
        
        return JsonResponse({
            'success': True,
            'created_count': created_count,
            'message': f'Successfully created/updated {created_count} follow-up records'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON data'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
