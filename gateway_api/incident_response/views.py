from django_filters.rest_framework import DjangoFilterBackend
from incident_response.models import *
from incident_response.serializers import *
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response


class CaseViewSet(viewsets.ModelViewSet):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["status", "tlp"]
    search_fields = ["title", "description"]
    ordering_fields = ["created_date", "modified_date"]
    ordering = ["-created_date"]
    permission_classes = [IsAuthenticated]
