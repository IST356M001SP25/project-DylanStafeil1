import pandas as pd
from nba_api.stats.static import players
from nba_api.stats.endpoints import shotchartdetail, leaguedashplayerstats
from nba_api.stats.library.parameters import SeasonAll
import time

# Get shot data for all active players in the 2024-25 NBA season
# Get all active NBA players
all_players = players.get_active_players()

# Initialize an empty DataFrame to store all shot data
all_shots_df = pd.DataFrame()

# Iterate through each player and fetch their shot data
for player in all_players:
    player_id = player['id']
    player_name = player['full_name']
    try:
        # Fetch shot chart data for the player for the 2024-25 regular season
        shot_chart = shotchartdetail.ShotChartDetail(
            team_id=0,
            player_id=player_id,
            season_type_all_star='Regular Season',
            season_nullable='2024-25',
            context_measure_simple='FGA'
        )
        # Convert the shot data to a DataFrame
        shot_df = shot_chart.get_data_frames()[0]
        # Append to the main DataFrame
        all_shots_df = pd.concat([all_shots_df, shot_df], ignore_index=True)
        print(f"Retrieved data for {player_name}")
        # Pause to respect rate limits
        time.sleep(1)
    except Exception as e:
        print(f"Could not retrieve data for {player_name}: {e}")
        continue

# Save the aggregated shot data to a CSV file
all_shots_df.to_csv('NBA_2024_25_ShotData.csv', index=False)


