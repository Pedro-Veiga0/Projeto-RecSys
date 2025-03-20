import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

ratings = pd.read_csv(r'C:\Users\veigu\OneDrive\Ambiente de Trabalho\Projeto RecSys\exploracao_pedro\ratings.csv', delimiter=';')
movies = pd.read_csv(r'C:\Users\veigu\OneDrive\Ambiente de Trabalho\Projeto RecSys\exploracao_pedro\movies.csv', delimiter=';')

movie_data = pd.merge(movies, ratings, on="imdb_title_id")

features = ['weighted_average_vote']

movie_features = movie_data[['imdb_title_id'] + features].set_index('imdb_title_id')

normaliza = (movie_features-movie_features.min())/(movie_features.max()-movie_features.min())
#diminiu tamanho de linhas para processar
subset_size = 10000
subset_normaliza = normaliza.head(subset_size)
coseno = cosine_similarity(subset_normaliza)

# print(movie_data['total_votes'].idxmax())
id_to_index = {id: index for index, id in enumerate(subset_normaliza.index)}
index_to_id = {index: id for id, index in id_to_index.items()}

def recomenda(titulo):
    movie_match = movie_data[movie_data.original_title == titulo]
    movie_id = movie_match["imdb_title_id"].values[0]
    matrix_index = id_to_index[movie_id]
    scores = list(enumerate(coseno[matrix_index]))
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    sorted_scores = sorted_scores[1:]
    movies = [movie_data[movie_data["imdb_title_id"] == index_to_id[movie[0]]]["title"].values[0] for movie in sorted_scores]
    return movies

def recommend_ten(movie_list):
    return movie_list[:10]

titulo = "The Fast and the Furious"
lst = recomenda(titulo)
m = recommend_ten(lst)
print(f"Top 10 recommendations for '{titulo}':")
for i, movie in enumerate(m, 1):
    print(f"{i}. {movie}")

#É NECESSÁRIO USER ID PARA REALIZAR ISTO POIS SENÃO É APENAS UMA APROXIMAÇÃO DE UM CONTENT-BASED FITERING