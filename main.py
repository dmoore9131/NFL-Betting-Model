import pandas as pd
import time
import random

def fetch_historical_game_data():
    data = {
        'Game': ['49ers vs Jets'],
        'Home Team': ['49ers'],
        'Away Team': ['Jets']
    }
    df_game_data = pd.DataFrame(data)
    return df_game_data

def fetch_player_stats():
    data = {
        'Team': ['49ers', 'Jets'],
        'Player': ['Brock Purdy', 'Aaron Rogers'],
        'Position': ['QB', 'QB'],
        'Yards': [320, 260],  # Example updated yardage
        'Touchdowns': [2, 1]  # Example updated touchdowns
    }
    df_player_stats = pd.DataFrame(data)
    return df_player_stats

def fetch_favorite_targets():
    data = {
        'Team': ['49ers', 'Jets'],
        'Favorite Target': ['WR Deebo Samuel/TE George Kittle', 'WR Garrett Wilson/TE Tyler Conklin'],
        'Target Stats (Yards)': [110, 95],  # Updated example yardage
        'Target Stats (Receptions)': [9, 8],
        'Target Stats (TDs)': [2, 1]
    }
    df_favorite_targets = pd.DataFrame(data)
    return df_favorite_targets

def fetch_injury_reports():
    data = {
        'Team': ['49ers', 'Jets'],
        'Player': ['George Kittle', 'Garrett Wilson'],
        'Injury': ['Hamstring', 'Knee'],
        'Status': ['Questionable', 'Questionable']
    }
    df_injury_reports = pd.DataFrame(data)
    return df_injury_reports

def advanced_stats():
    data = {
        'Team': ['49ers', 'Jets'],
        'YPP': [5.9, 5.2],  # Updated example values
        'EPA': [0.18, 0.11],
        'YPC': [4.7, 4.0],
        'Pass YPA': [8.0, 7.2],
        'Pass EPA': [0.05, -0.02],
        'Rush YPA': [4.6, 3.8]
    }
    df_advanced_stats = pd.DataFrame(data)
    return df_advanced_stats

def fetch_pff_data():
    data = {
        'Team': ['49ers', 'Jets'],
        'Offensive Grade': [86, 80],
        'Defensive Grade': [85, 83]
    }
    df_pff_data = pd.DataFrame(data)
    return df_pff_data

def fetch_external_predictions():
    data = {
        'Game': ['49ers vs Jets'],
        'Predicted Winner': ['49ers'],
        'Predicted Margin': [10],  # Updated example prediction margin
        'Total Over/Under': [45.5]  # Updated example over/under
    }
    df_predictions = pd.DataFrame(data)
    return df_predictions

def fetch_defensive_stats():
    data = {
        'Team': ['49ers', 'Jets'],
        'Sacks': [4, 3],
        'Interceptions': [2, 1],
        'Fumbles Recovered': [1, 1],
        'Tackles for Loss': [6, 5],
        'Passes Defended': [5, 4],
        'Best Defensive Player': ['Nick Bosa', 'Quinnen Williams']
    }
    df_defensive_stats = pd.DataFrame(data)
    return df_defensive_stats

def calculate_injury_impact(injury_reports, player_stats, defensive_stats):
    impact = {}
    for index, row in injury_reports.iterrows():
        if row['Status'] == 'Questionable':
            impact[row['Player']] = -0.2  # Adjusted impact value
    return impact

def calculate_experience_impact(player_stats, defensive_stats):
    experience_impact = {}
    for index, row in player_stats.iterrows():
        if 'Rookie' in row['Player'] or 'New Addition' in row['Player']:
            experience_impact[row['Player']] = -0.1  # Example impact value for rookies/new additions
    return experience_impact

def predict_score(player_stats, defensive_stats, injury_impact, experience_impact):
    # Base scores
    niners_score = 24  # Updated base score for 49ers
    jets_score = 17    # Updated base score for Jets

    # Apply injury impact
    for player, impact in injury_impact.items():
        if player in player_stats['Player'].values:
            team = player_stats[player_stats['Player'] == player]['Team'].values[0]
            if team == '49ers':
                niners_score += impact * 10  # Example calculation
            else:
                jets_score += impact * 10  # Example calculation
        elif player in defensive_stats['Best Defensive Player'].values:
            team = defensive_stats[defensive_stats['Best Defensive Player'] == player]['Team'].values[0]
            if team == '49ers':
                niners_score -= impact * 10  # Example calculation
            else:
                jets_score -= impact * 10  # Example calculation

    # Apply experience impact
    for player, impact in experience_impact.items():
        if player in player_stats['Player'].values:
            team = player_stats[player_stats['Player'] == player]['Team'].values[0]
            if team == '49ers':
                niners_score += impact * 5  # Example calculation
            else:
                jets_score += impact * 5  # Example calculation

    # Introduce randomness
    niners_score += random.randint(-3, 3)
    jets_score += random.randint(-3, 3)

    return niners_score, jets_score

def main():
    print("Welcome to the NFL Game Prediction System")

    # Wait for 1 minute
    print("Waiting for 1 minute...")
    time.sleep(60)

    # Fetch data
    historical_data = fetch_historical_game_data()
    player_stats = fetch_player_stats()
    favorite_targets = fetch_favorite_targets()
    injury_reports = fetch_injury_reports()
    advanced_stats_data = advanced_stats()
    pff_data = fetch_pff_data()
    external_predictions = fetch_external_predictions()
    defensive_stats = fetch_defensive_stats()

    # Calculate injury impact
    injury_impact = calculate_injury_impact(injury_reports, player_stats, defensive_stats)

    # Calculate experience impact
    experience_impact = calculate_experience_impact(player_stats, defensive_stats)

    # Predict score
    niners_score, jets_score = predict_score(player_stats, defensive_stats, injury_impact, experience_impact)

    # Display historical game data
    print("\nHistorical Game Data:")
    print(historical_data)

    # Display player stats
    print("\nPlayer Stats:")
    print(player_stats)

    # Display favorite targets
    print("\nFavorite Targets and Stats:")
    print(favorite_targets)

    # Display injury reports
    print("\nInjury Reports:")
    print(injury_reports)

    # Display advanced stats
    print("\nAdvanced Stats:")
    print(advanced_stats_data)

    # Display PFF grades
    print("\nPFF Data:")
    print(pff_data)

    # Display external predictions
    print("\nExternal Predictions:")
    print(external_predictions)

    # Display defensive stats
    print("\nDefensive Stats:")
    print(defensive_stats)

    # Display predicted score
    print("\nPredicted Score:")
    print(f"49ers: {niners_score}, Jets: {jets_score}")

if __name__ == "__main__":
    main()
