import os
import pandas as pd
from utils.api_client import ApiFootballClient

SEASON = 2023  # or loop later for historical stats
INPUT_FILE = "data/teams.csv"
OUTPUT_FILE = "data/team_stats.csv"

def main():
    client = ApiFootballClient(api_key=os.getenv("API_FOOTBALL_KEY"))

    if not os.path.exists(INPUT_FILE):
        print(f"Missing input file: {INPUT_FILE}")
        return

    teams_df = pd.read_csv(INPUT_FILE)
    all_stats = []

    for _, row in teams_df.iterrows():
        team_id = row["team_id"]
        league_id = row["league_id"]
        team_name = row["team_name"]
        league_name = row["league"]

        print(f"Fetching stats for {team_name} in {league_name}...")

        try:
            stats = client.get_team_stats(team_id=int(team_id), league_id=int(league_id), season=SEASON)
            if not stats:
                continue

            all_stats.append({
                "league": league_name,
                "league_id": league_id,
                "season": SEASON,
                "team": team_name,
                "team_id": team_id,
                "matches_played": stats.get("fixtures", {}).get("played", {}).get("total", None),
                "wins": stats.get("fixtures", {}).get("wins", {}).get("total", None),
                "draws": stats.get("fixtures", {}).get("draws", {}).get("total", None),
                "losses": stats.get("fixtures", {}).get("loses", {}).get("total", None),
                "goals_for": stats.get("goals", {}).get("for", {}).get("total", {}).get("total", None),
                "goals_against": stats.get("goals", {}).get("against", {}).get("total", {}).get("total", None),
                "avg_goals_for": stats.get("goals", {}).get("for", {}).get("average", {}).get("total", None),
                "avg_goals_against": stats.get("goals", {}).get("against", {}).get("average", {}).get("total", None),
                "avg_corners": stats.get("corners", {}).get("total", {}).get("total", None),
                "avg_cards": stats.get("cards", {}).get("yellow", {}).get("total", None),
                "ball_possession": stats.get("ball_possession", None),
                "clean_sheets": stats.get("clean_sheet", {}).get("total", None),
                "failed_to_score": stats.get("failed_to_score", {}).get("total", None)
            })
        except Exception as e:
            print(f"Stats failed for {team_name}: {e}")

    df = pd.DataFrame(all_stats)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Saved {len(df)} team stats to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
