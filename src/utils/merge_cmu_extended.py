import ast
from clean_cmu import clean_movies_cmu
import pandas as pd


def merge_cmu_extended(movie, extended_films) : 

    movie = clean_movies_cmu(movie)
    movie.rename(columns={'Wikipedia movie ID': 'page_id', 'Movie name': 'film', 'Movie genres' : 'genres', 'Movie languages' : 'languages', 'Movie box office revenue' : 'box_office', 'Movie runtime' : 'runtime', 'Movie countries' : 'countries'}, inplace=True)
    movie['genres'] = movie['genres'].apply(lambda s : s.split(','))


    extended_films['runtime'] = pd.to_numeric(extended_films['runtime'],  errors='coerce')
    extended_films['genres'] = extended_films['genres'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else '[]')


  
    

    extended_films['genres'] = extended_films['genres'].map(
    lambda genre_list: set(genre_list)
    )
    movie['genres'] = movie['genres'].map(
        lambda genre_list: set(genre_list)
    )
    all_films = pd.concat([movie, extended_films])

    return all_films