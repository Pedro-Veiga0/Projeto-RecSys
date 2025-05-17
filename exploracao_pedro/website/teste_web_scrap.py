from flask import Flask, render_template, jsonify, request, Response
import numpy as np
import pandas as pd

app = Flask(__name__)

def load_data():
    data = pd.read_csv(r'movies.csv', delimiter=';')
    data.dropna(subset=['original_title','description','genre'],inplace=True,axis=0)
    data = data.reset_index(drop=True)

    data["combined"] = data['genre'] + ' ' + data['original_title'] + ' ' + data['description']

    data.drop(['description','genre'],axis=1,inplace=True)
    return data

def content_recommender(title):
    movie_title = data['original_title']
    indices = pd.Series(data.index, index=data['original_title'])

    idx = indices[title]
    sim_scores = list(enumerate(cosine_similarities[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return movie_title.iloc[movie_indices]

@app.route('/')
def index():
    recommendations = []

    movie_name = request.form['movie']

    recommendations = content_recommender(movie_name)
    return render_template('index.html', recommendations=recommendations, movie_name=movie_name)

if __name__ == '__main__':
    app.run(debug=True)