from django.urls import path

from rest_framework.authtoken import views

from user.views import CreateUserView, CustomAuthToken

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("token/", CustomAuthToken.as_view(), name="token"),
]

app_name = "user"
