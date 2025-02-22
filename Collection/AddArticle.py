import requests
import pandas as pd


# Define the API endpoint URL
# url = 'https://api.semanticscholar.org/graph/v1/paper/search/'
url = 'https://api.semanticscholar.org/graph/v1/paper/search/match'

# Define the query parameters
QueryParams = {
    'query': "'Bone Development and Growth'",
    'fields': 'authors,year,title,abstract'}

# Directly define the API key (Reminder: Securely handle API keys in production environments)
# api_key = 'your api key goes here'  # Replace with the actual API key

# Define headers with API key
# headers = {'x-api-key': api_key}

# Send the API request
Response = requests.get(url, params=QueryParams).json()
print(f'Found {len(Response['data'])} article(s) matching the query')

for A, Article in enumerate(Response['data']):
    print(f'Article {A}:')
    for ArtData in Article.keys():
        print(ArtData, Article[ArtData])

# Select the article to add to the collection
ArtIdx = 0
Article = Response['data'][ArtIdx]

# Add the article to the collection
ArC = pd.read_csv('ArticlesCollection.csv',sep=';')
if Article['paperId'] not in ArC['Paper ID'].values:
    Authors = [A['name'] for A in Article['authors']]
    if Article['abstract'] is None:
        Article['abstract'] = ''
    Data = {'Authors': ' and '.join(Authors),
            'Year': int(Article['year']),
            'Paper ID': Article['paperId'],
            'Title': Article['title'],
            'Abstract': Article['abstract']}
    Idx = len(ArC)
    ArC.loc[Idx] = Data
    ArC.to_csv('ArticlesCollection.csv', index=False, sep=';')
    print('Article added to the collection')

# Add the authors to the collection
AuC = pd.read_csv('AuthorsCollection.csv')
for Author in Article['authors']:
    ID = int(Author['authorId'])
    if ID not in AuC['Author ID'].values.astype(int):
        Data = {'Author Name': Author['name'],
                'Author ID': Author['authorId'],
                'Paper IDs': Article['paperId']}
        Idx = len(AuC)
        AuC.loc[Idx] = Data

    else:
        Idx = AuC[AuC['Author ID'].astype(int) == ID].index[0]
        PaperIDs = AuC.loc[Idx, 'Paper IDs'].split(' ')
        if Article['paperId'] not in PaperIDs:
            PaperIDs.append(Article['paperId'])
            AuC.loc[Idx, 'Paper IDs'] = ' '.join(PaperIDs)
AuC.to_csv('AuthorsCollection.csv', index=False)
print('Author added to the collection')