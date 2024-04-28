from django.db import models
from django.db.models import F, Max


class MatchEventQuerySet(models.QuerySet):
    def with_differences(self):
        """
        Decorate QuerySet with the difference in points according to
        `score_home_team` and `score_away_team`
        """
        qs = self.annotate(difference=F("score_home_team") - F("score_away_team"))
        return qs.order_by("-difference")

    def points_leaders(self):
        """
        Group by `player_license_id` with the max corresponding points
        """
        qs = self.filter(player_license_id__isnull=False, player_points__isnull=False)
        qs = qs.values("player_license_id").order_by("player_license_id")
        qs = qs.annotate(total=Max("player_points"))
        qs = qs.order_by("-total")
        return qs

    def rebounds_leaders(self):
        """
        Group by `player_license_id` with the max corresponding rebounds
        """
        qs = self.filter(player_license_id__isnull=False, player_rebounds__isnull=False)
        qs = qs.values("player_license_id").order_by("player_license_id")
        qs = qs.annotate(total=Max("player_rebounds"))
        qs = qs.order_by("-total")
        return qs


class MatchEvent(models.Model):
    game_id = models.BigIntegerField(db_index=True)
    team_id = models.BigIntegerField(null=True, blank=True)
    player_license_id = models.BigIntegerField(null=True, blank=True)
    player_points = models.IntegerField(null=True, blank=True)
    player_rebounds = models.IntegerField(null=True, blank=True)
    action_time = models.TimeField(db_index=True)
    action_type = models.IntegerField(db_index=True)
    is_home_team = models.BooleanField()
    score_home_team = models.IntegerField()
    score_away_team = models.IntegerField()

    objects = MatchEventQuerySet.as_manager()
