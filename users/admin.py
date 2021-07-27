from users.models import UserCredential
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()


class UserAdmin(UserAdmin):
    search_fields = ("username", "email",)
    list_filter = ("voted", "credentials_sent", "campus",)
    list_display = ("username", "campus", "email", "voted", "credentials_sent", "is_staff", "is_superuser")
    readonly_fields = ("password", "voted", "date_joined", "last_login", "user_permissions", )
    


admin.site.register(User, UserAdmin)


@admin.register(UserCredential)
class UserCredentialAdmin(admin.ModelAdmin):
    list_display = ["student_id", "email", "campus"]
    search_fields = ["student_id", "email"]
    list_filter = ["campus"]