import os
import pandas as pd
from utils.api_client import ApiFootballClient

SEASON = 2023  # or loop over multiple seasons
INPUT_FILE = "data/teams.csv"
OUTPUT_FILE = "data/fixtures.csv"

def main():
    client = ApiFootballClient(api_key=os.getenv("API_FOOTBALL_KEY"))

    if not os.path.exists(INPUT_FILE):
        print(f"Missing input file: {INPUT_FILE}")
        return

    teams_df = pd.read_csv(INPUT_FILE)
    all_fixtures = []

    for _, row in teams_df.iterrows():
        team_id = row["team_id"]
        league_id = row["league_id"]
        team_name = row["team_name"]
        league_name = row["league"]

        print(f"Fetching fixtures for {team_name} in {league_name}...")

        try:
            fixtures = client.get_fixtures(league_id=int(league_id), season=SEASON, team_id=int(team_id))
            for fixture_data in fixtures:
                fixture = fixture_data["fixture"]
                teams = fixture_data["teams"]
                goals = fixture_data.get("goals", {})
                score = fixture_data.get("score", {})

                all_fixtures.append({
                    "fixture_id": fixture["id"],
                    "date": fixture["date"],
                    "venue": fixture["venue"]["name"],
                    "status": fixture["status"]["short"],
                    "league": league_name,
                    "league_id": league_id,
                    "season": SEASON,
                    "team": team_name,
                    "team_id": team_id,
                    "opponent": (
                        teams["away"]["name"] if teams["home"]["id"] == team_id else teams["home"]["name"]
                    ),
                    "goals_for": goals["for"] if teams["home"]["id"] == team_id else goals["against"],
                    "goals_against": goals["against"] if teams["home"]["id"] == team_id else goals["for"],
                    "full_time_score": score["fulltime"]
                })
        except Exception as e:
            print(f"Error fetching fixtures for {team_name}: {e}")

    df = pd.DataFrame(all_fixtures)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Saved {len(df)} fixtures to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
