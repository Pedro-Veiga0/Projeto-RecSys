import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns
from datetime import date, datetime
plt.style.use('ggplot') # estilo dos gráficos
pd.set_option('display.max_columns', 200) # quantidade de colunas que aparecem do nosso dataset

dataset_movies = pd.read_csv(r'C:\Users\BasilioCosta\Desktop\ines_ambiente_trabalho\mestrado\projeto_integrado\repositorio\Projeto-RecSys-1\exploracao_ines\movies.csv', sep = ';', encoding = 'ISO-8859-1') 
# coloquei encoding='ISO-8859-1' porque existem caracteres especiais no dataset que impedem que ele corra em UTF-8

dataset_ratings = pd.read_csv(r'C:\Users\BasilioCosta\Desktop\ines_ambiente_trabalho\mestrado\projeto_integrado\repositorio\Projeto-RecSys-1\exploracao_ines\ratings.csv', sep = ';') 
# este já não precisou de um encoding diferente, porque é um dataset numérico

datajoin = pd.concat([dataset_movies, dataset_ratings], axis = 1)

""" for col in datajoin.columns: # aqui confirmamos que a juncao dos datasets funcionou bem
    print(list(col))  """ 

# shift + alt + A faz o tipo de comentário acima

# ANÁLISE DO DATASET

#print(datajoin.shape) # temos inicialmente 85855 linhas e 71 colunas
#print(datajoin.head(20)) # 20 primeiras linhas do dataset
# como o pd por defeito não nos deixa ver as colunas todas e estamos a obter "imdb_title_id  ... non_us_voters_votes",
# então ativamos a condicao das linhas iniciais: pd.set_option('display.max_columns', 200)
#print(datajoin.columns) # nome das colunas 
#print(datajoin.dtypes) # tipo de variáveis de cada coluna

#print(datajoin.describe) # similar aos outros

# subset of our dataframe
df = datajoin[[#'imdb_title_id', 
        'title', 'original_title', 'year', 'date_published', 'genre', 'duration', 
        'country', 'language', 'director', 'writer', 'production_company', 'actors', 
        #'description', 
        'avg_vote', 'votes',       
        #'budget', 'usa_gross_income', 'worlwide_gross_income', 'metascore',       
        'reviews_from_users', 'reviews_from_critics', 
        #'imdb_title_id',
        'weighted_average_vote', 'total_votes', 'mean_vote', 'median_vote',       
        'votes_10', 'votes_9', 'votes_8', 'votes_7', 'votes_6', 'votes_5',        
        'votes_4', 'votes_3', 'votes_2', 'votes_1', 
        #'allgenders_0age_avg_vote', 'allgenders_0age_votes', 
        'allgenders_18age_avg_vote',
        'allgenders_18age_votes', 'allgenders_30age_avg_vote',
        'allgenders_30age_votes', 'allgenders_45age_avg_vote',
        'allgenders_45age_votes', 'males_allages_avg_vote',
        'males_allages_votes', 
        #'males_0age_avg_vote', 'males_0age_votes',
        'males_18age_avg_vote', 'males_18age_votes', 'males_30age_avg_vote',      
        'males_30age_votes', 'males_45age_avg_vote', 'males_45age_votes',
        'females_allages_avg_vote', 'females_allages_votes',
        #'females_0age_avg_vote', 'females_0age_votes', 
        'females_18age_avg_vote', 'females_18age_votes', 'females_30age_avg_vote', 'females_30age_votes',   
        'females_45age_avg_vote', 'females_45age_votes',
        'top1000_voters_rating', 'top1000_voters_votes', 'us_voters_rating',      
        'us_voters_votes', 'non_us_voters_rating', 'non_us_voters_votes']]

# retirei as colunas que não faziam sentido para o estudo que vamos fazer ou repetidas
# (provavelmente ainda vale a pena tirar mais) - mantive assim para ter nocao do que foi
# retirado

print(df)

#datajoin.drop(['females_18age_avg_vote'], axis = 1) outra maneira de retirar colunas 
# ao nosso dataset

# print(df.shape) podemos ver que o shape do nosso dataset mudou

print(df['year'].isnull().sum()) # existe 1 missing value nesta coluna
print(df[df['year'].isnull()]) # a linha onde está o missing value é a 83917

# a coluna 'year' tem o ano da coluna 'date_published', então só precisamos
# de usar a data que vem daí

df['date_published'] = pd.to_datetime(df['date_published'], format = '%d-%m-%Y', errors = 'coerce')
print(df['date_published'])

missyear = df.loc[df["year"] == 'NaN', "year"]
print(missyear)

missyear = pd.to_datetime(df['date_published'].values[83917].strftime("%Y"))
print(missyear)
""" df['year'] = df['year'].fillna(-1).astype(int)

print(pd.Int64Dtype(df['year']))
 """