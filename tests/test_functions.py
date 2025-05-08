import pytest
import os
import sys
import pandas as pd
from code.functions import get_player_stats, get_team_stats, get_zone_stats, get_league_zone_averages, plot_player_shot_chart, plot_team_shot_chart, plot_player_hotzones, plot_team_hotzones
import matplotlib.pyplot as plt

# Load test data
player_stats_df = pd.read_csv("cache/NBA_2024_25_PlayerStats.csv")
shots_df = pd.read_csv("cache/NBA_2024_25_ShotData.csv")

def test_get_player_stats():
    player = "Cade Cunningham"
    result = get_player_stats(player)
    assert result.iloc[0]['PLAYER_ID'] == 1630595
    assert player.lower() in result.iloc[0]['PLAYER_NAME'].lower()

def test_get_team_stats():
    team = "Detroit Pistons"
    result = get_team_stats(team)
    #Assert that TEAM_ID is correct
    assert result.iloc[0]['TEAM_ID'] == 1610612765
    assert all(team.lower() in name.lower() for name in result['TEAM_NAME'].unique())

def test_get_zone_stats():
    zones = get_zone_stats(shots_df)
    assert isinstance(zones, list)
    assert all(len(zone) == 7 for zone in zones)

def test_get_league_zone_averages():
    league_avg = get_league_zone_averages(shots_df)
    assert isinstance(league_avg, dict)
    assert all(isinstance(v, float) for v in league_avg.values())

def test_plot_player_shot_chart_runs():
    try:
        plot_player_shot_chart("Cade Cunningham")
    except Exception as e:
        assert False, f"plot_player_shot_chart raised an error: {e}"

def test_plot_team_shot_chart_runs():
    try:
        plot_team_shot_chart("Detroit Pistons")
    except Exception as e:
        assert False, f"plot_team_shot_chart raised an error: {e}"

def test_plot_player_hotzones_runs():
    league_avg = get_league_zone_averages(shots_df)
    try:
        plot_player_hotzones("Cade Cunningham", shots_df, league_avg)
    except Exception as e:
        assert False, f"plot_player_hotzones raised an error: {e}"

def test_plot_team_hotzones_runs():
    league_avg = get_league_zone_averages(shots_df)
    try:
        plot_team_hotzones("Detroit Pistons", shots_df, league_avg)
    except Exception as e:
        assert False, f"plot_team_hotzones raised an error: {e}"
