from django.contrib import admin

from .models import ElectoralCommisionMember


@admin.register(ElectoralCommisionMember)
class ElectoralCommisionMemberAdmin(admin.ModelAdmin):
    list_display = ["name", "image_tag"]