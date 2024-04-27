import responses
from django.test import TestCase
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR

from clients.acb import ACBApiClient, ACBApiClientException


class ACBApiClientTest(TestCase):
    def setUp(self) -> None:
        self.base_url = "https://mock.mock"
        self.client = ACBApiClient(base_url=self.base_url, token="mock")

    @responses.activate
    def test_get_match_events_error(self):
        game_id = 1
        url = f"{self.base_url}/openapilive/PlayByPlay/matchevents?idMatch={game_id}"
        responses.add(responses.GET, url, status=HTTP_500_INTERNAL_SERVER_ERROR)

        with self.assertRaises(ACBApiClientException) as context:
            self.client.get_match_events(game_id)

        self.assertEqual(str(context.exception), "Internal Server Error")
