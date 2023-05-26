from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from user.views import (
    CreateUserView,
    CreateTokenView,
    LogOutView,
    UserProfileView,
    UsersListView,
)

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("token/", CreateTokenView.as_view(), name="token"),
    path("logout/", LogOutView.as_view(), name="logout"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("users-list/", UsersListView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

app_name = "user"
