import pandas as pd

ratings = pd.read_csv(r'C:\Users\veigu\OneDrive\Ambiente de Trabalho\Projeto RecSys\exploracao_pedro\ratings.csv', delimiter=';')

tamanho = len(ratings.index)

ratings = ratings.drop(['imdb_title_id'], axis=1)

missing_values = ratings.isnull().sum()

percentagem = (missing_values / tamanho) * 100

df = pd.DataFrame({
    'Missing Values': missing_values,
    'Percentagem': percentagem.round(2)
})

indice = df[df['Percentagem']> 50 ].index
df.drop(indice, inplace=True) 

# print(df.to_string())

dados = ratings[~ratings.isna()]
colunas = [
    "allgenders_0age_votes", "allgenders_18age_votes",
    "allgenders_30age_votes", "allgenders_45age_votes",
    "males_allages_votes", "males_0age_votes", "males_18age_votes",
    "males_30age_votes", "males_45age_votes",
    "females_allages_votes", "females_0age_votes", "females_18age_votes",
    "females_30age_votes", "females_45age_votes",
    "top1000_voters_votes", "us_voters_votes", "non_us_voters_votes"
]

votos_total = dados['total_votes'].sum()
colunas_a_remover = []

for coluna in colunas:
    votos_demografia = dados[coluna].sum()
    proporcao =  votos_demografia / votos_total
    print('Proporção de votos em percentagem da coluna', coluna, proporcao.round(2)*100)
    if proporcao < .10:
        colunas_a_remover.append(coluna)
    proporcao = 0
print(colunas_a_remover)
