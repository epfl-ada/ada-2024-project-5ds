import pandas as pd
import numpy as np
import plotly.express as px
from IPython.display import display
import datetime as dt

from genres import categorize_genres

def create_full_film() : 
    df_film_wiki = pd.read_csv('film_2015_2024.csv')
    df_film_cmu = pd.read_csv('movie_cmu.csv')

    display(df_film_wiki.head(1))
    display(df_film_cmu.head(1))
    df_film_cmu = df_film_cmu.rename(columns={'Wikipedia movie ID':'wikipedia_id', 'Freebase movie ID': 'dataset_id',
                                               'Movie name': 'title', 'Movie release date': 'release_date', 'Movie box office revenue': 'box_office',
                                                 'Movie runtime': 'runtime', 'Movie languages': 'languages', 'Movie countries': 'countries', 'Movie genres': 'genres'})
    df_film_wiki = df_film_wiki.rename(columns={'page_id':'wikipedia_id', 'wikidata_id': 'dataset_id', 'film': 'title'})
    def parse_date_wiki(date):
        try:
            if date == 'NaN':
                return np.nan
            return dt.datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ").date()
        except:
            return np.nan
        
    df_film_wiki['release_date'] = df_film_wiki['release_date'].apply(parse_date_wiki)
    def parse_date_cmu(date):
        try:
            if date.isdigit():
                return dt.datetime.strptime(date, "%Y").date()
            elif date.count('-') == 1:
                return dt.datetime.strptime(date, "%Y-%m").date()
            elif date.count('-') == 2:
                return dt.datetime.strptime(date, "%Y-%m-%d").date()
            else:
                return np.nan
        except:
            return np.nan
    
    df_film_cmu['release_date'] = df_film_cmu['release_date'].apply(parse_date_cmu)

    def parse_runtime(x):
        try: 
            if x == 'NaN':
                return np.nan
            return int(x)
        except:
            return np.nan


    df_film_cmu['runtime'] = df_film_cmu['runtime'].apply(parse_runtime)
    df_film_wiki['runtime'] = df_film_wiki['runtime'].apply(parse_runtime)
    def parse_language_wiki(languages):
        try:
            languages = languages.split(',')
            languages = [language.strip() for language in languages]
            return languages
        except:
            return np.nan
    
    df_film_wiki['languages'] = df_film_wiki['languages'].apply(parse_language_wiki)

    from operator import contains


    def parse_language_cmu(languages):
        try:
            languages = languages.replace('{','').replace('}','').replace('"','')
            languages = languages.split(',')
            languages = [language.split(':') for language in languages]
            languages = [language[1].strip() for language in languages]
            languages = [language.split(' ')[0] if contains(language.lower(), 'language')  else language for language in languages]
            return languages
        except:
            return np.nan
        
    df_film_cmu['languages'] = df_film_cmu['languages'].apply(parse_language_cmu)

    def parse_country_wiki(countries):
        try:
            countries = countries.split(',')
            countries = [country.strip() for country in countries]
            return countries
        except:
            return np.nan
        
    df_film_wiki['countries'] = df_film_wiki['countries'].apply(parse_country_wiki)

    def parse_country_cmu(countries):
        try:
            countries = countries.replace('{','').replace('}','').replace('"','')
            countries = countries.split(',')
            countries = [country.split(':') for country in countries]
            countries = [country[1].strip() for country in countries]
            return countries
        except:
            return np.nan
        
    df_film_cmu['countries'] = df_film_cmu['countries'].apply(parse_country_cmu)

    def parse_genre_wiki(genres):
        try:
            genres = genres.replace('[','').replace(']','').replace("'",'').replace('"','')
            genres = genres.split(',')
            genres = [genre.strip() for genre in genres]
            return genres
        except:
            return None
        
    df_film_wiki['genres'] = df_film_wiki['genres'].apply(parse_genre_wiki)
    def parse_genre_cmu(genres):
        try:
            genres = genres.replace('{','').replace('}','').replace('"','')
            genres = genres.split(',')
            genres = [genre.split(':') for genre in genres]
            genres = [genre[1].strip() for genre in genres]
            return genres
        except:
            return None
        
    df_film_cmu['genres'] = df_film_cmu['genres'].apply(parse_genre_cmu)

    df_film_cmu
    df_film_cmu['categories'] = df_film_cmu['genres'].apply(categorize_genres)
    df_film_wiki['categories'] = df_film_wiki['genres'].apply(categorize_genres)

    def get_numerical_review(review):
        if contains(review, '%'):
            return int(review.replace('%',''))/100
        elif contains(review, '/'):
            return float(review.split('/')[0])/float(review.split('/')[1])
        else:
            return np.nan

    def parse_review(reviews):
        try:
            reviews = reviews.replace('[','').replace(']','').replace("'",'')
            reviews = reviews.split(',')
            reviews = [get_numerical_review(review.strip()) for review in reviews]
            return np.mean(reviews)
        except:
            return np.nan
        
    df_film_wiki['reviewScores'] = df_film_wiki['reviewScores'].apply(parse_review)

    def parse_awards(awards):
        try:
            awards = awards.replace('[','').replace(']','').replace("'",'')
            awards = awards.split(',')
            awards = [award.strip() for award in awards]
            return awards
        except:
            return []
        
    df_film_wiki['awardsNominated'] = df_film_wiki['awardsNominated'].apply(parse_awards)
    df_film_wiki['awardsReceived'] = df_film_wiki['awardsReceived'].apply(parse_awards)

    df_film_cmu['languages'] = df_film_cmu['languages'].apply(lambda x: ','.join(x) if isinstance(x, list) else x)
    df_film_cmu['countries'] = df_film_cmu['countries'].apply(lambda x: ','.join(x) if isinstance(x, list) else x)
    df_film_cmu['genres'] = df_film_cmu['genres'].apply(lambda x: ','.join(x) if isinstance(x, list) else x)
    df_film_cmu['categories'] = df_film_cmu['categories'].apply(lambda x: ','.join(x) if isinstance(x, list) else x)

    df_film_wiki['languages'] = df_film_wiki['languages'].apply(lambda x: ','.join(x) if isinstance(x, list) else x)
    df_film_wiki['countries'] = df_film_wiki['countries'].apply(lambda x: ','.join(x) if isinstance(x, list) else x)
    df_film_wiki['genres'] = df_film_wiki['genres'].apply(lambda x: ','.join(x) if isinstance(x, list) else x)
    df_film_wiki['categories'] = df_film_wiki['categories'].apply(lambda x: ','.join(x) if isinstance(x, list) else x)
    df_film_wiki['awardsNominated'] = df_film_wiki['awardsNominated'].apply(lambda x: ','.join(x) if isinstance(x, list) else x)
    df_film_wiki['awardsReceived'] = df_film_wiki['awardsReceived'].apply(lambda x: ','.join(x) if isinstance(x, list) else x)


    df_full = pd.merge(df_film_wiki, df_film_cmu, on=['wikipedia_id', 'dataset_id', 'title', 'release_date', 'box_office', 'runtime', 'languages', 'countries', 'genres', 'categories'], how='outer')


    df_full['languages'] = df_full['languages'].apply(lambda x: x.split(',') if isinstance(x, str) else x)
    df_full['countries'] = df_full['countries'].apply(lambda x: x.split(',') if isinstance(x, str) else x)
    df_full['genres'] = df_full['genres'].apply(lambda x: x.split(',') if isinstance(x, str) else x)
    df_full['categories'] = df_full['categories'].apply(lambda x: x.split(',') if isinstance(x, str) else x)
    df_full['awardsNominated'] = df_full['awardsNominated'].apply(lambda x: x.split(',') if isinstance(x, str) else [])
    df_full['awardsReceived'] = df_full['awardsReceived'].apply(lambda x: x.split(',') if isinstance(x, str) else [])



    df_full.to_csv('film_full.csv', index=False)

