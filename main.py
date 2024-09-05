import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier, NearestNeighbors
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay
import requests
from bs4 import BeautifulSoup

# Function to scrape data from the website
def scrape_nfl_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Extract the data you need from the soup object
        # This is an example, you need to adjust it based on the actual structure of the webpage
        data = []
        table = soup.find('table', {'id': 'team_stats'})
        for row in table.find_all('tr')[1:]:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append(cols)
        return data
    else:
        print(f"Failed to retrieve data from {url}")
        return None

# URL to scrape data from
url = 'https://www.pro-football-reference.com/teams/'

# Scrape the data
nfl_data = scrape_nfl_data(url)

# Convert the scraped data to a DataFrame
if nfl_data:
    columns = ['Column1', 'Column2', 'Column3']  # Adjust column names based on the actual data
    nfl_df = pd.DataFrame(nfl_data, columns=columns)
    print(nfl_df)

# Add some columns
nfl_df['True_Total'] = nfl_df['Tm_Pts'] + nfl_df['Opp_Pts']
nfl_df['Over'] = np.where(nfl_df['True_Total'] > nfl_df['Total'], 1, 0)
nfl_df['Under'] = np.where(nfl_df['True_Total'] < nfl_df['Total'], 1, 0)
nfl_df['Push'] = np.where(nfl_df['True_Total'] == nfl_df['Total'], 1, 0)
print(nfl_df)

for season in range(2021, 2024):
    print(nfl_df.query('Season == @season and Week == 1')['Under'].mean())

# Sort the data by Season, then by Week
nfl_df = nfl_df.sort_values(by=['Season','Week']).reset_index(drop=True)

# Create and Evaluate a Model for NFL Totals (1 = Under, 0 = Over or Push)
df = nfl_df.query('Home == 1').reset_index(drop=True)
features = ['Spread','Total']
target = 'Under'

for season in [2021, 2022, 2023]:
    print(f'\nResults for {season}:')
    y_preds = []
    y_trues = []
    for week in range(1, 19):
        print(f' Week {week:>2}:', end=' ')
        train_df = df.query('Season < @season or (Season == @season and Week < @week)')
        test_df = df.query('Season == @season and Week == @week and True_Total != Total')
        X_train = train_df[features]
        y_train = train_df[target]
        X_test = test_df[features]
        y_test = test_df[target]
        model = KNeighborsClassifier(n_neighbors=7)
        clf = model.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        y_true = y_test
        print(f'accuracy score={accuracy_score(y_true, y_pred):.2%}')
        y_preds += list(y_pred)
        y_trues += list(y_true)
    print(f'Season {season}: Total accuracy score={accuracy_score(y_trues, y_preds):.2%}')
    print(f'\nClassification Report for {season}:')
    print(classification_report(y_trues, y_preds, target_names=['Over','Under']))
    cm = confusion_matrix(y_trues, y_preds)
    display = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Over','Under'])
    display.plot()
    plt.grid(False)
    plt.show()

# Make predictions for NFL Totals (Season = 2024, Week = 1)
df = nfl_df.query('Home == 1').reset_index(drop=True)
features = ['Spread','Total']
target = 'Under'
season = 2024
week = 1
train_df = df.query('Season < @season or (Season == @season and Week < @week)')
X_train = train_df[features]
y_train = train_df[target]
week1 = [
    ['Ravens @ Chiefs', -3.0, 46.5],
    ['Packers @ Eagles', -1.5, 48.5],
    ['Cardinals @ Bills', -7.0, 48.0],
    ['Panthers @ Saints', -4.5, 40.5],
    ['Texans @ Colts', +2.0, 48.5]
]
X_new = pd.DataFrame(week1, columns=['Game','Spread','Total'])
model = KNeighborsClassifier(n_neighbors=7)
clf = model.fit(X_train, y_train)
y_pred = clf.predict(X_new[features])
X_new['KNC(7)'] = y_pred
X_new['KNC(7)'] = X_new['KNC(7)'].apply(lambda x: 'Under' if x == 1 else 'Over')
print(f'MODEL PREDICTIONS FOR WEEK {week} OF THE {season} NFL SEASON\n')
print(X_new[['Game','Spread','Total','KNC(7)']])
