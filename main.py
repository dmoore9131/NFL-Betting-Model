import pandas as pd

def fetch_historical_game_data():
    # Mock data for demonstration
    data = {
        'PtsW': [24, 30, 21],
        'PtsL': [17, 23, 18],
        'Team': ['Ravens', 'Ravens', 'Chiefs'],
        'Opponent': ['Chiefs', 'Bengals', 'Ravens'],
        'Home Points': [24, 30, 21],
        'Away Points': [17, 23, 18]
    }
    df_games = pd.DataFrame(data)
    return df_games

def fetch_player_stats():
    # Mock data for demonstration
    data = {
        'Team': ['Ravens', 'Ravens', 'Chiefs', 'Chiefs'],
        'Player': ['Lamar Jackson', 'Mark Andrews', 'Patrick Mahomes', 'Travis Kelce'],
        'Position': ['QB', 'TE', 'QB', 'TE'],
        'Yards': [250, 80, 320, 100],
        'Touchdowns': [2, 1, 3, 2]
    }
    df_player_stats = pd.DataFrame(data)
    return df_player_stats

def fetch_injury_reports():
    # Mock injury reports
    data = {
        'Team': ['Ravens', 'Chiefs'],
        'Player': ['Ronnie Stanley', 'Chris Jones'],
        'Injury': ['Knee', 'Calf'],
        'Status': ['Questionable', 'Out']
    }
    df_injuries = pd.DataFrame(data)
    return df_injuries

def advanced_stats():
    # Mock advanced stats for both teams
    data = {
        'Team': ['Ravens', 'Chiefs'],
        'YPP': [5.5, 6.2],
        'EPA': [0.1, 0.2],
        'YPC': [4.2, 4.5],
        'Pass YPA': [7.7, 7.4],
        'Pass EPA': [-0.03, 0.15],
        'Rush YPA': [4.5, 4.7]
    }
    df_adv_stats = pd.DataFrame(data)
    return df_adv_stats

def fetch_pff_data():
    # Mock PFF data for demonstration
    data = {
        'Team': ['Ravens', 'Chiefs'],
        'Player': ['Lamar Jackson', 'Patrick Mahomes'],
        'PFF Grade': [85.0, 90.0]
    }
    df_pff = pd.DataFrame(data)
    return df_pff

def analyze_team_performance(df_games, team_name):
    team_games = df_games[df_games['Team'] == team_name]
    avg_points_scored = team_games['Home Points'].mean()
    avg_points_allowed = team_games['Away Points'].mean()
    return avg_points_scored, avg_points_allowed

def predict_matchup(df_games, df_player_stats, df_injuries, df_adv_stats, df_pff, team1, team2):
    # Check if team data exists
    if team1 not in df_adv_stats['Team'].values or team2 not in df_adv_stats['Team'].values:
        raise ValueError(f"Data for one or both teams ({team1}, {team2}) not found in advanced stats.")
    
    avg_points_team1, avg_points_allowed_team1 = analyze_team_performance(df_games, team1)
    avg_points_team2, avg_points_allowed_team2 = analyze_team_performance(df_games, team2)
    
    team1_stats = df_adv_stats[df_adv_stats['Team'] == team1].iloc[0]
    team2_stats = df_adv_stats[df_adv_stats['Team'] == team2].iloc[0]
    
    # Incorporate PFF grades
    team1_pff = df_pff[df_pff['Team'] == team1].iloc[0]['PFF Grade']
    team2_pff = df_pff[df_pff['Team'] == team2].iloc[0]['PFF Grade']

    # Base score prediction using advanced stats
    team1_score = (avg_points_team1 - avg_points_allowed_team2) + (team1_stats['YPP'] * 2) - (team1_stats['Pass EPA'] * 1.5) + (team1_pff * 0.1)
    team2_score = (avg_points_team2 - avg_points_allowed_team1) + (team2_stats['YPP'] * 2) - (team2_stats['Pass EPA'] * 1.5) + (team2_pff * 0.1)
    
    # Adjust scores based on injuries
    injuries_team1 = df_injuries[df_injuries['Team'] == team1]
    injuries_team2 = df_injuries[df_injuries['Team'] == team2]
    
    if not injuries_team1.empty:
        team1_score -= injuries_team1.shape[0] * 1.0
    
    if not injuries_team2.empty:
        team2_score -= injuries_team2.shape[0] * 1.0
    
    # Scale scores based on O/U line (46.5)
    total_points = team1_score + team2_score
    scaling_factor = 46.5 / total_points if total_points > 0 else 1
    team1_score *= scaling_factor
    team2_score *= scaling_factor
    
    # Cap scores to a realistic range
    team1_score = max(1, min(40, team1_score))
    team2_score = max(1, min(40, team2_score))
    
    winner = team1 if team1_score > team2_score else team2
    
    team1_player_stats = df_player_stats[df_player_stats['Team'] == team1]
    team2_player_stats = df_player_stats[df_player_stats['Team'] == team2]
    
    return team1_score, team2_score, winner, team1_player_stats, team2_player_stats

def main():
    df_games = fetch_historical_game_data()
    df_player_stats = fetch_player_stats()
    df_injuries = fetch_injury_reports()
    df_adv_stats = advanced_stats()
    df_pff = fetch_pff_data()
    
    week1_schedule = [
        ('Ravens', 'Chiefs'),
        # Add more matchups for Week 1 as needed
    ]
    
    for team1, team2 in week1_schedule:
        try:
            team1_score, team2_score, winner, team1_stats, team2_stats = predict_matchup(df_games, df_player_stats, df_injuries, df_adv_stats, df_pff, team1, team2)
            
            # Print results
            print(f"Predicted Total Score - {team1}: {team1_score:.2f}")
            print(f"Predicted Total Score - {team2}: {team2_score:.2f}")
            print(f"Predicted Winner: {winner}")
            
            print(f"\n{team1} Player Stats:")
            print(team1_stats)
            
            print(f"\n{team2} Player Stats:")
            print(team2_stats)
        except ValueError as e:
            print(e)

if __name__ == "__main__":
    main()
