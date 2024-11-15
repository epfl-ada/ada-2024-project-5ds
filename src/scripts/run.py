import pandas as pd
import numpy as np
import ast

import sys
sys.path.append('D:/UNIV/MASTER-EPFL/ADA/applied-project/ada-2024-project-5ds/src/utils')
sys.path.append('D:/UNIV/MASTER-EPFL/ADA/applied-project/ada-2024-project-5ds/src/data')
from data_utils import save_dataframe_to_csv, load_dataframe_from_csv
from dataloader import load_initial_dataset

# Load the dataset
path = 'data/'
array_csv_files = ["films_2015.csv", "films_2016.csv", "films_2017.csv", "films_2018.csv", "films_2019.csv", "films_2020.csv", "films_2022.csv", "films_2023.csv", "films_2024.csv"]

def rename_columns(df):
    """
    Rename the columns of a DataFrame
    
    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to rename the columns of 
        
    Returns
    -------
    pd.DataFrame"""
    if 'Unnamed: 0' in df.index:
        return df.T.rename(columns=lambda x: df.loc['Unnamed: 0', x]).drop('Unnamed: 0')
    return df

def read_and_process_csv(file_path):
    """
    Read a CSV file and transpose it

    Parameters
    ----------
    file_path : str
        The path to the CSV file

    Returns
    -------
    pd.DataFrame
        The transposed DataFrame
    """
    df = pd.read_csv(file_path, index_col=0).transpose()
    return rename_columns(df)

def merged_csv(array_csv_files): 
    """
    Merge all the CSV files into a single CSV file

    Parameters
    ----------
    array_csv_files : list
        The list of CSV files to merge

    Returns
    -------
    pd.DataFrame
        The merged DataFrame saved in a CSV file in data
    
    """
    # Transpose the CSV files from 2015 to 2017
    transposed_dfs = [read_and_process_csv(path + f) for f in array_csv_files[:3]] + [pd.read_csv(path + f) for f in array_csv_files[3:6]]+ [read_and_process_csv(path + f) for f in array_csv_files[6:]]

    # Read the remaining CSV files without transposing
    all_dfs_merged = pd.concat(f for f in transposed_dfs)
    # Display the updated dataframe
    all_dfs_merged = all_dfs_merged.drop(columns= "Unnamed: 0")
    all_dfs_merged.to_csv('data/film_2015_2024.csv', index=False)


def extract_country(country_dict_str):
    """
    Extract the country names from a dictionary string

    Parameters
    ----------
    country_dict_str : str
        The dictionary string containing the country names
    
    Returns
    -------
    list
        The list of country names
    """

    try:
        # Safely evaluate the string as a dictionary
        country_dict = ast.literal_eval(country_dict_str)
        # Return the list of country names
        return list(country_dict.values())[0]
    except (ValueError, SyntaxError, IndexError):
        return country_dict_str
    
def extract_genre_names(genre_dict_str):
    """
    Extract the genre names from a dictionary string

    Parameters
    ----------
    genre_dict_str : str
        The dictionary string containing the genre names

    Returns
    -------
    str 
        The list of genre names

    """
    try:
        # Safely evaluate the string as a dictionary
        genre_dict = ast.literal_eval(genre_dict_str)
        # Return the list of genre names
        return ', '.join(genre_dict.values())
    except (ValueError, SyntaxError):
        return genre_dict_str

def extract_language(language_dict_str):
    """
    Extract the language name from a dictionary string

    Parameters
    ----------
    language_dict_str : str
        The dictionary string containing the language name
    
    Returns
    -------
    str
        The language name
    """
    try:
        # Safely evaluate the string as a dictionary
        language_dict = ast.literal_eval(language_dict_str)
        # Return the language name
        return list(language_dict.values())[0]
    except (ValueError, SyntaxError, IndexError):
        return language_dict_str

def clean_cmu_dataset(movie_df, character_df, extended_films_df ):
    """
    Cleans the cmu dataset

    Parameters
    ----------
    cmu_df : pd.DataFrame
        The DataFrame to clean

    Returns
    -------
    pd.DataFrame
        The cleaned DataFrame
    """


    #CLeaning the country, genre and language features
    movie_df['Movie countries'] = movie_df['Movie countries'].apply(extract_country)
    movie_df['Movie genres'] = movie_df['Movie genres'].apply(extract_genre_names)
    movie_df['Movie languages'] = movie_df['Movie languages'].apply(extract_language)

    #Cleaning the character date of birth and movie release date to only keep the year
    movie_df['Movie release date'] = pd.to_datetime(movie_df['Movie release date'], errors='coerce').dt.year
    character_df['Movie release date'] = pd.to_datetime(character_df['Movie release date'], errors='coerce').dt.year
    character_df['Actor date of birth'] = pd.to_datetime(character_df['Actor date of birth'], errors='coerce').dt.year
    extended_films_df["release date"] = extended_films_df['release_date'].apply(lambda x: x[:4] if pd.notna(x) else x)

    for col in movie_df.columns:
        if movie_df[col].dtype==object:
            movie_df[col] = movie_df[col].apply(lambda x: np.nan if x==np.nan else str(x).encode('utf-8', 'replace').decode('utf-8'))

    for col in character_df.columns:
        if character_df[col].dtype==object:
            character_df[col] = character_df[col].apply(lambda x: np.nan if x==np.nan else str(x).encode('utf-8', 'replace').decode('utf-8'))

    for col in extended_films_df.columns:
        if extended_films_df[col].dtype==object:
            extended_films_df[col] = extended_films_df[col].apply(lambda x: np.nan if x==np.nan else str(x).encode('utf-8', 'replace').decode('utf-8'))

    save_dataframe_to_csv(movie_df, 'movie_cmu.csv')
    save_dataframe_to_csv(character_df, 'character.csv')
    save_dataframe_to_csv(extended_films_df, 'film_2015_2024.csv')
    
merged_csv(array_csv_files)

# Load the dataset
movie, character = load_dataframe_from_csv('movie_cmu.csv'), load_dataframe_from_csv('character.csv')
film_2015_2024 = load_dataframe_from_csv('film_2015_2024.csv')
clean_cmu_dataset(movie, character, film_2015_2024)