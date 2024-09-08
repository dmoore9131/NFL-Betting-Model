import pandas as pd
import requests

# Define rosters for Rams and Lions

def fetch_weather_and_grass_data(game_id):
    # Simulated weather and grass data for demonstration
    weather_data = {
        2: {
            'Weather': 'Clear',
            'Grass Type': 'Artificial Turf',
            'Travel Impact': 3  # 1-10 scale where 10 is highest impact
        }
    }
    return weather_data.get(game_id, None)

def fetch_defensive_stats(game_id):
    # Simulated defensive stats for demonstration
    defensive_stats = {
        2: {
            'Rams': {'Sacks': 4, 'Interceptions': 1, 'Forced Fumbles': 2},
            'Lions': {'Sacks': 2, 'Interceptions': 2, 'Forced Fumbles': 1}
        }
    }
    return defensive_stats.get(game_id, None)

def fetch_game_data(game_id):
    # Simulated game data for demonstration
    game_data = {
        2: {
            'Historical': pd.DataFrame({
                'Game': ['Rams vs Lions'] * 10,
                'Home Team': ['Lions'] * 10,
                'Away Team': ['Rams'] * 10,
                'Home Score': [27] * 10,
                'Away Score': [24] * 10
            }),
            'Live': pd.DataFrame({
                'Team': ['Rams', 'Lions'],
                'Current Score': [17, 20],  # Example updated scores
                'Time of Possession': ['29:15', '30:45'],  # Example updated data
                'Penalties': [4, 5]  # Example updated data
            }),
            'Player Stats': pd.DataFrame({
                'Team': ['Rams'] * 5 + ['Lions'] * 5,
                'Player': ['Matthew Stafford', 'Cam Akers', 'Cooper Kupp', 'Tutu Atwell', 'Tyler Higbee',
                           'Jared Goff', 'D\'Andre Swift', 'Amon-Ra St. Brown', 'Josh Reynolds', 'Sam LaPorta'],
                'Yards': [280, 75, 130, 55, 60, 300, 90, 110, 70, 50],
                'Position': ['QB', 'RB', 'WR', 'WR', 'TE', 'QB', 'RB', 'WR', 'WR', 'TE']
            }),
            'Injury Reports': pd.DataFrame({
                'Team': ['Rams'] * 2 + ['Lions'] * 2,
                'Player': ['Tyler Higbee', 'Joe Noteboom', 'Aidan Hutchinson', 'Taylor Decker'],
                'Status': ['Probable', 'Out', 'Questionable', 'Out']
            }),
            'Ball Last Year': pd.DataFrame({
                'Team': ['Rams', 'Lions'],
                'Ball Possessions Last Year': [55, 53]  # Example data
            }),
            'Short Week Impact': pd.DataFrame({
                'Team': ['Rams', 'Lions'],
                'Impact Score': [3, 5]  # Impact score out of 10 for short weeks
            })
        }
    }

    game = game_data.get(game_id, None)
    if game:
        weather_data = fetch_weather_and_grass_data(game_id)
        defensive_stats = fetch_defensive_stats(game_id)

        # Fetch betting odds and predictions from external sources
        betting_odds = {
            'DraftKings': {'Rams': -110, 'Lions': -105, 'Over/Under': 48.5},
            'FanDuel': {'Rams': -108, 'Lions': -112, 'Over/Under': 48.0},
            'Vegas': {'Rams': -115, 'Lions': -110, 'Over/Under': 48.2}
        }

        # Fetch player props predictions from Pine Sports
        player_props = {
            'Cooper Kupp': {'Yards': 110.5, 'Touchdowns': 1.5},
            'Amon-Ra St. Brown': {'Yards': 90.5, 'Touchdowns': 1.0}
        }

        # Fantasy Draft Decisions
        fantasy_advice = {
            'Best Players': 'Matthew Stafford, Jared Goff, Cooper Kupp, Amon-Ra St. Brown',
            'Avoid Injured Players': 'Tyler Higbee, Aidan Hutchinson'
        }

        # Determine who gets the most targets, avoiding QBs
        def most_targets(team, injured_players):
            players = game['Player Stats'].query(f"Team == '{team}'")
            if injured_players:
                players = players[~players['Player'].isin(injured_players)]
            # Exclude QBs from the consideration
            players = players[~players['Position'].str.contains('QB')]
            return players.sort_values(by='Yards', ascending=False).iloc[0]['Player'] if not players.empty else 'No available players'

        injured_players_rams = game['Injury Reports'].query("Team == 'Rams' and Status != 'Probable'")['Player'].tolist()
        injured_players_lions = game['Injury Reports'].query("Team == 'Lions' and Status != 'Probable'")['Player'].tolist()

        most_targets_rams = most_targets('Rams', injured_players_rams)
        most_targets_lions = most_targets('Lions', injured_players_lions)

        # Incorporate weather, grass type, and short week into the analysis
        performance_adjustments = {
            'Weather': weather_data['Weather'],
            'Grass Type': weather_data['Grass Type'],
            'Travel Impact': weather_data['Travel Impact'],
            'Short Week Impact': game['Short Week Impact']
        }

        # Strategy Recommendations
        strategies = {
            'Offensive Coordinator Rams': 'Use short passes and screen plays to manage the Lions’ blitzing.',
            'Defensive Coordinator Rams': 'Focus on pressuring Jared Goff and covering the Lions’ WRs.',
            'Head Coach Rams': 'Maintain a run-pass balance and utilize play action.',
            'Offensive Coordinator Lions': 'Exploit the Rams secondary with deep passes.',
            'Defensive Coordinator Lions': 'Double-team Cooper Kupp and stop the Rams’ running game.',
            'Head Coach Lions': 'Leverage home field advantage and aggressive defensive schemes.'
        }

        return {
            'Historical': game['Historical'],
            'Live': game['Live'],
            'Player Stats': game['Player Stats'],
            'Injury Reports': game['Injury Reports'],
            'Fantasy Draft Decisions': fantasy_advice,
            'Most Targets Rams': most_targets_rams,
            'Most Targets Lions': most_targets_lions,
            'Weather Data': performance_adjustments,
            'Betting Odds': betting_odds,
            'Player Props': player_props,
            'Ball Last Year': game['Ball Last Year'],
            'Strategies': strategies
        }

    return None

# Example Usage:
game_data = fetch_game_data(2)
print(game_data['Historical'])
print(game_data['Live'])
print(game_data['Player Stats'])
print(game_data['Injury Reports'])
print("Fantasy Draft Decisions:")
print(game_data['Fantasy Draft Decisions'])
print("Most Targets Rams:", game_data['Most Targets Rams'])
print("Most Targets Lions:", game_data['Most Targets Lions'])
print("Weather Data:", game_data['Weather Data'])
print("Betting Odds:", game_data['Betting Odds'])
print("Player Props:", game_data['Player Props'])
print("Ball Possessions Last Year:")
print(game_data['Ball Last Year'])
print("Strategies:")
print(game_data['Strategies'])
