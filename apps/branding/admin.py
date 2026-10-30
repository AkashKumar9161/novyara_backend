from django.contrib import admin

from .models import SavedBrand


@admin.register(SavedBrand)
class SavedBrandAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "industry", "created_at")
    search_fields = ("meaning", "name", "industry")
    readonly_fields = ("created_at",)
from .models import LogoDesign


@admin.register(LogoDesign)
class LogoDesignAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "industry", "style", "palette", "updated_at")
    search_fields = ("name", "industry", "tagline", "user__username")
    list_filter = ("style", "palette", "symbol")
    readonly_fields = ("created_at", "updated_at")
