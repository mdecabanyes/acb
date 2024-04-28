from django.contrib import admin

from .models import MatchEvent


@admin.register(MatchEvent)
class MatchEventAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "game_id",
        "team_id",
        "player_license_id",
        "action_type",
        "score_home_team",
        "score_away_team",
    )
