from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from core.models import (
    IOC,
    TTP,
    Artifact,
    ArtifactTag,
    Case,
    CaseTTP,
    CorrelationResult,
    DumpUpload,
    EvidenceSource,
    Incident,
    IncidentMalware,
    IncidentThreatActor,
    Malware,
    Notification,
    Tag,
    ThreatActor,
    ThreatIntelFeed,
    ThreatIntelIOC,
    UserNotification,
)
from core.serializers import (
    ArtifactSerializer,
    ArtifactTagSerializer,
    CaseSerializer,
    CaseTTPSerializer,
    CorrelationResultSerializer,
    DumpUploadSerializer,
    EvidenceSourceSerializer,
    IncidentMalwareSerializer,
    IncidentSerializer,
    IncidentThreatActorSerializer,
    IOCSerializer,
    MalwareSerializer,
    NotificationSerializer,
    TagSerializer,
    ThreatActorSerializer,
    ThreatIntelFeedSerializer,
    ThreatIntelIOCSerializer,
    TTPSerializer,
    UserNotificationSerializer,
)


class IncidentViewSet(viewsets.ModelViewSet):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["status", "severity", "classification"]
    search_fields = ["title", "description"]
    ordering_fields = ["created_date", "modified_date", "severity"]
    ordering = ["-created_date"]
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["get"])
    def cases(self, request, pk=None):
        incident = self.get_object()
        cases = incident.cases.all()
        serializer = CaseSerializer(cases, many=True, context={"request": request})
        return Response(serializer.data)


class CaseViewSet(viewsets.ModelViewSet):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["status", "incident"]
    search_fields = ["title", "description"]
    ordering_fields = ["created_date", "modified_date"]
    ordering = ["-created_date"]
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["get"])
    def evidence_sources(self, request, pk=None):
        case = self.get_object()
        evidence_sources = case.evidence_sources.all()
        serializer = EvidenceSourceSerializer(
            evidence_sources, many=True, context={"request": request}
        )
        return Response(serializer.data)


class EvidenceSourceViewSet(viewsets.ModelViewSet):
    queryset = EvidenceSource.objects.all()
    serializer_class = EvidenceSourceSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["type", "case"]
    search_fields = ["name", "description"]
    ordering_fields = ["acquisition_date", "created_date"]
    ordering = ["-acquisition_date"]
    permission_classes = [IsAuthenticated]


class ArtifactViewSet(viewsets.ModelViewSet):
    queryset = Artifact.objects.all()
    serializer_class = ArtifactSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["type", "is_suspicious", "source"]
    search_fields = ["name", "path"]
    ordering_fields = ["created_date", "modified_date", "size"]
    ordering = ["-created_date"]
    permission_classes = [IsAuthenticated]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]
    permission_classes = [IsAuthenticated]


class ArtifactTagViewSet(viewsets.ModelViewSet):
    queryset = ArtifactTag.objects.all()
    serializer_class = ArtifactTagSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["artifact", "tag"]
    permission_classes = [IsAuthenticated]


class IOCViewSet(viewsets.ModelViewSet):
    queryset = IOC.objects.all()
    serializer_class = IOCSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["type", "tlp", "confidence", "case"]
    search_fields = ["value", "description"]
    ordering_fields = ["created_date", "first_seen", "last_seen"]
    ordering = ["-created_date"]
    permission_classes = [IsAuthenticated]


class TTPViewSet(viewsets.ModelViewSet):
    queryset = TTP.objects.all()
    serializer_class = TTPSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["tactic"]
    search_fields = ["technique_id", "name"]
    permission_classes = [IsAuthenticated]


class CaseTTPViewSet(viewsets.ModelViewSet):
    queryset = CaseTTP.objects.all()
    serializer_class = CaseTTPSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["case", "ttp"]
    permission_classes = [IsAuthenticated]


class ThreatActorViewSet(viewsets.ModelViewSet):
    queryset = ThreatActor.objects.all()
    serializer_class = ThreatActorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["origin"]
    search_fields = ["name", "aliases", "description"]
    permission_classes = [IsAuthenticated]


class IncidentThreatActorViewSet(viewsets.ModelViewSet):
    queryset = IncidentThreatActor.objects.all()
    serializer_class = IncidentThreatActorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["incident", "threat_actor"]
    permission_classes = [IsAuthenticated]


class MalwareViewSet(viewsets.ModelViewSet):
    queryset = Malware.objects.all()
    serializer_class = MalwareSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["type"]
    search_fields = ["name", "aliases", "description"]
    permission_classes = [IsAuthenticated]


class IncidentMalwareViewSet(viewsets.ModelViewSet):
    queryset = IncidentMalware.objects.all()
    serializer_class = IncidentMalwareSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["incident", "malware"]
    permission_classes = [IsAuthenticated]


class DumpUploadViewSet(viewsets.ModelViewSet):
    queryset = DumpUpload.objects.all()
    serializer_class = DumpUploadSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["dump_type", "status"]
    ordering_fields = ["upload_date"]
    ordering = ["-upload_date"]
    permission_classes = [IsAuthenticated]


class ThreatIntelFeedViewSet(viewsets.ModelViewSet):
    queryset = ThreatIntelFeed.objects.all()
    serializer_class = ThreatIntelFeedSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["feed_type", "status"]
    search_fields = ["name", "description"]
    permission_classes = [IsAuthenticated]


class ThreatIntelIOCViewSet(viewsets.ModelViewSet):
    queryset = ThreatIntelIOC.objects.all()
    serializer_class = ThreatIntelIOCSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["type", "tlp", "confidence", "severity", "feed"]
    search_fields = ["value", "description"]
    ordering_fields = ["created_date", "first_seen", "last_seen"]
    ordering = ["-created_date"]
    permission_classes = [IsAuthenticated]


class CorrelationResultViewSet(viewsets.ModelViewSet):
    queryset = CorrelationResult.objects.all()
    serializer_class = CorrelationResultSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["correlation_type", "severity", "is_false_positive"]
    ordering_fields = ["detected_date"]
    ordering = ["-detected_date"]
    permission_classes = [IsAuthenticated]


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["notification_type", "severity", "is_read"]
    ordering_fields = ["created_date"]
    ordering = ["-created_date"]
    permission_classes = [IsAuthenticated]


class UserNotificationViewSet(viewsets.ModelViewSet):
    queryset = UserNotification.objects.all()
    serializer_class = UserNotificationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["user", "is_read"]
    permission_classes = [IsAuthenticated]
