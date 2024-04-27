from django.test import TestCase

from clients.acb import ACBApiClient


class ACBApiClientTest(TestCase):
    def setUp(self) -> None:
        self.client = ACBApiClient()

    def test_get_match_events(self):
        game_id = 103789
        match_events = self.client.get_match_events(game_id)

        self.assertEqual(len(match_events), 546)
