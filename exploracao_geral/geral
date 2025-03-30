import numpy as np # array-processing package
import pandas as pd # data analysis toolkit
import matplotlib.pyplot as plt # static, animated and interactive visualizations
import seaborn as sns # data visualization library
import re # regular expressions
from sklearn.metrics.pairwise import cosine_similarity # computes cosine similarity between samples
from sklearn.preprocessing import StandardScaler # standardizes features by removing the mean and scaling to unit variance
from scipy.sparse import csr_matrix # sparse matrix package for numeric data


#----- Loading the datasets ----------------------------------------------------------------------------------------------------------------------------------------------------

#movies = pd.read_csv('datasets/imbd_movies.csv', sep = ";", encoding = "latin1")
#moviesaux = pd.read_csv('datasets/imdb_movies.csv', sep=";", encoding="latin1")
#ratings = pd.read_csv('datasets/imdb_ratings.csv', sep = ";")
#ratingsaux = pd.read_csv('datasets/imdb_ratings.csv', sep=";")

movies = pd.read_csv(r'C:/Users/Asus/Desktop/mestrado/projeto_integrado_matematica_computacao/Projeto-RecSys/exploracao_jessica/datasets/imdb_movies.csv', encoding = 'UTF-8', sep = ';') 
moviesaux = pd.read_csv(r'C:/Users/Asus/Desktop/mestrado/projeto_integrado_matematica_computacao/Projeto-RecSys/exploracao_jessica/datasets/imdb_movies.csv', encoding = 'UTF-8', sep = ';') 
ratings = pd.read_csv(r'C:/Users/Asus/Desktop/mestrado/projeto_integrado_matematica_computacao/Projeto-RecSys/exploracao_jessica/datasets/imdb_ratings.csv', encoding = 'UTF-8', sep = ';')
ratingsaux = pd.read_csv(r'C:/Users/Asus/Desktop/mestrado/projeto_integrado_matematica_computacao/Projeto-RecSys/exploracao_jessica/datasets/imdb_ratings.csv', encoding = 'UTF-8', sep = ';')

imdb_merged = pd.merge(movies, ratings, how = "inner", on = "imdb_title_id")


#---- Data analysis  -----------------------------------------------------------------------------------------------------------------------

missing_values_m = moviesaux.isnull().sum()
# print('MOVIES', missing_values_m)

tamanho = len(movies.index)

moviesaux = moviesaux.drop(['imdb_title_id'], axis = 1)

missing_values = movies.isnull().sum()

percentagem = (missing_values / tamanho) * 100

df = pd.DataFrame({
    'Missing Values': missing_values,
    'Percentagem': percentagem.round(2)
})

#print(df.to_string())
indice = df[df['Percentagem']> 50 ].index
movies = movies.drop(columns=indice)

#---------------------------------------------------------------

tamanho = len(ratings.index)

ratingsaux = ratingsaux.drop(['imdb_title_id'], axis=1)

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
    #print('Proporção de votos em percentagem da coluna', coluna, proporcao.round(2)*100)
    if proporcao < .10:
        colunas_a_remover.append(coluna)
    proporcao = 0

ratings = ratings.drop(columns = indice)

#---------------------------------------------------------------

# Complement country and language 
# Note: agg() applies a function to the group; lambda is an anonymous function; empty checks if the mode is empty
country_mode_per_language = imdb_merged.groupby("language")["country"].agg(lambda x: x.mode()[0] if not x.mode().empty else "NA")
language_mode_per_country = imdb_merged.groupby("country")["language"].agg(lambda x: x.mode()[0] if not x.mode().empty else "NA")

# Fill country with the mode of language
# Note: .map() maps values of series according to input correspondence
imdb_merged.loc[imdb_merged["country"].isna(), "country"] = imdb_merged["language"].map(country_mode_per_language)
# Fill language with the mode of country
imdb_merged.loc[imdb_merged["language"].isna(), "language"] = imdb_merged["country"].map(language_mode_per_country)
# Fill the remaining missing values with NA
imdb_merged.fillna({"country": "NA", "language": "NA"}, inplace = True)

#---------------------------------------------------------------

# Handle date_published
# Check if the date_published column is in the format dd-mm-yyyy
def transform_date_format(x):

    if isinstance(x, str):

        if re.match(r'^\d{4}-\d{2}-\d{2}$', x): # if the date is in the format yyyy-mm-dd
            date = pd.to_datetime(x)
            return date.strftime('%d-%m-%Y')

        elif re.match(r'^\d{4}$', x):  # if the date is only the year
            return f"01-01-{x}"  # return a date with day 01 and month 01: here it can become random if we want, but it is not relevant

    return x # if the date is already in the format dd-mm-yyyy


imdb_merged['date_published'] = imdb_merged['date_published'].apply(transform_date_format)

#print(imdb_merged.info())


#----- Handle data types ----------------------------------------------------------------------------------------------------------------------------------------------------

