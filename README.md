# Movie Recommendation System
**University Project (Universidade do Minho)**

## 🎯 Overview
This project explores and compares multiple **Recommendation System** techniques for movie suggestions using Python. The system uses artificial user profiles and real metadata from the IMDb movie database to test and evaluate different approaches:

- **Collaborative Filtering (User-Based, Item-Based, Matrix Factorization)**
- **Content-Based Filtering**
- **Hybrid Systems**
- **Semantic Approaches using Sentence Transformers**

> The project was developed in collaboration with Accenture and supervised by professors and industry mentors.

---

## 📁 Datasets
- `imdb_movies.csv`: Movie metadata (titles, genres, actors, directors, etc.)
- `imdb_ratings.csv`: Ratings statistics (votes, demographic breakdown, averages)

> Over 80,000 movies used after cleaning and preprocessing.

---

## 🧠 Implemented Approaches

### 🔷 Collaborative Filtering
- **User-Based**: Recommends items based on similar users' preferences.
- **Item-Based**: Suggests similar items using cosine/Pearson similarity.
- **Matrix Factorization (SVD)**: Decomposes the user-item matrix to reveal latent factors.

### 🔶 Content-Based Filtering
- Uses **TF-IDF** and metadata such as genres, description, director, and actors.
- Recommends similar movies based on content similarity (cosine distance).

### 🔄 Hybrid System
- Combines collaborative and content-based features.
- Solves **cold start problems** for new users/items.

### 🧠 Sentence Transformers
- Uses `all-mpnet-base-v2` for semantic similarity between movies.
- Captures deep meaning beyond simple keyword matching.

---

## 🔎 Evaluation Metrics

| Model / Approach             | Precision@10 | Recall@10 | F1-score@10 |
|-----------------------------|--------------|-----------|-------------|
| TF-IDF                      | 70%          | 100%      | 82.35%      |
| Sentence Transformer        | Higher semantic relevance, less lexical bias |
| Matrix Factorization (SVD)  | Best RMSE, moderate MAE                    |
| Item-Based Filtering (Cosine + k=5) | Best overall balance for sparse data |

> RMSE and MAE used for numeric rating prediction models.

---

## ⚙️ Setup & Usage

### ✅ Installation

```bash
pip install -r requirements.txt
```

Or manually install key libraries:

```bash
pip install pandas numpy scikit-learn matplotlib seaborn flask sentence-transformers
```

### 🚀 Running the System

Example commands:

```bash
# Content-based TF-IDF
python content_filtering.py

# Collaborative Filtering
python collaborative_user.py
python collaborative_item.py

# Matrix Factorization
python svd_recommendation.py

# Semantic Recommendations
python semantic_transformer.py
```

---

## 🌐 Web App (Flask)
A **Flask-based web app** allows users to:
- Input a movie title for similar suggestions
- Select genres, actors, and directors for custom recommendations

> Hosted via Google Colab using `ngrok` and enriched with TMDb API for movie posters.

---

## 🧪 Optimization
- Multiple metrics tested: Cosine, Pearson, Euclidean, Manhattan, Linear Kernel
- Parameter tuning: latent dimensions (`k`), neighbor counts, batch handling for scalability

---

## 🧰 Technologies Used
- Python, Pandas, NumPy
- Scikit-learn, Sentence Transformers, Flask
- Google Colab, TMDb API, ngrok