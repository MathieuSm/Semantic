import requests
import pandas as pd


Data = pd.read_csv('Papers.csv')
for i in range(10):
    print(i, Data['title'][i])

PositivePaperIds = [2, ]
NegativePaperIds = [4, ]

# Define the API endpoint URL
URL = 'https://api.semanticscholar.org/recommendations/v1/papers'

# Define the query parameters
QueryParams = {
    'fields': 'title,url,citationCount,authors',
    'limit': '500'
}

# Define the request data
Seed = {'positivePaperIds': [Data.loc[i,'paperId'] for i in PositivePaperIds],
        'negativePaperIds': [Data.loc[i,'paperId'] for i in NegativePaperIds]}

# Directly define the API key (Reminder: Securely handle API keys in production environments)
# api_key = "your api key goes here"  # Replace with the actual API key

# Define headers with API key
# headers = {"x-api-key": api_key}

# Send the API request
Response = requests.post(URL, params=QueryParams, json=Seed).json()#, headers=headers).json()

# Sort the recommended papers by citation count
Papers = pd.DataFrame(Response['recommendedPapers'])
Papers = Data.sort_values('citationCount', ascending=False)
Papers.to_csv('RecommendedPapers.csv', index=False)