# Note: optimization of the data types reduces memory usage and improves processing speed while preserving the necessary precision

#for coluna in imdb_merged.select_dtypes(include = ["int64"]).columns:
#    print(f"{coluna}: min = {imdb_merged[coluna].min()}, max = {imdb_merged[coluna].max()}")

#for coluna in imdb_merged.select_dtypes(include = ["float64"]).columns:
#    print(f"{coluna}: min = {imdb_merged[coluna].min()}, max = {imdb_merged[coluna].max()}")

#print(np.iinfo(np.int8))
#print(np.iinfo(np.int16))
#print(np.iinfo(np.int32))

# Floats
for coluna in imdb_merged.select_dtypes(include = ["float64"]).columns:
    imdb_merged[coluna] = imdb_merged[coluna].astype("float32")

    #if re.search(r"avg|rating|metascore|mean", coluna): 
    #    imdb_merged[coluna] = imdb_merged[coluna].astype("float16")

    #else: 
    #    imdb_merged[coluna] = imdb_merged[coluna].astype("int64")

# Integers
for coluna in imdb_merged.select_dtypes(include = ["int64"]).columns:
    minimo = imdb_merged[coluna].min()
    maximo = imdb_merged[coluna].max()

    if minimo >= -128 and maximo <= 127:
        imdb_merged[coluna] = imdb_merged[coluna].astype("int8")

    elif minimo >= -32768 and maximo <= 32767:
        imdb_merged[coluna] = imdb_merged[coluna].astype("int16")

    elif minimo >= -2147483648 and maximo <= 2147483647:
        imdb_merged[coluna] = imdb_merged[coluna].astype("int32")

#print(imdb_merged.info()) # check the size of the dataset and the changed types

#---------------------------------------------------------------

# PARA OS DADOS DE TEXTO:

colunas_a_processar = ['genre', 'country', 'language', 'director', 'writer', 'production_company', 'actors']
# achei que estas fizessem mais sentido 

# Armazenar os resultados
listas_unicas = {}  # Armazena os valores de cada coluna, apenas um de cada
mais_comuns = {}  # Armazena os 3 mais comuns

# Função para processar cada coluna
def processar_coluna(df, coluna):
    todos_os_valores = df[coluna].dropna().str.split(', ').explode() # aqui remove os missing values
    # separa os valores de cada linha por vírgulas e coloca-os em linhas diferentes
    lista_unica = sorted(todos_os_valores.unique().tolist())  # Lista ordenada dos valores que existem
    contagem = Counter(todos_os_valores)  # Freqência de cada valor
    mais_comuns = contagem.most_common(3)  # 3 mais comuns
    return lista_unica, mais_comuns

# Aplicar a função a cada coluna e armazenar os resultados
for coluna in colunas_a_processar:
    listas_unicas[coluna], mais_comuns[coluna] = processar_coluna(df, coluna)

'''
for coluna in colunas_a_processar:
    print(f"\nColuna: {coluna}")
    print(f"Valores únicos ordenados: {listas_unicas[coluna]}")
    print(f"Top 3 mais comuns: {mais_comuns[coluna]}")"
'''


# LINHAS DUPLICADAS - INEXISTENTES:

# apesar de haver muitas linhas com valores que parecem estar duplicados, na realidade, se formos a comparar os valores
# 'title', 'year' e 'language', percebemos que as linhas apenas parecem estar duplicadas; existem filmes que têm o mesmo 
# nome mas que foram publicados em anos diferentes ou que estão em línguas diferentes 

#print(df.loc[df.duplicated(subset = ['title', 'year', 'language'])])



#----- Item-Based Collaborative Filtering ----------------------------------------------------------------------------------------------------------------------------------------------------


# Item Based Collaborative Filtering - recommends items based on similarity with the items that the target user rated. 
# The similarity can be computed with Pearson Correlation or Cosine Similarity. 


# Select relevant columns of a random sample
# Note: we can't use the entire dataset, otherwise it will take too long to run the code
imdb_merged = imdb_merged.sample(n = 5000, random_state = 3112) # set seed
ratings = imdb_merged[['title', 'avg_vote']]

# Pivot table: each movie as a row, avg_vote as features
movie_ratings = ratings.pivot_table(index = 'title', values = 'avg_vote')

# Normalize the ratings
# Note: StandardScaler standardizes features by removing the mean and scaling to unit variance
# Note: fit_transform() fits to data, then transforms it
scaler = StandardScaler()
movie_ratings_scaled = scaler.fit_transform(movie_ratings)

# Convert to sparse matrix to save memory
# Note: csr_matrix() compresses the sparse matrix
movie_ratings_sparse = csr_matrix(movie_ratings_scaled)

# Split dataset using indices
num_splits = 10
index_chunks = np.array_split(movie_ratings.index, num_splits)

# Compute similarity in chunks and store results in a dictionary
similarity_dict = {}

