from rest_framework import serializers

from .models import MatchEvent


class MatchEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchEvent
        fields = "__all__"
