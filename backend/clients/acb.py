from typing import Any, List

import requests

from base.settings import ACB_API_BASE_URL, ACB_API_TOKEN
from match_event.models import MatchEvent


class ACBClientException(Exception):
    pass


class ACBClient:
    def __init__(
        self, base_url: str = ACB_API_BASE_URL, token: str = ACB_API_TOKEN
    ) -> None:
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {token}"}

    @classmethod
    def _parse_match_event(cls, match_event: Any) -> MatchEvent:
        team_id = None
        if team := match_event.get("team", {}):
            team_id = team.get("id_team_denomination")
        return MatchEvent(
            game_id=match_event.get("id_match"),
            team_id=team_id,
            player_license_id=match_event.get("id_license"),
            action_time=match_event.get("crono"),
            action_type=match_event.get("id_playbyplaytype"),
            is_home_team=match_event.get("local"),
            score_home_team=match_event.get("score_local"),
            score_away_team=match_event.get("score_visitor"),
        )

    def get_match_events(self, game_id: int) -> List[MatchEvent]:
        url = f"{self.base_url}/openapilive/PlayByPlay/matchevents?idMatch={game_id}"

        response = requests.get(url, headers=self.headers)

        if not response.ok:
            raise ACBClientException(response.reason)

        match_events = response.json()

        return [self._parse_match_event(match_event) for match_event in match_events]