for i in range(num_splits):
    for j in range(num_splits):
        # Extract submatrices from the sparse matrix
        rows = list(index_chunks[i])
        cols = list(index_chunks[j])
        
        movie_chunk_i = movie_ratings_sparse[movie_ratings.index.isin(rows)]
        movie_chunk_j = movie_ratings_sparse[movie_ratings.index.isin(cols)]
        
        # Compute cosine similarity for the chunk
        sim_chunk = cosine_similarity(movie_chunk_i, movie_chunk_j)
        similarity_dict[(i, j)] = sim_chunk

# Recommend 'n' most similar movies to a given movie title based on similarity chunks
def recommend_movies(movie_title, n = 5):
    
    if movie_title not in movie_ratings.index:
        return f"Movie {movie_title} not found."

    # Identify the chunk containing the movie
    row_chunk_idx, row_idx_in_chunk = None, None

    for i, index_chunk in enumerate(index_chunks):
        if movie_title in index_chunk:
            row_chunk_idx = i
            row_idx_in_chunk = list(index_chunk).index(movie_title)
            break  # exit loop once found

    if row_chunk_idx is None or row_idx_in_chunk is None:
        return f"Movie {movie_title} not found in any chunk."

    # Collect similarities from all chunks
    # Note: hstack() stacks arrays in sequence column-wise
    similarities = np.hstack([similarity_dict[(row_chunk_idx, j)][row_idx_in_chunk] for j in range(num_splits)])

    # Get top 'n' similar movies (excluding self)
    # Note: argsort()[::-1] returns the indices in descending order in order to get the most similar movies first
    sorted_indices = np.argsort(similarities)[::-1][1 : n+1] # start from 1 to exclude the movie itself

    # Retrieve recommended movies
    recommended_movie_ids = movie_ratings.index[sorted_indices]

    return imdb_merged[imdb_merged['title'].isin(recommended_movie_ids)][['title', 'description', 'avg_vote']]


# Tryout
# Note: we can't select a movie manually that is not in the sample
movie_example = imdb_merged.sample(n = 1, random_state = 3112) # set seed
print("Selected movie:")
print(f"title: {movie_example['title'].values[0]}, description: {movie_example['description'].values[0]}, avg_vote: {movie_example['avg_vote'].values[0]}")
print("\n--------------------\n")


recommendations = recommend_movies(movie_example['title'].values[0], n = 5)
print("Movies recommendations:")
print(recommendations)



#---------------------------------------------------------------------------------------------------------------------------------------
#USER-BASED COLLABORATIVE FILTERING
#---------------------------------------------------------------------------------------------------------------------------------------

user_ratings = pd.read_csv("user_ratings.csv") 

user_movie_matrix = user_ratings.pivot(index = ' User ID ', columns = ' Movie ID ', values = ' User Rating ')
user_movie_matrix = user_movie_matrix.fillna(0)
#print(user_movie_matrix)

#Calcular similaridade entre filmes através de Cosine Similarity
#user_similarity = cosine_similarity(user_movie_matrix)
user_similarity = user_movie_matrix.T.corr(method='pearson')
user_similarity_df = pd.DataFrame(user_similarity, index=user_movie_matrix.index, columns=user_movie_matrix.index)
#print(user_similarity_df.head())

def recomendar_UBC(user_id, num_rec):

    similares_users = user_similarity_df[user_id].drop(user_id).sort_values(ascending=False)
    #print(similares_users)
    
    # Pesar os ratings pelos coeficientes de similaridade
    weighted_ratings = user_movie_matrix.loc[similares_users.index].T.dot(similares_users) / similares_users.sum()
    user_rated_movies = user_movie_matrix.loc[user_id] # Remover filmes já avaliados pelo utilizador
    #acc = user_rated_movies
    #acc = [get_titulo(movie_id) for movie_id in acc.index]
    #print(acc)

    recomendacoes = weighted_ratings[user_rated_movies == 0].sort_values(ascending=False)
    recomendacoes = recomendacoes.iloc[:-(int(len(recomendacoes) * 0.5))] #Remover a metade pior dos filmes simialres

    #Função auxiliar para conseguir o nome do filme
    def get_titulo(movie_id):
        title = imdb_merged.loc[imdb_merged['imdb_title_id'] == movie_id, 'title']
        return title.values[0]

    #Cria uma lista de pesos onde os filmes mais bem classificados têm maior chance de serem escolhidos, 
    # mas sem excluir completamente os outros
    recomendacoes = recomendacoes.sample(n=num_rec, weights=np.linspace(1, 0.1, len(recomendacoes)))
    
    recommended_movie_names = [get_titulo(movie_id) for movie_id in recomendacoes.index]
    return recommended_movie_names


# Testar as recomendações
utilizador = np.random.randint(1, 100)
num_rec = 5
print(f"Recomendações para o User '{utilizador}':", recomendar_UBC(utilizador, num_rec))



