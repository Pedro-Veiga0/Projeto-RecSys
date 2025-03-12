import pandas as pd

movies = pd.read_csv(r'C:\Users\veigu\OneDrive\Ambiente de Trabalho\Projeto RecSys\exploracao_pedro\movies.csv', delimiter=';')

missing_values_m = movies.isnull().sum()
# print('MOVEIS', missing_values_m)

tamanho = len(movies.index)

movies = movies.drop(['imdb_title_id'], axis=1)

missing_values = movies.isnull().sum()

percentagem = (missing_values / tamanho) * 100

df = pd.DataFrame({
    'Missing Values': missing_values,
    'Percentagem': percentagem.round(2)
})

print(df.to_string())
indice = df[df['Percentagem']> 50 ].index
df.drop(indice, inplace=True) 
