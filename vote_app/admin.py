from django.contrib import admin
from .models import Candidate, Category, PageControlPanel, Support


class CandidateInline(admin.TabularInline):
    model = Candidate
    extra = 0
    min_num = 1
    show_change_link = True

    readonly_fields = ("number_of_votes", )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [CandidateInline, ]
    list_display = ["name",]
    readonly_fields = ("slug", "voters")


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ("full_name", "image_tag", "category", "number_of_votes",)
    readonly_fields = ("number_of_votes",)


@admin.register(Support)
class SupportAdmin(admin.ModelAdmin):
    list_display = ("full_name", "student_id", "email_address",)
    search_fields = ("full_name", "student_id", "email_address",)
    readonly_fields = ("full_name", "student_id", "email_address", "message",)


@admin.register(PageControlPanel)
class PageControlPanelAdmin(admin.ModelAdmin):
    list_display = ("name", "enable_voting_page", "enable_results_page",)