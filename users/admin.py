from django.contrib import admin
from django.conf import settings
from .models import User

class UserAdmin(admin.ModelAdmin):
    search_fields = ("username", "email",)
    list_filter = ("voted",)
    list_display = ("username", "first_name", "last_name", "email", "voted",)
    readonly_fields = ("password", "voted",)


admin.site.register(User, UserAdmin)