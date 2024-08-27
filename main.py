import requests

# Define the API URL
url = "https://data.oddalerts.com/api/trends/homeWin?api_token=jPL5UFhVkTPSqzfJo"

# Make a GET request to the API
response = requests.get(url)

# Parse the JSON response
data = response.json()

# Loop through the data and print the home team name and their win percentage
for item in data['data']:
    print(f"Team: {item['home_name']}, Win Percentage: {item['home_win_per']}%")
