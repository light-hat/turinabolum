from rest_framework import routers
from rest import views

router = routers.DefaultRouter()

router.register(r'incidents', views.IncidentViewSet)
router.register(r'cases', views.CaseViewSet)
router.register(r'evidence-sources', views.EvidenceSourceViewSet)
router.register(r'artifacts', views.ArtifactViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'artifact-tags', views.ArtifactTagViewSet)
router.register(r'iocs', views.IOCViewSet)
router.register(r'ttps', views.TTPViewSet)
router.register(r'case-ttps', views.CaseTTPViewSet)
router.register(r'threat-actors', views.ThreatActorViewSet)
router.register(r'incident-threat-actors', views.IncidentThreatActorViewSet)
router.register(r'malware', views.MalwareViewSet)
router.register(r'incident-malware', views.IncidentMalwareViewSet)
router.register(r'dump-uploads', views.DumpUploadViewSet)
router.register(r'threat-intel-feeds', views.ThreatIntelFeedViewSet)
router.register(r'threat-intel-iocs', views.ThreatIntelIOCViewSet)
router.register(r'correlation-results', views.CorrelationResultViewSet)
router.register(r'notifications', views.NotificationViewSet)
router.register(r'user-notifications', views.UserNotificationViewSet)

urlpatterns = router.urls
