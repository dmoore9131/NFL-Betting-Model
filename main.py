import pandas as pd
import requests

# Define rosters for Packers and Eagles
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
        'Britain Covey', 'Isaiah Rodgers O', 'Rick Lovato'
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
        '-', '-', '-', '-', 'Travis Glover', 'Brenton Cox Jr.', 'Colby Wooden', 'Jonathan Ford IR', 'Arron Mosby O',
        '-', '-', '-', 'LJ Davis IR', '-', '-', '-', '-', '-', '-', '-'
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
        'Keisean Nixon', 'Matt Orzech'
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
        '-', '-', '-', 'LJ Davis IR', '-', '-', '-', '-', '-', '-', '-'
    ],
    '4th': [
        '-', 'AJ Dillon IR', '-', '-', '-', 'Tyler Davis IR', '-', '-', '-', '-',
        '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'
    ]
}

# Function to fetch live rosters using ESPN API
def get_team_roster(team_id):
    url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{team_id}"
    response = requests.get(url)
    data = response.json()
    roster = data['team']['roster']['entries']
    return roster

# Define the 2024 rosters for other teams
def fetch_all_team_rosters():
    teams = [
        '49ers', 'Bears', 'Bengals', 'Bills', 'Broncos', 'Browns', 'Buccaneers', 'Cardinals',
        'Chargers', 'Chiefs', 'Colts', 'Commanders', 'Cowboys', 'Dolphins', 'Falcons', 'Giants',
        'Jaguars', 'Jets', 'Lions', 'Panthers', 'Patriots', 'Raiders', 'Rams', 'Ravens', 'Saints',
        'Seahawks', 'Steelers', 'Texans', 'Titans', 'Vikings'
    ]
    
    team_ids = {
        '49ers': '1', 'Bears': '2', 'Bengals': '3', 'Bills': '4', 'Broncos': '5', 'Browns': '6',
        'Buccaneers': '7', 'Cardinals': '8', 'Chargers': '9', 'Chiefs': '10', 'Colts': '11',
        'Commanders': '12', 'Cowboys': '13', 'Dolphins': '14', 'Falcons': '15', 'Giants': '16',
        'Jaguars': '17', 'Jets': '18', 'Lions': '19', 'Panthers': '20', 'Patriots': '21',
        'Raiders': '22', 'Rams': '23', 'Ravens': '24', 'Saints': '25', 'Seahawks': '26',
        'Steelers': '27', 'Texans': '28', 'Titans': '29', 'Vikings': '30'
    }
    
    teams_rosters = {}
    for team in teams:
        team_id = team_ids[team]
        teams_rosters[team] = get_team_roster(team_id)
    
    return teams_rosters

def fetch_game_data(game_id):
    # Simulated game data for demonstration
    game_data = {
        1: {
            'Historical': pd.DataFrame({
                'Game': ['Packers vs Eagles'] * 10,
                'Home Team': ['Eagles'] * 10,
                'Away Team': ['Packers'] * 10,
                'Home Score': [24] * 10,
                'Away Score': [27] * 10
            }),
            'Live': pd.DataFrame({
                'Team': ['Packers', 'Eagles'],
                'Current Score': [28, 21]
            }),
            'Player Stats': pd.DataFrame({
                'Team': ['Packers'] * 5 + ['Eagles'] * 5,
                'Player': ['Jordan Love', 'Josh Jacobs', 'Christian Watson', 'Romeo Doubs', 'Jayden Reed',
                           'Jalen Hurts', 'Saquon Barkley', 'A.J. Brown', 'DeVonta Smith', 'Dallas Goedert'],
                'Position': ['QB', 'RB', 'WR', 'WR', 'WR', 'QB', 'RB', 'WR', 'WR', 'TE'],
                'Yards': [320, 95, 85, 90, 100, 340, 95, 105, 90, 85],
                'Touchdowns': [3, 1, 1, 1, 1, 3, 1, 2, 1, 1],
                'PFF Grade': [88, 75, 80, 82, 85, 90, 78, 89, 87, 83]  # Example PFF grades
            }),
            'Injury Reports': pd.DataFrame({
                'Player': ['Christian Watson', 'Romeo Doubs', 'Jalen Hurts', 'Saquon Barkley', 'Dallas Goedert'],
                'Team': ['Packers'] * 2 + ['Eagles'] * 3,
                'Injury': ['Hamstring', 'Ankle', 'Shoulder', 'Knee', 'Calf'],
                'Status': ['Doubtful', 'Questionable', 'Probable', 'Out', 'Questionable']
            })
        }
    }
    
    game = game_data.get(game_id, None)
    if game:
        # Fantasy Draft Decisions
        fantasy_advice = {
            'Packers': {
                'start': [player for player in game['Player Stats'].query("Team == 'Packers' and Position in ['WR', 'RB']")['Player'].tolist() if player not in game['Injury Reports'].query("Status == 'Out'")['Player'].tolist()],
                'sit': [player for player in game['Player Stats'].query("Team == 'Packers' and Position in ['WR', 'RB']")['Player'].tolist() if player in game['Injury Reports'].query("Status == 'Out'")['Player'].tolist()]
            },
            'Eagles': {
                'start': [player for player in game['Player Stats'].query("Team == 'Eagles' and Position in ['WR', 'RB']")['Player'].tolist() if player not in game['Injury Reports'].query("Status == 'Out'")['Player'].tolist()],
                'sit': [player for player in game['Player Stats'].query("Team == 'Eagles' and Position in ['WR', 'RB']")['Player'].tolist() if player in game['Injury Reports'].query("Status == 'Out'")['Player'].tolist()]
            }
        }

        # Determine who gets the most targets
        def most_targets(team, injured_players):
            players = game['Player Stats'].query(f"Team == '{team}' and Position == 'WR' or Position == 'RB'")
            if injured_players:
                players = players[~players['Player'].isin(injured_players)]
            return players.sort_values(by='Yards', ascending=False).iloc[0]['Player'] if not players.empty else 'No available players'

        injured_players_packers = game['Injury Reports'].query("Team == 'Packers' and Status != 'Probable'")['Player'].tolist()
        injured_players_eagles = game['Injury Reports'].query("Team == 'Eagles' and Status != 'Probable'")['Player'].tolist()

        most_targets_packers = most_targets('Packers', injured_players_packers)
        most_targets_eagles = most_targets('Eagles', injured_players_eagles)

        return {
            'Historical': game['Historical'],
            'Live': game['Live'],
            'Player Stats': game['Player Stats'],
            'Injury Reports': game['Injury Reports'],
            'Fantasy Draft Decisions': fantasy_advice,
            'Most Targets Packers': most_targets_packers,
            'Most Targets Eagles': most_targets_eagles
        }
    
    return None

# Example Usage:
game_data = fetch_game_data(1)
print(game_data['Historical'])
print(game_data['Live'])
print(game_data['Player Stats'])
print(game_data['Injury Reports'])
print("Fantasy Draft Decisions:")
print(game_data['Fantasy Draft Decisions'])
print("Most Targets Packers:", game_data['Most Targets Packers'])
print("Most Targets Eagles:", game_data['Most Targets Eagles'])
