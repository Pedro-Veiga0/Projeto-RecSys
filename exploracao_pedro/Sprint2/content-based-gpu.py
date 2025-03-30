import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

#SÓ LÊ ATÉ ÀS 25K PRIMEIRAS ROWS
data = pd.read_csv(r'C:\Users\veigu\OneDrive\Ambiente de Trabalho\Projeto RecSys\exploracao_pedro\movies.csv', delimiter=';', nrows=2000)

#REMOVE ROWS COM MISSING VALUES NAQUELAS COLUNAS
data.dropna(subset=['actors','director','writer','original_title','description','genre'],inplace=True,axis=0)

# data.drop(columns=['title','imdb_title_id','date_published','duration','country','language','reviews_from_critics','production_company','avg_vote','votes','budget','usa_gross_income','worlwide_gross_income','metascore','reviews_from_users'])
data = data.reset_index(drop=True)

#TRANSFORMA TEXTO DE CADA ROW EM UMA LISTA
data['description'] = [re.sub(r'[^\w\s]', '', t) for t in data['description']]
data['actors'] = [re.sub(',',' ',re.sub(' ','',t)) for t in data['actors']]
data['director'] = [re.sub(',',' ',re.sub(' ','',t)) for t in data['director']]
data['writer'] = [re.sub(',',' ',re.sub(' ','',t)) for t in data['writer']]
data['original_title'] = [re.sub(r'[^\w\s]', '', t) for t in data['original_title']]
data['genre'] = [re.sub(',',' ',re.sub(' ','',t)) for t in data['genre']]

#JUNTA TUDO PARA UMA NOVA COLUNA
#NOTA: SE REMOVER DATA-DIRECTOR-WRITER A MATRIZ FICAA LIGEIRAMENTE +PEQUENA
data["combined"] = data['genre'] + '  ' + data['actors'] + ' ' + data['director'] + ' ' + data['writer'] + ' ' + data['original_title'] + ' ' + data['description']
data.drop(['actors','director','writer','description','genre'],axis=1,inplace=True)

#VECTORIZER PEGA EM CADA PALAVRA DO TEXTO E SEPARA-A NA LISTA SEM REPETIR PALAVRAS
vectorizer = TfidfVectorizer()
matrix = vectorizer.fit_transform(data["combined"])
# linhas, colunas = matrix.shape
# print('---------SHAPE--------',linhas, colunas)
# print(matrix)

#UTILIZA O LINEAR_KERNEL (SEMELHANTE E +RÁPIDO QUE O COSINE_SIMILARITY) PARA CALCULAR A MATRIZ
cosine_similarities = linear_kernel(matrix,matrix)
movie_title = data['original_title']
indices = pd.Series(data.index, index=data['original_title'])

#FUNÇÃO PARA ENUMERAR OS FILMES + SEMELHANTES AO ESCOLHIDO
def content_recommender(title):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_similarities[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return movie_title.iloc[movie_indices]

print(content_recommender('The Godfather'))


#+NOTAS:the TF-IDF (Term Frequency-Inverse Document Frequency) metric is used to measure the importance of a word in a document relative to a collection of documents (corpus). 

#The fit_transform() method performs two operations: Fit: It learns the vocabulary of all unique words in data["combined"] and computes their IDF scores. Transform: It converts each document into a numerical vector where each value corresponds to the TF-IDF score of a word in that document.

#LINK KAGGLE - https://www.kaggle.com/code/omeroruccelik/content-based-recommendation-systems