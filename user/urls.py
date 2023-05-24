from django.urls import path

from user.views import CreateUserView, CreateTokenView

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("token/", CreateTokenView.as_view(), name="token"),
]

app_name = "user"
