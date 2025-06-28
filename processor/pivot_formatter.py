import pandas as pd
import os

FIXTURES_FILE = "data/fixtures.csv"
STATS_FILE = "data/team_stats.csv"
OUTPUT_FILE = "data/merged_dataset.csv"

def main():
    if not os.path.exists(FIXTURES_FILE) or not os.path.exists(STATS_FILE):
        print("Missing input files.")
        return

    # Load datasets
    fixtures = pd.read_csv(FIXTURES_FILE)
    stats = pd.read_csv(STATS_FILE)

    # Merge on team_id + season + league_id
    merged = fixtures.merge(
        stats,
        how="left",
        on=["team_id", "season", "league_id"],
        suffixes=('', '_team')
    )

    # Feature formatting
    merged["date"] = pd.to_datetime(merged["date"])
    merged["is_home"] = merged.apply(lambda x: x["team"] == x["team"], axis=1)
    merged["goal_diff"] = merged["goals_for"] - merged["goals_against"]

    # Add simple outcome tag
    merged["result"] = merged["goal_diff"].apply(
        lambda x: "W" if x > 0 else "L" if x < 0 else "D"
    )

    # Sort for time series
    merged = merged.sort_values(by=["team", "date"])

    # Save output
    merged.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ Merged dataset saved to {OUTPUT_FILE} with {len(merged)} rows.")

if __name__ == "__main__":
    main()
