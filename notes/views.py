"""
Views for Note API.
"""
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Note
from .serializers import NoteSerializer, NoteDetailSerializer


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                "notes",
                OpenApiTypes.STR,
                description="Comma separated list of IDs to filter.",
            )
        ]
    )
)
class NoteViewSet(viewsets.ModelViewSet):
    """View for manage note APIs."""

    serializer_class = NoteSerializer
    queryset = Note.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def _params_to_ints(self, qs):
        """Convert a list of strings to integers."""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        """Retrieve notes for authenticated user."""
        queryset = self.queryset

        return queryset.filter(
            user=self.request.user
            ).order_by("-id").distinct()

    def perform_create(self, serializer):
        """Create a new note."""
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        """Return appropriate serializer class based on the request method."""
        if self.request.method in ["GET", "HEAD"]:
            return NoteDetailSerializer
        else:
            return NoteSerializer


@api_view(["GET"])
def health_check(request):
    """Returns successful response."""
    return Response({"healthy": True})
