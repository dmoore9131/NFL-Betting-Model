import pandas as pd
import numpy as np

# Define updated team rosters
eagles_roster = {
    'Position': [
        'QB', 'RB', 'WR', 'WR', 'WR', 'TE', 'LT', 'LG', 'C', 'RG', 'RT',
        'LDE', 'NT', 'RDE', 'WLB', 'LILB', 'RILB', 'SLB', 'LCB', 'SS', 'FS', 'RCB', 'NB',
        'PK', 'P', 'H', 'PR', 'KR', 'LS'
    ],
    'Starter': [
        'Jalen Hurts', 'Saquon Barkley', 'A.J. Brown', 'DeVonta Smith', 'Jahan Dotson', 
        'Dallas Goedert', 'Jordan Mailata', 'Landon Dickerson', 'Cam Jurgens', 'Mekhi Becton', 
        'Lane Johnson', 'Milton Williams', 'Jordan Davis', 'Jalen Carter', 'Bryce Huff', 
        'Zack Baun', 'Nakobe Dean', 'Josh Sweat', 'Kelee Ringo', 'C.J. Gardner-Johnson', 
        'Reed Blankenship', 'Darius Slay Jr.', 'Quinyon Mitchell', 'Jake Elliott', 'Braden Mann', 
        'Braden Mann', 'Britain Covey', 'Isaiah Rodgers O', 'Rick Lovato'
    ],
    '2nd': [
        'Kenny Pickett', 'Kenneth Gainwell', 'Johnny Wilson', 'Britain Covey', 'Ainias Smith IR', 
        'Grant Calcaterra', 'Fred Johnson', 'Trevor Keegan', '-', 'Tyler Steen', 
        'Darian Kinnard', 'Moro Ojomo', 'Byron Young', 'Thomas Booker IV', 'Brandon Graham', 
        'Jeremiah Trotter Jr.', 'Devin White O', 'Nolan Smith Jr.', 'Isaiah Rodgers O', 
        'Avonte Maddox', 'James Bradberry IV IR', 'Cooper DeJean', '-', '-', '-', '-', 
        '-', '-', '-', '-'
    ],
    '3rd': [
        'Tanner McKee', 'Will Shipley', 'Jacob Harris IR', '-', '-', 'Albert Okwuegbunam Jr. IR', 
        '-', '-', '-', '-', 'Brandon Graham', '-', '-', 'Oren Burks', 'Ben VanSumeren', 
        'Jalyx Hunt', 'Eli Ricks', 'Tristin McCollum', 'Sydney Brown O', '-', '-', '-', 
        '-', '-', '-', '-'
    ],
    '4th': [
        '-', '-', '-', '-', '-', 'McCallan Castles IR', '-', '-', '-', '-', 
        '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'
    ]
}

packers_roster = {
    'Position': [
        'QB', 'RB', 'WR', 'WR', 'WR', 'TE', 'LT', 'LG', 'C', 'RG', 'RT',
        'LDE', 'LDT', 'RDT', 'RDE', 'WLB', 'MLB', 'SLB', 'LCB', 'SS', 'FS', 'RCB', 'NB',
        'PK', 'P', 'H', 'PR', 'KR', 'LS'
    ],
    'Starter': [
        'Jordan Love', 'Josh Jacobs', 'Christian Watson', 'Romeo Doubs', 'Jayden Reed', 
        'Luke Musgrave', 'Rasheed Walker', 'Elgton Jenkins', 'Josh Myers', 'Jordan Morgan', 
        'Zach Tom', 'Preston Smith', 'Kenny Clark', 'T.J. Slaton', 'Rashan Gary', 
        'Quay Walker', 'Eric Wilson', 'Isaiah McDuffie', 'Jaire Alexander', 'Javon Bullard', 
        'Xavier McKinney', 'Eric Stokes', 'Keisean Nixon', 'Brayden Narveson', 'Daniel Whelan', 
        'Daniel Whelan', 'Keisean Nixon', 'Keisean Nixon', 'Matt Orzech'
    ],
    '2nd': [
        'Malik Willis', 'MarShawn Lloyd Q', 'Dontayvion Wicks', 'Bo Melton', 'Malik Heath', 
        'Tucker Kraft Q', 'Andre Dillard', '-', 'Jacob Monk', 'Sean Rhyan', 'Kadeem Telfort', 
        'Lukas Van Ness', 'Devonte Wyatt', 'Karl Brooks', 'Kingsley Enagbare', '-', 
        'Edgerrin Cooper', 'Ty\'Ron Hopper', 'Corey Ballentine', 'Evan Williams', 
        'Zayne Anderson', 'Carrington Valentine', '-', '-', '-', '-', '-', '-', 
        '-', '-', '-', '-'
    ],
    '3rd': [
        '-', 'Emanuel Wilson Q', '-', '-', '-', 'Ben Sims', '-', '-', '-', '-', 
        'Travis Glover', 'Brenton Cox Jr.', 'Colby Wooden', 'Jonathan Ford IR', 'Arron Mosby O', 
        '-', '-', '-', 'LJ Davis IR', '-', '-', '-', '-', '-', '-', '-', '-', '-'
    ],
    '4th': [
        '-', 'AJ Dillon IR', '-', '-', '-', 'Tyler Davis IR', '-', '-', '-', '-', 
        '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'
    ]
}

