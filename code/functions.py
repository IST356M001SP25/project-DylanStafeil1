import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import pandas as pd
import seaborn as sns


# Load both datasets from the cache
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

# Get per-game stats for every player on a team
def get_team_stats(team_name):
    df = player_stats.copy()
    return df[df['TEAM_NAME'].str.lower().str.contains(team_name.lower())]

# Get per-game stats for an individual player
def get_player_stats(player_name):
    df = player_stats.copy()
    return df[df['PLAYER_NAME'].str.lower() == player_name.lower()]

# Draw the lines of a basketball court
def draw_court(ax=None, color='black', lw=2):
    if ax is None:
        ax = plt.gca()

    # Hoop
    hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)

    # Backboard
    backboard = Rectangle((-30, -7.5), 60, -1, linewidth=lw, color=color)

    # Paint
    outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color, fill=False)
    inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color, fill=False)

    # Free throw
    top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180, linewidth=lw, color=color, fill=False)
    bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color, linestyle='dashed')

    # Restricted area
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw, color=color)

    # Three-point line
    corner3_left = Rectangle((-220, -47.5), 0, 140, linewidth=lw, color=color)
    corner3_right = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
    arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw, color=color)

    court_elements = [hoop, backboard, outer_box, inner_box,
                      top_free_throw, bottom_free_throw, restricted,
                      corner3_left, corner3_right, arc]

    for element in court_elements:
        ax.add_patch(element)

    ax.set_xlim(-250, 250)
    ax.set_ylim(-47.5, 470)
    ax.set_aspect('equal')
    ax.axis('off')

    return ax

# Get shot chart data for a team
def plot_player_shot_chart(player_name):
    shots = shot_data[shot_data['PLAYER_NAME'].str.lower() == player_name.lower()]
    if shots.empty:
        st.warning("No shot data found for that player.")
        return
    fig, ax = plt.subplots(figsize=(12, 11))
    draw_court(ax)
    ax.set_title(f"{player_name} Shot Chart (2024-25)", fontsize=16)

    # Plot shots with correct coordinates and color mapping
    ax.scatter(
        shots['LOC_X'],
        shots['LOC_Y'],
        c=shots['SHOT_MADE_FLAG'].map({1: 'green', 0: 'red'}),
        s=25,
        alpha=0.6,
        edgecolors='k',
        linewidth=0.2
    )

    ax.set_xlim(-250, 250)
    ax.set_ylim(-47.5, 470)
    st.pyplot(fig)
# Get shot chart data for an individual player
def plot_team_shot_chart(team_name):
    shots = shot_data[shot_data['TEAM_NAME'].str.lower().str.contains(team_name.lower())]

    if shots.empty:
        st.warning("No shot data found for that team.")
        return

    fig, ax = plt.subplots(figsize=(12, 11))
    draw_court(ax)
    ax.set_title(f"{team_name} Shot Chart (2024-25)", fontsize=16)

    ax.scatter(
        shots['LOC_X'],
        shots['LOC_Y'],
        c=shots['SHOT_MADE_FLAG'].map({1: 'green', 0: 'red'}),
        s=25,
        alpha=0.6,
        edgecolors='k',
        linewidth=0.2
    )

    ax.set_xlim(-250, 250)
    ax.set_ylim(-47.5, 470)
    st.pyplot(fig)

#Plot team shot density
def plot_team_shot_density(team_name):
    shots = shot_data[shot_data['TEAM_NAME'].str.lower().str.contains(team_name.lower())]

    if shots.empty:
        st.warning("No shot data found for that team.")
        return

    fig, ax = plt.subplots(figsize=(12, 11))
    draw_court(ax)
    ax.set_title(f"{team_name} Shot Density (2024-25)", fontsize=16)

    sns.kdeplot(
        x=shots['LOC_X'],
        y=shots['LOC_Y'],
        fill=True,
        cmap="inferno",
        thresh=0.05,
        levels=100,
        alpha=0.8,
        ax=ax
    )

    ax.set_xlim(-250, 250)
    ax.set_ylim(-47.5, 470)
    ax.axis('off')

    st.pyplot(fig)

#Plot player shot density

def plot_player_shot_density(player_name):
    shots = shot_data[shot_data['PLAYER_NAME'].str.lower() == player_name.lower()]
    
    if shots.empty:
        st.warning("No shot data found for that player.")
        return

    fig, ax = plt.subplots(figsize=(12, 11))
    draw_court(ax)
    ax.set_title(f"{player_name} Shot Density (2024-25)", fontsize=16)

    sns.kdeplot(
        x=shots['LOC_X'],
        y=shots['LOC_Y'],
        fill=True,
        cmap="inferno",
        thresh=0.05,
        levels=100, 
        alpha=0.8,
        ax=ax
    )

    ax.set_xlim(-250, 250)
    ax.set_ylim(-47.5, 470)
    ax.axis('off')

    st.pyplot(fig)

