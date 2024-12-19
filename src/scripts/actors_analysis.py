import pandas as pd
import re

def data_cleaning(extended_films, winning_actors_info, imdb_ratings, new_film_dataset):
    extended_films["Movie genres"] = extended_films["genres"]
    extended_films["Movie release date"] = extended_films["release_date"]
    extended_films["Movie languages"] = extended_films["languages"]
    extended_films["Movie countries"] = extended_films["countries"]
    extended_films["Movie name"] = extended_films["film"]
    extended_films["Movie box office revenue"] = extended_films["box_office"]
    extended_films["Movie runtime"] = extended_films["runtime"]
    extended_films["Wikipedia movie ID"] = extended_films["page_id"]
    extended_films = extended_films.drop(columns=["genres", "release_date", "languages", "countries", "release date", "film", "box_office", "runtime", "page_id"])

    winning_actors_info["Actor name"] = winning_actors_info["actor"]
    winning_actors_info = winning_actors_info.drop(columns=["actor"])

    imdb_ratings['Movie release date'] = imdb_ratings['title_year']  
    imdb_ratings['Movie name'] = imdb_ratings['movie_title'] 
    imdb_ratings = imdb_ratings.drop(columns=['title_year', 'movie_title'])

    new_film_dataset['Wikipedia movie ID'] = new_film_dataset['wikipedia_id']
    new_film_dataset['Movie name'] = new_film_dataset['title']
    new_film_dataset['Movie release date'] = new_film_dataset['release_date']
    new_film_dataset['Movie genres'] = new_film_dataset['categories']
    new_film_dataset['Movie box office revenue'] = new_film_dataset['box_office']

    new_film_dataset.drop(columns=['wikipedia_id', 'title', 'release_date', 'categories', 'box_office'], inplace=True)

    return extended_films, winning_actors_info, imdb_ratings, new_film_dataset

def deriving_actors_dataset_preprocessing(oscar_winning_actors, oscar_winning_actresses, movie_cmu, extended_films, film_full, winning_actors_info, character):
    
    oscar_act = pd.concat([oscar_winning_actors, oscar_winning_actresses], axis=0)
    oscar_act_movies_cmu  = pd.merge(oscar_act, movie_cmu, left_on='film_id', right_on='Wikipedia movie ID')
    oscar_act_movies_cmu.drop(columns=['film_id'], inplace=True) 
    oscar_act_movies_extendedDS  = pd.merge(oscar_act, extended_films, left_on='film_id', right_on='Wikipedia movie ID')
    oscar_act_movies_extendedDS.drop(columns=['film_id'], inplace=True)
    # Convert the 'Movie release date' column to datetime
    oscar_act_movies_extendedDS['Movie release date'] = pd.to_datetime(oscar_act_movies_extendedDS['Movie release date'])
    # Format the column to only show Year-Month-Day
    oscar_act_movies_extendedDS['Movie release date'] = oscar_act_movies_extendedDS['Movie release date'].dt.strftime('%Y-%m-%d')
    oscar_act_movies = pd.concat([oscar_act_movies_cmu, oscar_act_movies_extendedDS], axis=0)
    oscar_act_movies.drop(columns=['wikidata_id'], inplace=True)
    oscar_act_movies_new = pd.merge(oscar_act, film_full, left_on='film_id', right_on='Wikipedia movie ID')
    oscar_act_movies_new.drop(columns=['film_id'], inplace=True)
    oscar_actress_info_copy = pd.merge(winning_actors_info, oscar_act_movies_new, left_on='page_id', right_on='Actress id')
    oscar_actors_info_copy = pd.merge(winning_actors_info, oscar_act_movies_new, left_on='page_id', right_on='Actors id')
    oscar_act_info = pd.concat([oscar_actors_info_copy, oscar_actress_info_copy], axis=0)   
    oscar_act_info['Movie release year'] = oscar_act_info['Movie release date'].apply(standardize_date_format)
    oscar_act_info.drop(columns=['sexLabel'], inplace=True)  #Remove the columns that are in character.csv
    duplicates_with_different_ages = oscar_act_info.groupby('Actor name').filter(lambda x: x['page_id'].nunique() > 1)
    # Prepare data for box office revenue evolution
    oscar_revenue_data_corrected = oscar_act_info[['Movie box office revenue', 'Movie release year']].dropna()
    oscar_revenue_data_corrected = oscar_revenue_data_corrected.dropna(subset=['Movie release year'])

    # Group by year and calculate total box office revenue
    oscar_revenue_data_corrected['Year'] = oscar_revenue_data_corrected['Movie release year']
    revenue_by_year_corrected = oscar_revenue_data_corrected.groupby('Year')['Movie box office revenue'].sum().reset_index()
    oscar_act_info = pd.merge(oscar_act_info, character[['Wikipedia movie ID', 'Actor name', 'Actor age at movie release', 'Actor date of birth', 'Actor ethnicity','Character name', 'Freebase actor ID']], on=['Wikipedia movie ID', 'Actor name'])
    
    oscar_act_movies_all = character[character['Freebase actor ID'].isin(oscar_act_info['Freebase actor ID'])]
    oscar_act_movies_all = oscar_act_movies_all.drop(columns=['Freebase movie ID', 'Movie release date'])
    oscar_act_movies_all = oscar_act_movies_all.merge(movie_cmu, on='Wikipedia movie ID', how='left')

    return revenue_by_year_corrected, oscar_act_info, oscar_act_movies, oscar_act_movies_all

