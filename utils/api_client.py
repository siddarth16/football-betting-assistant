import requests
import os
from typing import Optional

class ApiFootballClient:
    def __init__(self, api_key: Optional[str] = None):
        self.base_url = "https://v3.football.api-sports.io"
        self.api_key = api_key or os.getenv("API_FOOTBALL_KEY")
        self.headers = {
            "x-apisports-key": self.api_key
        }

    def get(self, endpoint: str, params: dict = {}) -> dict:
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code != 200:
            raise Exception(f"API call failed: {response.status_code} - {response.text}")
        return response.json()

    def get_teams(self, league_id: int, season: int) -> list:
        result = self.get("teams", {"league": league_id, "season": season})
        return result.get("response", [])

    def get_fixtures(self, league_id: int, season: int, team_id: Optional[int] = None) -> list:
        params = {"league": league_id, "season": season}
        if team_id:
            params["team"] = team_id
        result = self.get("fixtures", params)
        return result.get("response", [])

    def get_team_stats(self, team_id: int, league_id: int, season: int) -> dict:
        result = self.get("teams/statistics", {
            "team": team_id,
            "league": league_id,
            "season": season
        })
        return result.get("response", {})
