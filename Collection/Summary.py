import pandas as pd
import matplotlib.pyplot as plt

AuC = pd.read_csv('AuthorsCollection.csv')

for Idx, Row in AuC.iterrows():
    N = len(Row['Paper IDs'].split(' '))
    AuC.loc[Idx, 'Num Papers'] = N

Sorted = AuC.sort_values('Num Papers', ascending=False)
N = 10

Figure, Axis = plt.subplots(1,1)
Axis.bar(Sorted['Author Name'].head(N), Sorted['Num Papers'].head(N))
Axis.set_title(f'Top {N} authors by number of papers')
Axis.set_ylabel('Number of papers')
Axis.set_xlabel('Author name')
Axis.tick_params(axis='x', rotation=45)
plt.show(Figure)

