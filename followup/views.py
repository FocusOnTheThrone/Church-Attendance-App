from datetime import date, timedelta

from django.db.models import Max, Q
from django.utils.dateparse import parse_date
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as http_status

from attendance.models import Person
from .models import FollowUpCase
from .serializers import FollowUpCaseSerializer


class FollowUpCaseViewSet(viewsets.ModelViewSet):
    """
    CRUD API for follow-up cases.
    """

    queryset = FollowUpCase.objects.select_related("person", "assigned_to")
    serializer_class = FollowUpCaseSerializer
    permission_classes = [permissions.IsAuthenticated]


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

        # Last seen date per person (based on Attendance -> Service.date)
        people = Person.objects.annotate(last_seen=Max("attendances__service__date"))

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
