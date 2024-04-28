import json
import os

import responses
from django.forms.models import model_to_dict
from django.test import TestCase
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR

from base.settings import ACB_API_BASE_URL, BASE_DIR
from clients.acb import ACBClient, ACBClientException

FIXTURE_PATH = os.path.join(BASE_DIR, "tests", "fixtures", "match_events.json")


class ACBClientTest(TestCase):
    def setUp(self) -> None:
        self.client = ACBClient()

    def test_get_match_events(self):
        game_id = 103789
        match_events = self.client.get_match_events(game_id)

        self.assertEqual(len(match_events), 546)

    @responses.activate
    def test_get_match_events_error(self):
        game_id = 1
        url = f"{ACB_API_BASE_URL}/openapilive/PlayByPlay/matchevents?idMatch={game_id}"
        responses.add(responses.GET, url, status=HTTP_500_INTERNAL_SERVER_ERROR)

        with self.assertRaises(ACBClientException) as context:
            self.client.get_match_events(game_id)

        self.assertEqual(str(context.exception), "Internal Server Error")

    def test_parse_match_event(self):
        with open(FIXTURE_PATH, "r") as file:
            match_event = json.load(file)[0]
        instance = self.client._parse_match_event(match_event)
        self.assertDictEqual(
            {
                "id": None,
                "game_id": 1,
                "team_id": 2503,
                "player_license_id": 30001114,
                "action_time": "00:10:00",
                "action_type": 599,
                "is_home_team": False,
                "score_home_team": 0,
                "score_away_team": 0,
            },
            model_to_dict(instance),
        )