# Define court zones
ZONES = {
    "Restricted Area": ((-80, 80), (-47.5, 60)),
    "Paint (Non-RA)": ((-80, 80), (60, 143)),
    
    "Left Midrange": ((-220, -80), (-47.5, 143)),
    "Right Midrange": ((80, 220), (-47.5, 143)),
    "Top Midrange": ((-80, 80), (143, 225)),

    "Left Corner 3": ((-250, -220), (-47.5, 143)),
    "Right Corner 3": ((220, 250), (-47.5, 143)),

    "Left Wing 3": ((-250, -80), (143, 300)),
    "Right Wing 3": ((80, 250), (143, 300)),
    "Top of Key 3": ((-80, 80), (225, 300)),
}


# Calculate FG% per zone
def get_zone_stats(df):
    results = []
    for zone, ((x_min, x_max), (y_min, y_max)) in ZONES.items():
        subset = df[(df['LOC_X'] >= x_min) & (df['LOC_X'] < x_max) &
                    (df['LOC_Y'] >= y_min) & (df['LOC_Y'] < y_max)]
        attempts = len(subset)
        makes = subset['SHOT_MADE_FLAG'].sum()
        pct = makes / attempts * 100 if attempts > 0 else 0
        results.append((zone, pct, attempts, x_min, y_min, x_max - x_min, y_max - y_min))
    return results

#Get league averages for each zone
def get_league_zone_averages(df):
    averages = {}
    for zone, ((x_min, x_max), (y_min, y_max)) in ZONES.items():
        shots = df[(df['LOC_X'] >= x_min) & (df['LOC_X'] < x_max) &
                   (df['LOC_Y'] >= y_min) & (df['LOC_Y'] < y_max)]
        attempts = len(shots)
        makes = shots['SHOT_MADE_FLAG'].sum()
        avg_pct = makes / attempts * 100 if attempts > 0 else 0
        averages[zone] = avg_pct
    return averages


#Get player hot/cold zones
def plot_player_hotzones(player_name, df, league_avgs):
    player_shots = df[df['PLAYER_NAME'].str.lower() == player_name.lower()]
    if player_shots.empty:
        st.warning(f"No shot data found for {player_name}")
        return

    stats = get_zone_stats(player_shots)
    diffs = [pct - league_avgs.get(zone, 0) for zone, pct, *_ in stats]
    max_abs_diff = max(abs(d) for d in diffs) or 1  # prevent div by 0

    norm = mcolors.TwoSlopeNorm(vmin=-max_abs_diff, vcenter=0, vmax=max_abs_diff)
    cmap = cm.get_cmap('seismic')

    fig, ax = plt.subplots(figsize=(10, 9))
    ax.set_xlim(-250, 250)
    ax.set_ylim(-47.5, 470)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(f"{player_name} Hot Zones (Colored vs. League Avg)", fontsize=16)

    draw_court(ax)

    for (zone, pct, attempts, x, y, w, h), diff in zip(stats, diffs):
        color = cmap(norm(diff))
        rect = Rectangle((x, y), w, h, color=color, alpha=0.7)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, f"{pct:.1f}%", ha='center', va='center', fontsize=12, weight='bold')

    st.pyplot(fig)

#Get team hot/cold zones
def plot_team_hotzones(team_name, df, league_avgs):
    team_shots = df[df['TEAM_NAME'].str.lower().str.contains(team_name.lower())]
    if team_shots.empty:
        st.warning(f"No shot data found for {team_name}")
        return

    stats = get_zone_stats(team_shots)
    diffs = [pct - league_avgs.get(zone, 0) for zone, pct, *_ in stats]
    max_abs_diff = max(abs(d) for d in diffs) or 1

    norm = mcolors.TwoSlopeNorm(vmin=-max_abs_diff, vcenter=0, vmax=max_abs_diff)
    cmap = cm.get_cmap('seismic')

    fig, ax = plt.subplots(figsize=(10, 9))
    ax.set_xlim(-250, 250)
    ax.set_ylim(-47.5, 470)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(f"{team_name} Hot Zones (Colored vs. League Avg)", fontsize=16)

    draw_court(ax)

    for (zone, pct, attempts, x, y, w, h), diff in zip(stats, diffs):
        color = cmap(norm(diff))
        rect = Rectangle((x, y), w, h, color=color, alpha=0.7)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, f"{pct:.1f}%", ha='center', va='center', fontsize=12, weight='bold')

    st.pyplot(fig)
