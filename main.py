import os

# Set season globally (can be dynamic later)
os.environ["SEASON"] = "2023"

# Set your API key securely (or set via GitHub Actions secret)
# os.environ["API_FOOTBALL_KEY"] = "your-api-key-here"

print("\n🚀 Starting autonomous football pipeline...\n")

# Step 1: Fetch teams
from scraper.fetch_teams import main as fetch_teams
fetch_teams()

# Step 2: Fetch fixtures
from scraper.fetch_fixtures import main as fetch_fixtures
fetch_fixtures()

# Step 3: Fetch team stats
from scraper.fetch_team_stats import main as fetch_stats
fetch_stats()

# Step 4: Format pivot dataset
from processor.pivot_formatter import main as format_data
format_data()

# Step 5: Run predictor
from model.predictor import main as run_model
run_model()

print("\n✅ All steps completed successfully.\n")
