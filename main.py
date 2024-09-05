import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay
import requests
from bs4 import BeautifulSoup

# Function to scrape data from the website
def scrape_nfl_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the div with id 'content'
        content_div = soup.find('div', {'id': 'content'})
        if content_div is None:
            print("No content div found on the webpage.")
            return None, None

        # Find the first table within the content div
        table = content_div.find('table')
        if table is None:
            print("No table found within the content div.")
            return None, None

        # Extract data from the table
        headers = [header.text.strip() for header in table.find_all('th')]
        data = []
        for row in table.find_all('tr')[1:]:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append(cols)

        # Check if the number of columns in the data matches the headers
        if len(data) > 0 and len(data[0]) == len(headers):
            return headers, data
        else:
            print("Mismatch between headers and data columns.")
            return None, None
    else:
        print(f"Failed to retrieve data from {url}")
        return None, None

# URL to scrape data from
url = 'https://www.pro-football-reference.com/teams/'

# Scrape the data
headers, nfl_data = scrape_nfl_data(url)

# Convert the scraped data to a DataFrame
if nfl_data and headers:
    nfl_df = pd.DataFrame(nfl_data, columns=headers)
    print(nfl_df)
else:
    print("No data was scraped from the webpage.")
    # Attempt to load data from a CSV file as a fallback
    try:
        nfl_df = pd.read_csv('nfl_scores_2015-2023.csv')
        print(nfl_df)
    except FileNotFoundError:
        print("CSV file not found. Please ensure the file 'nfl_scores_2015-2023.csv' is in the correct directory.")

# Rest of your code...
