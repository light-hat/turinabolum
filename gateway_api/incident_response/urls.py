from rest import views
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r"cases", views.CaseViewSet)

urlpatterns = router.urls
