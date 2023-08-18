from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

from post.views import PostViewSet


router = routers.DefaultRouter()

router.register(r"post-list", PostViewSet, basename="post-detail")

urlpatterns = [] + router.urls + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

app_name = "post"
