import requests

# Replace 'YOUR_API_KEY' with your actual API key
api_key = 'YOUR_API_KEY'
url = f'https://api.the-odds-api.com/v4/sports?apiKey={api_key}'

response = requests.get(url)
data = response.json()

print(data)
