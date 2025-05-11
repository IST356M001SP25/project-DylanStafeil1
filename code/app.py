import streamlit as st
import pandas as pd
from functions import (
    draw_court,
    get_player_stats,
    get_team_stats,
    plot_player_shot_chart,
    plot_team_shot_chart,
    plot_player_hotzones,
    plot_team_hotzones,
    get_league_zone_averages,
    plot_team_shot_density,
    plot_player_shot_density
)
# Load datasets once to get dropdown options
player_stats = pd.read_csv('cache/NBA_2024_25_PlayerStats.csv')
shot_data = pd.read_csv('cache/NBA_2024_25_ShotData.csv')

#Add the TEAM_NAME column to the player_stats DataFrame
team_map = shot_data[['TEAM_ID', 'TEAM_NAME']].drop_duplicates()
player_stats = player_stats.merge(team_map, on='TEAM_ID', how='left')

#select the columns we want to keep
player_stats = player_stats[['PLAYER_NAME', 'TEAM_ABBREVIATION', 'TEAM_NAME',
                               'GP', 'MIN', 'PTS', 'FG_PCT', 'FG3_PCT', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST',
                               'STL', 'BLK', 'TOV', 'PLUS_MINUS', 'PLAYER_ID', 'TEAM_ID']]
shot_data = shot_data[['PLAYER_NAME', 'TEAM_ID', 'TEAM_NAME', 'LOC_X', 'LOC_Y', 'SHOT_MADE_FLAG']]


# Unique sorted team and player options
all_teams = sorted(player_stats['TEAM_NAME'].dropna().unique())
all_players = sorted(player_stats['PLAYER_NAME'].dropna().unique())

#Make sure player_id and team_id are strings
player_stats['PLAYER_ID'] = player_stats['PLAYER_ID'].astype(str)
player_stats['TEAM_ID'] = player_stats['TEAM_ID'].astype(str)

#calculate league averages by zone
LEAGUE_AVG_BY_ZONE = get_league_zone_averages(shot_data)

# Streamlit layout
st.set_page_config(page_title="NBA 2024–25 Stats, Shot Charts, and Hot/Cold Zones", layout="wide")
st.title("NBA 2024–25 Stats & Shot Charts")

tab1, tab2 = st.tabs(["📋 Team", "👤 Player"])

with tab1:
    selected_team = st.selectbox("Choose a team:", all_teams)
    team_id = player_stats[player_stats['TEAM_NAME'] == selected_team]['TEAM_ID'].values[0]
    st.header(f"{selected_team} Stats, Shot Chart, and Hot/Cold Zones")
    st.image(f"https://cdn.nba.com/logos/nba/{team_id}/primary/D/logo.svg", width=200)

    st.subheader("Per-Game Stats")
    team_stats = get_team_stats(selected_team)
    st.dataframe(team_stats.reset_index(drop=True), use_container_width=True)
    
    st.subheader("Shot Charts")
    chart_type_team = st.radio(
    "Select Shot Chart Type:", 
    ["Make/Miss Chart", "Density Chart"], 
    horizontal=True, 
    key="team_chart_type"
)

    if chart_type_team == "Make/Miss Chart":
        plot_team_shot_chart(selected_team)
    else:
        st.subheader("NOTE: Density chart takes ~1 minute to load")
        plot_team_shot_density(selected_team)

    st.subheader("Hot/Cold Zones")
    plot_team_hotzones(selected_team, shot_data, LEAGUE_AVG_BY_ZONE)

with tab2:
    selected_player = st.selectbox("Choose a player:", all_players)
    player_id = player_stats[player_stats['PLAYER_NAME'] == selected_player]['PLAYER_ID'].values[0]
    st.header(f"{selected_player} Stats, Shot Chart, and Hot/Cold Zones")
    st.image(f"https://cdn.nba.com/headshots/nba/latest/260x190/{player_id}.png")

    st.subheader("Per-Game Stats")
    player_stats = get_player_stats(selected_player)
    st.dataframe(player_stats.reset_index(drop=True), use_container_width=True)

    st.subheader("Shot Charts")
    chart_type_player = st.radio(
    "Select Shot Chart Type:", 
    ["Make/Miss Chart", "Density Chart"], 
    horizontal=True, 
    key="player_chart_type")

    if chart_type_player == "Make/Miss Chart":
        plot_player_shot_chart(selected_player)
    else:
        st.subheader("NOTE: Density chart takes ~15 seconds to load")
        plot_player_shot_density(selected_player)

    st.subheader("Hot/Cold Zones")
    plot_player_hotzones(selected_player, shot_data, LEAGUE_AVG_BY_ZONE)
