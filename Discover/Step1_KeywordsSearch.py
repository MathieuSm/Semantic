import time 
import requests
import pandas as pd

# Define the API endpoint URL
url = 'http://api.semanticscholar.org/graph/v1/paper/search/bulk'

# Define the query parameters
QueryParams = {
    'query': 'plasticity + invariant + mechanics',
    'fields': 'title,url,citationCount,authors',
    # 'year': '2023-'
}

# Directly define the API key (Reminder: Securely handle API keys in production environments)
# api_key = 'your api key goes here'  # Replace with the actual API key

# Define headers with API key
# headers = {'x-api-key': api_key}

# Send the API request
Response = requests.get(url, params=QueryParams).json()

# save results to csv file
print(f'Will retrieve an estimated {Response['total']} documents')
Data = pd.DataFrame(Response['data'])
Retrieved = len(Data)
while Response['token'] != None:
    time.sleep(1)
    print(f'Retrieved {Retrieved} papers so far')
    QueryParams['token'] = Response['token']
    Response = requests.get(url, params=QueryParams).json()
    Data = pd.concat([Data, pd.DataFrame(Response['data'])])
    Retrieved += len(Response['data'])
print(f'Done! Retrieved {Retrieved} papers total')

Data = Data.sort_values('citationCount', ascending=False)
Data.to_csv('Papers.csv', index=False)
