import requests
import pandas as pd

Data = pd.read_csv('RecommendedPapers.csv')

AuthorsIds = []
for Idx, Row in Data.head(10).iterrows():
    Split = Row['authors'].split('\'')
    for s, S in enumerate(Split):
        if 'authorId' == S:
            AuthorsIds.append(Split[s+2])
AuthorsIds = list(set(AuthorsIds))

# Define the API endpoint URL
URL = 'https://api.semanticscholar.org/graph/v1/author/batch'

# Define the query parameters
QueryParams = {'fields': 'name,url,paperCount,hIndex,papers'}

# Define the request data
Data = {'ids': AuthorsIds}

# Directly define the API key (Reminder: Securely handle API keys in production environments)
# api_key = "your api key goes here"  # Replace with the actual API key

# Define headers with API key
# headers = {"x-api-key": api_key}

# Send the API request
Response = requests.post(URL, params=QueryParams, json=Data).json()

Results = pd.DataFrame(Response)
Results = Results.sort_values('hIndex', ascending=False)
print('Most influent authors:')
print(Results[['name','paperCount','hIndex']].head(10))