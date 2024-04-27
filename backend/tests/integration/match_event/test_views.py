from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from match_event.models import MatchEvent, MatchEventActionType


class MatchEventListAPIViewTest(APITestCase):
    def setUp(self) -> None:
        self.game_id = 1
        self.match_event = MatchEvent.objects.create(
            game_id=self.game_id,
            team_id=2,
            player_license_id=3,
            action_time="00:10:00",
            action_type=MatchEventActionType.objects.create(normalized_description="Some type"),
        )
        self.user = User.objects.create(username="test", password="12345")

    def test_unauthenticated(self):
        url = reverse("match_event_list", args=(self.game_id,))
        result = self.client.get(url)

        self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_match_events_list(self):
        self.client.force_authenticate(user=self.user)

        url = reverse("match_event_list", args=(self.game_id,))
        result = self.client.get(url)

        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(len(result.json()), 1)
