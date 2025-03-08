import pandas as pd
import numpy as np 

movies = pd.read_csv(r'C:\Users\veigu\OneDrive\Ambiente de Trabalho\Projeto RecSys\movies_utf8.csv', encoding='latin-1', delimiter=';')
ratings = pd.read_csv(r'C:\Users\veigu\OneDrive\Ambiente de Trabalho\Projeto RecSys\ratings.csv', encoding='latin-1', delimiter=';')
  
print(movies.head())
print(ratings.head())