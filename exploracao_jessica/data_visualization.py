# Week 2: Data Exploration & Preprocessing

# -> Initial visualization of data using Matplotlib/Seaborn


#----- Importing libraries

import numpy as np # array-processing package
import pandas as pd # data analysis toolkit
import matplotlib.pyplot as plt # static, animated and interactive visualizations
import seaborn as sns # data visualization library
import pprint # data pretty printer


#----- Loading the datasets

# Note: the datasets were saved as CSV UTF-8 files; sep or delimiter
imdb_movies = pd.read_csv(r'C:/Users/Asus/Desktop/mestrado/projeto_integrado_matematica_computacao/Projeto-RecSys/exploracao_jessica/datasets/imdb_movies.csv', encoding = 'UTF-8', sep = ';') 
imdb_ratings = pd.read_csv(r'C:/Users/Asus/Desktop/mestrado/projeto_integrado_matematica_computacao/Projeto-RecSys/exploracao_jessica/datasets/imdb_ratings.csv', encoding = 'UTF-8', sep = ';')


#----- Merging the datasets

# Note: inner join returns matching values in both tables
imdb_merged = pd.merge(imdb_movies, imdb_ratings, how = "inner", on = "imdb_title_id")


#----- Dropping columns

size = len(imdb_merged)

# Note: inplace = True modifies the original DataFrame; 10 columns were dropped
for column in imdb_merged.columns:
    if imdb_merged[column].isnull().sum() > 0.5*size:
        imdb_merged.drop(columns = [column], inplace = True)


#----- Data visualization

# Path to save the figures
save_dir = r"C:/Users/Asus/Desktop/mestrado/projeto_integrado_matematica_computacao/Projeto-RecSys/exploracao_jessica/figures"

# Barplot with genres

# Note: the genres are separated by commas; .explode() splits the elements into new rows
genres_30 = imdb_merged['genre'].str.split(',').explode().str.strip().value_counts().head(30)
print(genres_30)

plt.figure(figsize = (10, 6))
barplot_genres = sns.barplot(x = genres_30.values, y = genres_30.index) 
plt.title('Count of Votes by Genres')
plt.xlabel('Count')
plt.ylabel('Genre')
# Note: bbox_inches='tight' removes unnecessary white spaces
plt.savefig(f"{save_dir}/barplot_genres.png", bbox_inches = 'tight')
#plt.show()


# Pie chart with countries

countries_10 = imdb_merged['country'].value_counts().head(10)
#print(countries_10)

# Note: equal ensures that pie chart is drawn as a circle;
# %1.1f displays a decimal number with 1 decimal place; %% displays the % symbol
plt.figure(figsize = (10, 6))
plt.pie(countries_10, labels = countries_10.index, autopct = '%1.1f%%')
plt.title('Count of Votes by Countries')
plt.axis('equal')  
plt.tight_layout()
plt.savefig(f"{save_dir}/piechart_coutries.png", bbox_inches = 'tight')
#plt.show() 


# Most popular movies

top_movies = imdb_merged.nlargest(10, 'total_votes')
#print(top_movies)

plt.figure(figsize = (13, 6))
sns.barplot(y = top_movies['title'], x = top_movies['total_votes'])
plt.title('Most Popular Movies by Votes')
plt.xlabel('Total Votes')
plt.ylabel('Movie Title')
plt.savefig(f"{save_dir}/barplot_topmovies.png", bbox_inches = 'tight')
plt.tight_layout()
#plt.show()


# Distribution of average votes

# Note: kde = True creates a smoothed curve over the histogram
plt.figure(figsize = (10, 6))
sns.histplot(imdb_merged['avg_vote'], bins = 20, kde = True)
plt.title('Distribution of Average Votes')
plt.xlabel('Average Votes')
plt.ylabel('Frequency')
plt.savefig(f"{save_dir}/hist_avgvotes.png", bbox_inches = 'tight')
#plt.show()


# Average votes by gender and age 

gender_age_ratings = pd.DataFrame({'Age Class': ['18-29', '30-44', '45+'],

                                    'Male': [imdb_merged['males_18age_avg_vote'].mean(),
                                             imdb_merged['males_30age_avg_vote'].mean(),
                                             imdb_merged['males_45age_avg_vote'].mean()],

                                     'Female': [imdb_merged['females_18age_avg_vote'].mean(),
                                                imdb_merged['females_30age_avg_vote'].mean(),
                                                imdb_merged['females_45age_avg_vote'].mean()]})

# Note: melt() unpivots the DataFrame from wide to long format
gender_age_ratings = gender_age_ratings.melt(id_vars = 'Age Class', var_name = 'Gender', value_name = 'Average Vote')
plt.figure(figsize = (10, 6))
sns.barplot(x = 'Age Class', y = 'Average Vote', hue = 'Gender', data = gender_age_ratings, palette = 'coolwarm')

plt.title('Mean Average Vote by Gender and Age')
plt.xlabel('Age Class')
plt.ylabel('Mean Average Vote')
plt.ylim(0, 8)
plt.legend(title = 'Gender')
plt.savefig(f"{save_dir}/barplot_genderage.png", bbox_inches = 'tight')
plt.show()




