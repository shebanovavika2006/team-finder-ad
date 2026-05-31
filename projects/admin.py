from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("name", "description", "owner__email")
    raw_id_fields = ("owner",)
    date_hierarchy = "created_at"  # Добавлен удобный фильтр по датам
    empty_value_display = "-пусто-" # Обработка пустых полей
