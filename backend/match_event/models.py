from django.db import models


class MatchEventActionType(models.Model):
    normalized_description = models.CharField(max_length=512)


class MatchEvent(models.Model):
    game_id = models.BigIntegerField()
    team_id = models.BigIntegerField()
    player_license_id = models.BigIntegerField()
    action_time = models.DurationField()
    action_type = models.ForeignKey(MatchEventActionType, on_delete=models.CASCADE)
