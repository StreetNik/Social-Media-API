from django.contrib import admin
from user.models import User, Profile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Profile)
class Profile(admin.ModelAdmin):
    pass
