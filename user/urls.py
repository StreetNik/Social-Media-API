from django.urls import path

from user.views import CreateUserView, CreateTokenView, LogOutView

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("token/", CreateTokenView.as_view(), name="token"),
    path("logout/", LogOutView.as_view(), name="logout"),
]

app_name = "user"
