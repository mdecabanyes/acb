from django.contrib import admin

from .models import MatchEvent, MatchEventActionType


@admin.register(MatchEventActionType)
class MatchEventActionTypeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "normalized_description",
    )
    ordering = ("normalized_description",)


@admin.register(MatchEvent)
class MatchEventAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "game_id",
        "team_id",
        "player_license_id",
        "action_time",
        "action_type",
    )
    ordering = ("action_time",)
