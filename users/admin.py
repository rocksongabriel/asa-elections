from users.models import UserCredential
from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    search_fields = ("username", "email",)
    list_filter = ("voted",)
    list_display = ("username", "first_name", "last_name", "campus", "email", "voted",)
    readonly_fields = ("password", "voted",)
    


admin.site.register(User, UserAdmin)


@admin.register(UserCredential)
class UserCredentialAdmin(admin.ModelAdmin):
    list_display = ["student_id", "email", "campus"]
    search_fields = ["student_id", "email"]
    list_filter = ["campus"]