from django.db import models
from django.db.models import Case, Count, F, IntegerField, Q, Sum, Value, When


class MatchEventQuerySet(models.QuerySet):
    def with_points(self):
        """
        Decorate QuerySet with the corresponding points according to its
        `action_type`
        """
        conditions = [
            When(action_type=MatchEvent.ONE_POINTS_ACTION_TYPE, then=Value(1)),
            When(action_type=MatchEvent.TWO_POINTS_ACTION_TYPE, then=Value(2)),
            When(action_type=MatchEvent.THREE_POINTS_ACTION_TYPE, then=Value(3)),
        ]
        return self.annotate(
            points=Case(
                *conditions,
                default=Value(0),
                output_field=IntegerField(),
            )
        )

    def with_differences(self):
        """
        Decorate QuerySet with the difference in points according to
        `score_home_team` and `score_away_team`
        """
        qs = self.filter(
            Q(action_type=MatchEvent.ONE_POINTS_ACTION_TYPE)
            | Q(action_type=MatchEvent.TWO_POINTS_ACTION_TYPE)
            | Q(action_type=MatchEvent.THREE_POINTS_ACTION_TYPE)
        )
        qs = self.annotate(difference=F("score_home_team") - F("score_away_team"))
        return qs.order_by("-difference")

    def points_leaders(self):
        """
        Group by `player_license_id adding` up the corresponding points
        """
        qs = self.filter(
            Q(action_type=MatchEvent.ONE_POINTS_ACTION_TYPE)
            | Q(action_type=MatchEvent.TWO_POINTS_ACTION_TYPE)
            | Q(action_type=MatchEvent.THREE_POINTS_ACTION_TYPE)
        )
        qs = qs.with_points()
        qs = qs.filter(player_license_id__isnull=False)
        qs = qs.values("player_license_id").order_by("player_license_id")
        qs = qs.annotate(total=Sum("points"))
        qs = qs.order_by("-total")
        return qs

    def rebounds_leaders(self):
        """
        Group by `player_license_id` counting up the number of rebounds
        """
        qs = self.filter(
            Q(action_type=MatchEvent.OFFENSIVE_REBOUND_ACTION_TYPE)
            | Q(action_type=MatchEvent.DEFFENSIVE_REBOUND_ACTION_TYPE)
        )
        qs = qs.filter(player_license_id__isnull=False)
        qs = qs.values("player_license_id").order_by("player_license_id")
        qs = qs.annotate(total=Count("player_license_id"))
        qs = qs.order_by("-total")
        return qs


class MatchEvent(models.Model):
    ONE_POINTS_ACTION_TYPE = 92
    TWO_POINTS_ACTION_TYPE = 93
    THREE_POINTS_ACTION_TYPE = 94

    OFFENSIVE_REBOUND_ACTION_TYPE = 101
    DEFFENSIVE_REBOUND_ACTION_TYPE = 104

    game_id = models.BigIntegerField(db_index=True)
    team_id = models.BigIntegerField(null=True, blank=True)
    player_license_id = models.BigIntegerField(null=True, blank=True)
    action_time = models.TimeField(db_index=True)
    action_type = models.IntegerField(db_index=True)
    is_home_team = models.BooleanField()
    score_home_team = models.IntegerField()
    score_away_team = models.IntegerField()

    objects = MatchEventQuerySet.as_manager()
