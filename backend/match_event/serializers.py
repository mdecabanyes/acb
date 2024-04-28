from rest_framework import serializers

from .models import MatchEvent


class MatchEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchEvent
        fields = ("team_id", "player_license_id", "action_time", "action_type")


class PBPLeanSerializer(serializers.Serializer):
    match_events = MatchEventSerializer(many=True)


class PlayerGameLeadersSerializer(serializers.Serializer):
    player_license_id = serializers.IntegerField()
    total = serializers.IntegerField()


class TeamGameLeadersSerializer(serializers.Serializer):
    points = PlayerGameLeadersSerializer(many=True)
    rebounds = PlayerGameLeadersSerializer(many=True)


class GameLeadersSerializer(serializers.Serializer):
    home_team_leaders = TeamGameLeadersSerializer()
    away_team_leaders = TeamGameLeadersSerializer()


class GameBiggestLeadSerializer(serializers.Serializer):
    home_team = serializers.IntegerField()
    away_team = serializers.IntegerField()
