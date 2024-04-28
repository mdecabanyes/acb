import json
import os
from unittest import mock

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from base.settings import BASE_DIR
from clients.acb import ACBClient
from match_event.models import MatchEvent

FIXTURE_PATH = os.path.join(BASE_DIR, "tests", "fixtures", "match_events.json")


class GameAPIViewTest(APITestCase):
    def setUp(self) -> None:
        self.game_id = 1

        with open(FIXTURE_PATH, "r") as file:
            match_events = json.load(file)

        MatchEvent.objects.bulk_create(
            ACBClient._parse_match_event(match_event) for match_event in match_events
        )

        self.user = User.objects.create(username="test", password="12345")

    def test_unauthenticated(self):
        url = reverse("pbp_lean", args=(self.game_id,))
        result = self.client.get(url)

        self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)

    @mock.patch(
        "match_event.views.ACBClient.get_match_events", mock.MagicMock(return_value=[])
    )
    def test_not_found(self):
        self.client.force_authenticate(user=self.user)

        game_id = 2
        url = reverse("pbp_lean", args=(game_id,))
        result = self.client.get(url)

        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)

    @mock.patch("match_event.views.ACBClient.get_match_events")
    def test_load_from_database(self, mock_get_match_events):
        self.client.force_authenticate(user=self.user)

        game_id = 1
        url = reverse("pbp_lean", args=(game_id,))
        result = self.client.get(url)

        self.assertEqual(result.status_code, status.HTTP_200_OK)
        mock_get_match_events.assert_not_called()

    def test_get_pbp_lean(self):
        self.client.force_authenticate(user=self.user)

        url = reverse("pbp_lean", args=(self.game_id,))
        result = self.client.get(url)

        self.assertEqual(result.status_code, status.HTTP_200_OK)
        data = result.json()
        self.assertIn("match_events", data)
        self.assertEqual(len(data["match_events"]), 137)
        self.assertIn("team_id", data["match_events"][0])
        self.assertIn("player_license_id", data["match_events"][0])
        self.assertIn("action_time", data["match_events"][0])
        self.assertIn("action_type", data["match_events"][0])

    def test_get_game_leaders(self):
        self.client.force_authenticate(user=self.user)

        url = reverse("game_leaders", args=(self.game_id,))
        result = self.client.get(url)

        self.assertEqual(result.status_code, status.HTTP_200_OK)
        data = result.json()
        self.assertIn("home_team_leaders", data)
        self.assertIn("away_team_leaders", data)
        self.assertIn("points", data["home_team_leaders"])
        self.assertIn("rebounds", data["home_team_leaders"])
        self.assertEqual(10, len(data["home_team_leaders"]["points"]))
        self.assertEqual(10, len(data["home_team_leaders"]["rebounds"]))
        self.assertDictEqual(
            {"player_license_id": 20212265, "total": 5},
            data["home_team_leaders"]["points"][0],
        )
        self.assertDictEqual(
            {"player_license_id": 30001950, "total": 3},
            data["home_team_leaders"]["rebounds"][0],
        )

    def test_get_game_biggest_lead(self):
        self.client.force_authenticate(user=self.user)

        url = reverse("game_biggest_lead", args=(self.game_id,))
        result = self.client.get(url)

        self.assertEqual(result.status_code, status.HTTP_200_OK)
        data = result.json()
        self.assertDictEqual({"home_team": 6, "away_team": 2}, data)