def fetch_historical_game_data():
    data = {
        'Game': ['Packers vs Eagles'] * 10,
        'Home Team': ['Eagles'] * 10,
        'Away Team': ['Packers'] * 10,
        'Home Score': [24] * 10,
        'Away Score': [27] * 10
    }
    df_game_data = pd.DataFrame(data)
    return df_game_data

def fetch_live_game_data():
    data = {
        'Team': ['Packers', 'Eagles'],
        'Current Score': [28, 21]
    }
    df_live_game_data = pd.DataFrame(data)
    return df_live_game_data

def fetch_player_stats():
    data = {
        'Team': ['Packers'] * 5 + ['Eagles'] * 5,
        'Player': ['Jordan Love', 'Josh Jacobs', 'Christian Watson', 'Romeo Doubs', 'Jayden Reed',
                   'Jalen Hurts', 'Saquon Barkley', 'A.J. Brown', 'DeVonta Smith', 'Dallas Goedert'],
        'Position': ['QB', 'RB', 'WR', 'WR', 'WR', 'QB', 'RB', 'WR', 'WR', 'TE'],
        'Yards': [320, 95, 85, 90, 100, 340, 95, 105, 90, 85],
        'Touchdowns': [3, 1, 1, 1, 1, 3, 1, 2, 1, 1]
    }
    df_player_stats = pd.DataFrame(data)
    return df_player_stats

def fetch_injury_reports():
    data = {
        'Team': ['Packers', 'Eagles'],
        'Player': ['Josh Jacobs', 'Lane Johnson'],
        'Injury': ['Hamstring', 'Ankle'],
        'Status': ['Questionable', 'Probable']
    }
    df_injury_reports = pd.DataFrame(data)
    return df_injury_reports

def fetch_training_camp_data():
    data = {
        'Team': ['Packers', 'Eagles'],
        'Player': ['Jordan Love', 'Jalen Hurts'],
        'Camp Performance': [92, 95],
        'Camp Insights': ['Improved passing accuracy', 'Excellent leadership']
    }
    df_training_camp = pd.DataFrame(data)
    return df_training_camp

def fetch_mini_camp_data():
    data = {
        'Team': ['Packers', 'Eagles'],
        'Player': ['Christian Watson', 'A.J. Brown'],
        'Mini Camp Performance': [90, 93],
        'Mini Camp Insights': ['Strong route running', 'Outstanding catch ability']
    }
    df_mini_camp = pd.DataFrame(data)
    return df_mini_camp

def fetch_walk_through_data():
    data = {
        'Team': ['Packers', 'Eagles'],
        'Player': ['Elgton Jenkins', 'Fletcher Cox'],
        'Walk Through Performance': [88, 90],
        'Walk Through Insights': ['Improved blocking', 'Strong defensive presence']
    }
    df_walk_through = pd.DataFrame(data)
    return df_walk_through

