import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt 

# NO METASCORE FOR MOVIES
# CASA
movies = pd.read_csv(r'C:\Users\veigu\OneDrive\Ambiente de Trabalho\Projeto RecSys\exploracao_pedro\movies_utf8.csv', delimiter=';')
ratings = pd.read_csv(r'C:\Users\veigu\OneDrive\Ambiente de Trabalho\Projeto RecSys\exploracao_pedro\ratings.csv', delimiter=';')

# portatil 
# movies = pd.read_csv(r'C:\Users\Pedro Afonso\Desktop\Trabalhos UM\1º Ano\2º Semestre\PIM\Projeto-RecSys\exploracao_pedro\movies_utf8.csv', delimiter=';')
# ratings = pd.read_csv(r'C:\Users\Pedro Afonso\Desktop\Trabalhos UM\1º Ano\2º Semestre\PIM\Projeto-RecSys\exploracao_pedro\ratings.csv', delimiter=';')
  
# print(movies.head())
# print(ratings.head())

junta = movies.merge(ratings, on='imdb_title_id')

# print(junta.head())

# missing_values = junta.isnull().sum()
# missing_values_m = movies.isnull().sum()
# missing_values_r = ratings.isnull().sum()
# print('MOVEIS', missing_values_m)
# print('RATINGS',missing_values_r)
# print(missing_values)

# print(junta.info())
# genero = movies['genre'].str.split(',').str[0].str.strip()
# sns.countplot(movies, x=genero, stat="percent", palette="husl")
# intervalos = pd.cut(movies['duration'], bins=[0, 30, 60, 90, 120, float('inf')], labels=['0-30', '31-60', '61-90', '91-120', '120+'])
# sns.kdeplot(movies, x='avg_vote', hue=intervalos, fill=True, palette='husl')
 
# intervalos = pd.cut(ratings['weighted_average_vote'], bins=[0, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 10], labels=['0-2.5', '2.5-3.5', '3.5-4.5', '4.5-5.5', '5.5-6.5', '6.5-7.5', '7.5-8.5', '8.5-10'])
sns.countplot(x=junta['weighted_average_vote'], stat="count", palette="husl")
plt.tight_layout()
plt.show()