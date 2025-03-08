import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt 

# CASA
# movies = pd.read_csv(r'C:\Users\veigu\OneDrive\Ambiente de Trabalho\Projeto RecSys\movies_utf8.csv', delimiter=';')
# ratings = pd.read_csv(r'C:\Users\veigu\OneDrive\Ambiente de Trabalho\Projeto RecSys\ratings.csv', delimiter=';')

# portatil 
movies = pd.read_csv(r'C:\Users\Pedro Afonso\Desktop\Trabalhos UM\1º Ano\2º Semestre\PIM\Projeto-RecSys\exploracao_pedro\movies_utf8.csv', delimiter=';')
ratings = pd.read_csv(r'C:\Users\Pedro Afonso\Desktop\Trabalhos UM\1º Ano\2º Semestre\PIM\Projeto-RecSys\exploracao_pedro\ratings.csv', delimiter=';')
  
# print(movies.head())
# print(ratings.head())

junta = movies.merge(ratings, on='imdb_title_id')

# print(junta.head())

# missing_values = junta.isnull().sum()
# missing_values_m = movies.isnull().sum()
# missing_values_r = ratings.isnull().sum()
# print('MOVEIS', missing_values_m)
# print('RATINGS',missing_values_r)

# print(junta.info())

sns.countplot(movies, x="date_published")
plt.show()