def advanced_stats():
    data = {
        'Team': ['Packers', 'Eagles'],
        'Average Yards per Game': [350, 320],
        'Turnovers': [10, 8],
        'Sacks Allowed': [25, 22]
    }
    df_adv_stats = pd.DataFrame(data)
    return df_adv_stats

def head_to_head_data():
    data = {
        'Team': ['Packers', 'Eagles'],
        'Head-to-Head Wins': [3, 2]
    }
    df_head_to_head = pd.DataFrame(data)
    return df_head_to_head

def top_performers():
    data = {
        'Team': ['Packers', 'Eagles'],
        'Player': ['Jordan Love', 'Jalen Hurts'],
        'Performance Score': [95, 97]
    }
    df_performers = pd.DataFrame(data)
    return df_performers

def compile_data():
    historical_game_data = fetch_historical_game_data()
    live_game_data = fetch_live_game_data()
    training_camp_data = fetch_training_camp_data()
    mini_camp_data = fetch_mini_camp_data()
    walk_through_data = fetch_walk_through_data()
    adv_stats = advanced_stats()
    head_to_head = head_to_head_data()
    performers = top_performers()
    
    # Ensure DataFrames have consistent column names
    historical_game_data.rename(columns={'Home Team': 'Team'}, inplace=True)
    live_game_data.rename(columns={'Team': 'Team'}, inplace=True)
    training_camp_data.rename(columns={'Team': 'Team'}, inplace=True)
    mini_camp_data.rename(columns={'Team': 'Team'}, inplace=True)
    walk_through_data.rename(columns={'Team': 'Team'}, inplace=True)
    adv_stats.rename(columns={'Team': 'Team'}, inplace=True)
    head_to_head.rename(columns={'Team': 'Team'}, inplace=True)
    performers.rename(columns={'Team': 'Team'}, inplace=True)
    
    # Ensure all DataFrames have the same length
    max_length = max(len(historical_game_data), len(live_game_data), len(training_camp_data),
                     len(mini_camp_data), len(walk_through_data), len(adv_stats), len(head_to_head),
                     len(performers))
    
    # Pad DataFrames with NaNs to ensure they all have the same length
    def pad_df(df, max_length):
        if len(df) < max_length:
            df = pd.concat([df, pd.DataFrame(np.nan, index=range(max_length - len(df)), columns=df.columns)], ignore_index=True)
        return df
    
    historical_game_data = pad_df(historical_game_data, max_length)
    live_game_data = pad_df(live_game_data, max_length)
    training_camp_data = pad_df(training_camp_data, max_length)
    mini_camp_data = pad_df(mini_camp_data, max_length)
    walk_through_data = pad_df(walk_through_data, max_length)
    adv_stats = pad_df(adv_stats, max_length)
    head_to_head = pad_df(head_to_head, max_length)
    performers = pad_df(performers, max_length)

    return historical_game_data, live_game_data, training_camp_data, mini_camp_data, walk_through_data, adv_stats, head_to_head, performers

def predict_game():
    # Placeholder for actual prediction logic
    predicted_home_score = 24
    predicted_away_score = 27
    winner = "Packers"
    reason = "Based on recent performance and player stats."
    return predicted_home_score, predicted_away_score, winner, reason

def game_summary():
    historical_game_data, live_game_data, training_camp_data, mini_camp_data, walk_through_data, adv_stats, head_to_head, performers = compile_data()
    
    predicted_home_score, predicted_away_score, winner, reason = predict_game()
    
    summary = {
        'Historical Game Data': historical_game_data,
        'Live Game Data': live_game_data,
        'Training Camp Data': training_camp_data,
        'Mini Camp Data': mini_camp_data,
        'Walk Through Data': walk_through_data,
        'Advanced Statistics': adv_stats,
        'Head-to-Head Data': head_to_head,
        'Top Performers': performers,
        'Predicted Scores': {
            'Eagles': predicted_home_score,
            'Packers': predicted_away_score
        },
        'Prediction Reason': reason,
        'Predicted Winner': winner
    }
    
    return summary

# Fetch and display game summary
try:
    game_summary_data = game_summary()
    for key, value in game_summary_data.items():
        print(f"{key}:\n{value}\n")
except Exception as e:
    print(f"An error occurred: {e}")
