from typing import Any

import requests

from base.settings import ACB_API_BASE_URL, ACB_API_TOKEN


class ACBApiClientException(Exception):
    pass


class ACBApiClient:
    def __init__(self, base_url: str = ACB_API_BASE_URL, token: str = ACB_API_TOKEN) -> None:
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {token}"}

    def get_match_events(self, game_id: int) -> Any:
        url = f"{self.base_url}/openapilive/PlayByPlay/matchevents?idMatch={game_id}"

        response = requests.get(url, headers=self.headers)

        if not response.ok:
            raise ACBApiClientException(response.reason)

        return response.json()
