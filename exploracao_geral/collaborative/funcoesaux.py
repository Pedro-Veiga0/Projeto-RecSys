import numpy as np
import pandas as pd

def fallback_recomendacoes(user_id, dataset, ratings_df, train_movie_matrix, popular_movies):
    """
    Gera recomendações fallback com base em géneros preferidos e popularidade.
    """
    #Filmes já vistos
    vistos = train_movie_matrix.loc[user_id]
    filmes_vistos = set(vistos[vistos > 0].index)

    #Géneros preferidos
    generos = genero_preferido(user_id, ratings_df, dataset)

    #Filmes do género preferido que o user ainda não viu
    dataset_genero = dataset.copy()
    dataset_genero['genre'] = dataset_genero['genre'].fillna('').str.split(',')
    dataset_genero = dataset_genero.explode('genre')
    dataset_genero['genre'] = dataset_genero['genre'].str.strip()

    candidatos_genero = dataset_genero[
        dataset_genero['genre'].isin(generos)
    ].drop_duplicates(subset='imdb_title_id')

    candidatos_genero = candidatos_genero[
        ~candidatos_genero['imdb_title_id'].isin(filmes_vistos)
    ]

    num_generos = np.random.randint(4, 8)
    num_populares = 10 - num_generos
    filmes_genero = candidatos_genero['imdb_title_id'].sample(
        min(num_generos, len(candidatos_genero)), random_state=4465
    ).tolist()

    #Filmes populares ou recentes ainda não vistos
    candidatos_extras = [f for f in popular_movies if f not in filmes_vistos]
    filmes_extras = candidatos_extras[:num_populares]

    return filmes_genero + filmes_extras

'''
------------------------------------------------------------------------------------------------------------------------------------
'''
def rerank_diversidade_novidade(recs, dataset):
    """
    Devolve das recomendações com base em novidade e diversidade.
    """
    df = dataset[dataset['imdb_title_id'].isin(recs)].copy()
    df['year'] = pd.to_numeric(df['year'], errors='coerce')
    df['votes'] = pd.to_numeric(df.get('votes', 0), errors='coerce')

    #Score novidade: quanto mais recente, maior o score
    ano_max = df['year'].max()
    ano_min = df['year'].min()
    df['score_novidade'] = (df['year'] - ano_min) / (ano_max - ano_min + 1e-9)

    #Score popularidade invertida: quanto menos votos, maior o score
    vot_max = df['votes'].max()
    df['score_popularidade'] = 1 - (df['votes'] / (vot_max + 1e-9))

    #Combinação dos dois scores
    df['score_rerank'] = 0.6 * df['score_novidade'] + 0.4 * df['score_popularidade']

    return df.sort_values('score_rerank', ascending=False)['imdb_title_id'].tolist()

'''
------------------------------------------------------------------------------------------------------------------------------------
'''

def get_titulo(movie_id, dataset):
    """
    Devolve o título original do filme dado o ID.
    """
    title = dataset.loc[dataset['imdb_title_id'] == movie_id, 'original_title']
    return title.values[0] if not title.empty else None

'''
------------------------------------------------------------------------------------------------------------------------------------
'''

def genero_preferido(user_id, ratings_df, dataset):
    """
    Devolve os géneros preferidos do utilizador com base nas suas avaliações.
    """
    filmes_user = ratings_df[ratings_df[' User ID '] == user_id]
    filmes_user = filmes_user.merge(dataset[['imdb_title_id', 'genre']], left_on=' Movie ID ', right_on='imdb_title_id')

    filmes_user['genre'] = filmes_user['genre'].str.split(',')
    filmes_user = filmes_user.explode('genre')
    filmes_user['genre'] = filmes_user['genre'].str.strip()

    media_por_genero = filmes_user.groupby('genre')[' User Rating '].mean().sort_values(ascending=False)
    top_generos = media_por_genero.index[:2].tolist()

    return top_generos

'''
------------------------------------------------------------------------------------------------------------------------------------
'''

def criar_users_ratings(dataset, num_users=100, num_filmesfixos=1250, num_filmestotais=2500, output_csv="user_ratings.csv"):
    """
    Cria um conjunto de utilizadores fictícios e gera ratings para os filmes,
    guardando os dados num ficheiro CSV.

    Parâmetros:
    - dataset: DataFrame com os filmes (deve conter 'imdb_title_id' e 'avg_vote')
    - num_users: Número de utilizadores fictícios a criar
    - num_filmesfixos: Número de filmes comuns a todos os utilizadores
    - num_filmestotais: Total de filmes avaliados por utilizador
    - output_csv: Nome do ficheiro CSV de saída
    """
    users = list(range(1, num_users + 1))
    user_ratings = []

    # Filmes fixos (avaliados por todos os utilizadores)
    filmes_fixos = np.random.choice(dataset['imdb_title_id'], size=num_filmesfixos, replace=False)

    for user in users:
        filmes_avaliados = list(filmes_fixos)

        # Filmes restantes únicos para cada utilizador
        filmes_restantes = np.random.choice(
            dataset[~dataset['imdb_title_id'].isin(filmes_fixos)]['imdb_title_id'],
            size=num_filmestotais - num_filmesfixos,
            replace=False
        )

        filmes_avaliados.extend(filmes_restantes)

        for movie_id in filmes_avaliados:
            avg_vote = dataset.loc[dataset['imdb_title_id'] == movie_id, 'avg_vote'].values[0]
            rating = np.clip(np.random.normal(avg_vote, 3), 1, 10)
            user_ratings.append({
                ' User ID ': user,
                ' Movie ID ': movie_id,
                ' User Rating ': round(rating, 1)
            })

    ratings_df = pd.DataFrame(user_ratings)
    ratings_df.to_csv(output_csv, index=False)

    return ratings_df

'''
------------------------------------------------------------------------------------------------------------------------------------
'''