def standardize_date_format(date):
    if pd.isna(date):  # Handle NaN values explicitly
        return None  # Or return a default value, e.g., -1 or an empty string
    if isinstance(date, str):  # If it's a string (datetime-like), process it
        return pd.to_datetime(date).year  # Extract just the year from the datetime
    elif isinstance(date, float):  # If it's a float, treat it as a year
        return int(date)  # Convert float year to integer year
    return None  # Handle missing or invalid data

def get_genre_count(oscar_act_info, oscar_act_movies_all):
    # Create a set of unique (Actor name, Wikipedia movie ID) combinations for rewards
    best_act_movies = set(
        zip(oscar_act_info['Actor name'], oscar_act_info['Wikipedia movie ID'])
    )

    # Add a new column indicating if the movie is a Best Actor Reward
    oscar_act_movies_all['Best Actor Reward'] = oscar_act_movies_all.apply(
        lambda row: (row['Actor name'], row['Wikipedia movie ID']) in best_act_movies,
        axis=1
    )

    # Prepare the data for the bar chart
    oscar_movies_all = oscar_act_movies_all.copy()
    oscar_movies_all['Movie genres'] = oscar_movies_all['Movie genres'].fillna('Unknown')
    oscar_movies_all['Best Actor Reward'] = oscar_movies_all['Best Actor Reward'].map({True: 'Oscar-Winning', False: 'Non-Oscar-Winning'})

    # Split the genres into individual rows for analysis
    genres_split = oscar_movies_all.assign(Movie_genres_split=oscar_movies_all['Movie genres'].str.split(', ')).explode('Movie_genres_split')

    # Group and count movies by genre and whether they won an Oscar
    genre_counts = genres_split.groupby(['Movie_genres_split', 'Best Actor Reward']).size().reset_index(name='Count')

    # Limit to the top 15 genres with the highest total count
    top_genres = genre_counts.groupby('Movie_genres_split')['Count'].sum().nlargest(15).index
    filtered_genre_counts = genre_counts[genre_counts['Movie_genres_split'].isin(top_genres)]

    return filtered_genre_counts

def get_pie_genre_counts(oscar_movies_all):
    # Extract and clean the genres
    genres_data = oscar_movies_all[['Movie genres']].dropna()
    genres_data = genres_data.assign(Movie_genres_split=genres_data['Movie genres'].str.split(', ')).explode('Movie_genres_split')

    # Use regex to remove any empty strings, square brackets, and extra spaces
    genres_data['Movie_genres_split'] = genres_data['Movie_genres_split'].apply(lambda x: re.sub(r"[\[\]']", '', x).strip())

    # Count the occurrences of each genre
    genre_counts = genres_data['Movie_genres_split'].value_counts().reset_index()
    genre_counts.columns = ['Genre', 'Count']
    return genre_counts

def get_movies_and_first_oscar_date(group):
    # Sort movies by release date
    group["Movie release date"] = group["Movie release date"].apply(lambda x: x.split('-')[0] if isinstance(x, str) else x)
    group = group.sort_values(by='Movie release date')
    print(group)
    # Find the first Oscar-winning movie and its date
    first_oscar = group.loc[group['Best Actor Reward']].nsmallest(1, 'Movie release date')
    first_oscar_date = first_oscar['Movie release date'].iloc[0] if not first_oscar.empty else None
    # Count movies before the first Oscar-winning movie
    if pd.notnull(first_oscar_date):
        movies_before = group[group['Movie release date'] < first_oscar_date].shape[0]
    else:
        movies_before = group.shape[0]  # If no Oscar win, count all movies
    
    return pd.Series({'Movies Before First Oscar': movies_before, 'First Oscar Date': first_oscar_date})
