# from clients.acb import ACBApiClient
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from .models import MatchEvent
from .serializers import MatchEventSerializer


class MatchEventListAPIView(ListAPIView):
    model = MatchEvent
    serializer_class = MatchEventSerializer
    ordering = ("action_time",)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        game_id = self.kwargs["game_id"]
        match_events = MatchEvent.objects.filter(game_id=game_id)
        # if not match_events:
        #     client = ACBApiClient()
        #     match_events_api = client.get_match_events(game_id=game_id)
        #     print(match_events_api)
        return match_events
