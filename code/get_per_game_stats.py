import pandas as pd
from nba_api.stats.static import players
from nba_api.stats.endpoints import shotchartdetail, leaguedashplayerstats
from nba_api.stats.library.parameters import SeasonAll
import time

# Get per game stats for all players in the 2024-25 NBA season
# Define the season
season = '2024-25'

# Retrieve per-game statistics for all players in the specified season
player_stats = leaguedashplayerstats.LeagueDashPlayerStats(
    season=season,
    season_type_all_star='Regular Season',
    per_mode_detailed='PerGame'
)

# Convert the retrieved data to a pandas DataFrame
df = player_stats.get_data_frames()[0]

# Save the DataFrame to a CSV file
df.to_csv('NBA_2024_25_PlayerStats.csv', index=False)