from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework import routers

from post.views import PostViewSet


router = routers.DefaultRouter()

router.register(r"post-list", PostViewSet, basename="post-detail")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "post-list/<int:pk>/like-toggle/",
        PostViewSet.as_view({"post": "toggle_like"}),
        name="post-toggle-like",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

app_name = "post"
