from django.contrib import admin
from .models import BusinessPlan, StartupIdea, StartupProject


@admin.register(StartupIdea)
class StartupIdeaAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "industry", "created_at")
    list_filter = ("industry", "created_at")
    search_fields = ("idea", "user__username", "user__email")
    readonly_fields = ("created_at",)


@admin.register(BusinessPlan)
class BusinessPlanAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "industry", "created_at", "updated_at")
    list_filter = ("industry", "created_at")
    search_fields = ("business_idea", "user__username")
    readonly_fields = ("created_at", "updated_at")


@admin.register(StartupProject)
class StartupProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user", "stage", "industry", "updated_at")
    list_filter = ("stage", "industry", "updated_at")
    search_fields = ("name", "description", "user__username", "user__email")
    readonly_fields = ("created_at", "updated_at")
