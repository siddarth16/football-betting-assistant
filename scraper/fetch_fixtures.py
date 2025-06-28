import os
import pandas as pd
from utils.api_client import ApiFootballClient

SEASON = 2023  # You can later loop over multiple seasons
INPUT_FILE = "data/teams.csv"
OUTPUT_FILE = "data/fixtures.csv"

def main():
    client = ApiFootballClient(api_key=os.getenv("API_FOOTBALL_KEY"))

    if not os.path.exists(INPUT_FILE):
        print(f"❌ Missing input file: {INPUT_FILE}")
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

                # Safely extract goals
                goals_for = None
                goals_against = None
                if "goals" in fixture_data and fixture_data["goals"]:
                    home_id = teams["home"]["id"]
                    away_id = teams["away"]["id"]
                    goals = fixture_data["goals"]
                    if team_id == home_id:
                        goals_for = goals.get("home")
                        goals_against = goals.get("away")
                    else:
                        goals_for = goals.get("away")
                        goals_against = goals.get("home")

                # Determine opponent
                opponent = teams["away"]["name"] if teams["home"]["id"] == team_id else teams["home"]["name"]

                all_fixtures.append({
                    "fixture_id": fixture["id"],
                    "date": fixture["date"],
                    "venue": fixture.get("venue", {}).get("name"),
                    "status": fixture["status"]["short"],
                    "league": league_name,
                    "league_id": league_id,
                    "season": SEASON,
                    "team": team_name,
                    "team_id": team_id,
                    "opponent": opponent,
                    "goals_for": goals_for,
                    "goals_against": goals_against,
                    "full_time_score": fixture_data.get("score", {}).get("fulltime")
                })

        except Exception as e:
            print(f"⚠️ Error fetching fixtures for {team_name}: {e}")

    # Save output
    df = pd.DataFrame(all_fixtures)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"\n✅ Saved {len(df)} fixtures to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
