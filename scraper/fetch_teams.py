import yaml
import os
import pandas as pd
from utils.api_client import ApiFootballClient

# Config
SEASON = 2023  # Change to desired historical season
OUTPUT_FILE = "data/teams.csv"

def load_competitions(file_path="competitions.yaml"):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)["competitions"]

def main():
    client = ApiFootballClient(api_key=os.getenv("API_FOOTBALL_KEY"))
    competitions = load_competitions()

    all_teams = []

    for comp in competitions:
        league_id = comp["id"]
        league_name = comp["name"]
        print(f"Fetching teams for {league_name}...")
        
        try:
            teams = client.get_teams(league_id=league_id, season=SEASON)
            for team_data in teams:
                team = team_data["team"]
                all_teams.append({
                    "league": league_name,
                    "league_id": league_id,
                    "season": SEASON,
                    "team_id": team["id"],
                    "team_name": team["name"],
                    "country": team["country"],
                    "founded": team.get("founded"),
                    "logo": team.get("logo")
                })
        except Exception as e:
            print(f"Failed to fetch for {league_name}: {e}")

    # Save to CSV
    df = pd.DataFrame(all_teams)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Saved {len(df)} teams to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
