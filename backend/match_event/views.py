from django.http import Http404
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from clients.acb import ACBClient

from .models import MatchEvent
from .serializers import (
    GameBiggestLeadSerializer,
    GameLeadersSerializer,
    PBPLeanSerializer,
)


class ACBGenericAPIView(GenericAPIView):
    """
    Base view which retrieves the `QuerySet` corresponding to the `game_id` path param
    """

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        game_id = self.kwargs["game_id"]
        qs = MatchEvent.objects.filter(game_id=game_id)
        if not qs.exists():
            client = ACBClient()
            match_events = client.get_match_events(game_id=game_id)
            MatchEvent.objects.bulk_create(match_events)
            qs = MatchEvent.objects.filter(game_id=game_id)
        if not qs.exists():
            raise Http404('"game_id" not found.')
        return qs


class PBPLeanAPIView(ACBGenericAPIView):
    """
    For a given `game_id`, retrieve the list of `MatchEvent`
    """

    serializer_class = PBPLeanSerializer

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset().order_by("action_time")

        data = {"match_events": list(qs.values())}

        serializer = self.serializer_class(data=data)
        serializer.is_valid()

        return Response(serializer.data, status=status.HTTP_200_OK)


class GameLeadersAPIView(ACBGenericAPIView):
    """
    For a given `game_id`, retrieve the lists of points and rebounds by each player
    in descending order
    """

    serializer_class = GameLeadersSerializer

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        qs_home = qs.filter(is_home_team=True)
        qs_away = qs.filter(is_home_team=False)

        data = {
            "home_team_leaders": {
                "points": list(
                    qs_home.points_leaders().values("player_license_id", "total")
                ),
                "rebounds": list(
                    qs_home.rebounds_leaders().values("player_license_id", "total")
                ),
            },
            "away_team_leaders": {
                "points": list(
                    qs_away.points_leaders().values("player_license_id", "total")
                ),
                "rebounds": list(
                    qs_away.rebounds_leaders().values("player_license_id", "total")
                ),
            },
        }

        serializer = self.serializer_class(data=data)
        serializer.is_valid()

        return Response(serializer.data, status=status.HTTP_200_OK)


class GameBiggestLeadAPIView(ACBGenericAPIView):
    """
    For a given `game_id`, retrieve the biggest lead by each each team
    """

    serializer_class = GameBiggestLeadSerializer

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        qs = qs.with_differences()

        data = {"home_team": qs.first().difference, "away_team": -qs.last().difference}

        serializer = self.serializer_class(data=data)
        serializer.is_valid()

        return Response(serializer.data, status=status.HTTP_200_OK)
