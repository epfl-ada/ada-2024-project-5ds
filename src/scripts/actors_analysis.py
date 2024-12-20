import pandas as pd
import re
import plotly.express as px
import plotly.graph_objects as go

def data_cleaning(extended_films, winning_actors_info, imdb_ratings, new_film_dataset):
    """
    Data cleaning for the datasets used in the analysis.

    Parameters:
    - extended_films (pd.DataFrame): The extended films dataset.
    - winning_actors_info (pd.DataFrame): The winning actors information dataset.
    - imdb_ratings (pd.DataFrame): The IMDb ratings dataset.
    - new_film_dataset (pd.DataFrame): The new film dataset.

    Returns:
    - extended_films (pd.DataFrame): The cleaned extended films dataset.
    - winning_actors_info (pd.DataFrame): The cleaned winning actors information dataset.
    - imdb_ratings (pd.DataFrame): The cleaned IMDb ratings dataset.
    - new_film_dataset (pd.DataFrame): The cleaned new film dataset.


    """
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
    """
    Data preprocessing for the actors dataset.

    Parameters:
    - oscar_winning_actors (pd.DataFrame): The dataset containing Oscar-winning actors.
    - movie_cmu (pd.DataFrame): The CMU movie dataset.
    - extended_films (pd.DataFrame): The extended films dataset.
    - film_full (pd.DataFrame): The full film dataset.
    - winning_actors_info (pd.DataFrame): The winning actors information dataset.
    - character (pd.DataFrame): The character dataset.

    Returns:
    - revenue_by_year_corrected (pd.DataFrame): The total box office revenue by year.
    - oscar_act_info (pd.DataFrame): The dataset containing information about Oscar-winning actors.
    - oscar_act_movies (pd.DataFrame): The dataset containing movies of Oscar-winning actors.
    - oscar_act_movies_all (pd.DataFrame): The dataset containing all movies of Oscar-winning actors.

    
    """
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
    film_full['Movie genres'] = (
        film_full['Movie genres']
        .str.strip('[]')  # Remove square brackets
        .str.replace("'", '')  # Remove single quotes
        .str.replace('"', '')  # Remove double quotes
        .str.strip()  # Remove leading and trailing spaces
    )
    oscar_act_movies_all = oscar_act_movies_all.merge(film_full, on='Wikipedia movie ID', how='left')

    return revenue_by_year_corrected, oscar_act_info, oscar_act_movies, oscar_act_movies_all

def standardize_date_format(date):
    """
    """
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
    group["Movie release date"] = group["Movie release date"].apply(lambda x: x.split('-')[0] if isinstance(x, str) else x).astype(int)
    group = group.sort_values(by='Movie release date')
    # Find the first Oscar-winning movie and its date
    first_oscar = group.loc[group['Best Actor Reward']].nsmallest(1, 'Movie release date')
    first_oscar_date = first_oscar['Movie release date'].iloc[0] if not first_oscar.empty else None
    # Count movies before the first Oscar-winning movie
    if pd.notnull(first_oscar_date):
        movies_before = group[group['Movie release date'] < first_oscar_date].shape[0]
    else:
        movies_before = group.shape[0]  # If no Oscar win, count all movies
    
    return pd.Series({'Movies Before First Oscar': movies_before, 'First Oscar Date': first_oscar_date})


def evolution_imdb_scores(imdb_ratings, oscar_act_movies_all):
    imdb_ratings['Movie name'] = imdb_ratings['Movie name'].str.strip()
    filtered_ratings = imdb_ratings[['Movie name', 'Movie release date', 'imdb_score']]
    filtered_oscar_actors = oscar_act_movies_all[['Movie name', 'Movie release date', 'Actor name', 'Best Actor Reward']]
    filtered_oscar_actors['Movie release date'] = filtered_oscar_actors['Movie release date'].apply(lambda x: int(x.split('-')[0]) if isinstance(x, str) and pd.notna(x) else x)
    merged_data = pd.merge(filtered_ratings, filtered_oscar_actors, how='right', on=['Movie name', 'Movie release date'])


    # Extract relevant columns for analysis
    rating_evolution = merged_data[['Actor name', 'Movie name', 'Movie release date', 'imdb_score', 'Best Actor Reward']]

    # Convert release_year to numeric for proper sorting
    rating_evolution['Movie release date'] = pd.to_numeric(rating_evolution['Movie release date'], errors='coerce')


    # Filter data for movies released from 1980 onwards
    rating_evolution = rating_evolution[rating_evolution['Movie release date'] >= 1980]

    # Remove rows with missing or invalid IMDb score
    rating_evolution = rating_evolution.dropna(subset=['Movie release date', 'imdb_score'])

    # Sort data by actress name and release date
    rating_evolution = rating_evolution.sort_values(by=['Actor name', 'Movie release date'])

    return rating_evolution

def show_imdb_scores(rating_evolution):
    """
    Visualizes the evolution of IMDb scores for movies starring Oscar-winning actors/actresses.
    Parameters:
    rating_evolution (pd.DataFrame): A DataFrame containing the following columns:
        - 'Movie release date': The release year of the movie.
        - 'Actor name': The name of the actor/actress.
        - 'imdb_score': The IMDb score of the movie.
        - 'Best Actor Reward': Boolean indicating if the actor/actress won the Best Actor/Actress award.
        - 'Movie name': The name of the movie.
    The function generates an interactive Plotly scatter plot with the following features:
    - Different colors for different actors/actresses.
    - Conditional marker sizes and symbols based on whether the actor/actress won the Best Actor/Actress award.
    - Hover text displaying detailed information about each movie.
    - Dropdown menu to filter the plot by individual actors/actresses or show all.
    - Legend indicating the actors/actresses.
    Returns:
    None: The function displays the plot using Plotly's `fig.show()` method.
    """
    # Adjust x-axis range to start before the first movie release date
    rating_evolution['Movie release date'] = rating_evolution['Movie release date'].astype(int)
    x_range = [1975, 2020]  


    # Generate a color palette using Plotly's native discrete color scale
    actors_movies_count = rating_evolution['Actor name'].value_counts()
    relevant_actors = actors_movies_count[actors_movies_count >= 4].index
    relevant_actors = rating_evolution[rating_evolution['Actor name'].isin(relevant_actors)]
    unique_actors = relevant_actors[relevant_actors['Best Actor Reward'] == True]['Actor name'].unique()

    colors = px.colors.qualitative.Plotly  # Or use other palettes like `D3`, `Viridis`, etc.
    color_map = {actor: colors[i % len(colors)] for i, actor in enumerate(unique_actors)}

    # Create legend-only traces
    legend_traces = [
        go.Scatter(
            x=[None],  # No data points for this trace
            y=[None],  # No data points for this trace
            mode="markers",
            marker=dict(
                size=8,
                color=color_map[actor],
                symbol="circle"  # Always use a circle for the legend
            ),
            name=actor,  # Actress name in the legend
            showlegend=True,
            legendgroup=actor  # Group legend items for the same actor
        )
        for actor in unique_actors
    ]


    scatter_traces = [
        go.Scatter(
            x=rating_evolution[rating_evolution['Actor name'] == actor]['Movie release date'],
            y=rating_evolution[rating_evolution['Actor name'] == actor]['imdb_score'],
            mode='markers',
            marker=dict(
                size=[15 if reward else 8 for reward in rating_evolution[rating_evolution['Actor name'] == actor]['Best Actor Reward']],
                color=color_map[actor],
                symbol=[
                    'star' if reward else 'circle'  # Conditional marker symbol
                    for reward in rating_evolution[rating_evolution['Actor name'] == actor]['Best Actor Reward']
                ]
            ),
            name=actor,
            legendgroup=actor,  # Group scatter and line for the same actor
            showlegend=False,  # Show legend for scatter
            hovertext=[
                f"Name: {actress_i}<br>Movie: {movie}<br>IMDb Score: {score}<br>Release Date: {year}<br>Academy Award for Best Actor/Actress: {'Yes' if reward else 'No'}"
                for movie, score, year, reward, actress_i in zip(
                    rating_evolution[rating_evolution['Actor name'] == actor]['Movie name'],
                    rating_evolution[rating_evolution['Actor name'] == actor]['imdb_score'],
                    rating_evolution[rating_evolution['Actor name'] == actor]['Movie release date'],
                    rating_evolution[rating_evolution['Actor name'] == actor]['Best Actor Reward'],
                    rating_evolution[rating_evolution['Actor name'] == actor]['Actor name']
                )
            ],
            hoverinfo="text",  # Show only hover text
        )
        for actor in unique_actors
    ]

    line_traces = [
        go.Scatter(
            x=rating_evolution[rating_evolution['Actor name'] == actor]['Movie release date'],
            y=rating_evolution[rating_evolution['Actor name'] == actor]['imdb_score'],
            mode='lines+markers',  # Add both lines and markers
            line=dict(color=color_map[actor]),  # Use the same color as the scatter
            marker=dict(
                size=[15 if reward else 8 for reward in rating_evolution[rating_evolution['Actor name'] == actor]['Best Actor Reward']],
                symbol=[
                    'star' if reward else 'circle'  # Conditional marker symbol
                    for reward in rating_evolution[rating_evolution['Actor name'] == actor]['Best Actor Reward']
                ]
            ),
            name=actor,
            legendgroup=actor,
            visible=False,  # Start with lines hidden
            hovertext=[
                f"Movie: {movie}<br>IMDb Score: {score}<br>Release Date: {year}<br>Academy Award for Best Actor/Actress : {'Yes' if reward else 'No'}"
                for movie, score, year, reward in zip(
                    rating_evolution[rating_evolution['Actor name'] == actor]['Movie name'],
                    rating_evolution[rating_evolution['Actor name'] == actor]['imdb_score'],
                    rating_evolution[rating_evolution['Actor name'] == actor]['Movie release date'],
                    rating_evolution[rating_evolution['Actor name'] == actor]['Best Actor Reward']
                )
            ],
            hoverinfo="text"  # Show only hover text
        )
        for actor in unique_actors
    ]

    # Combine scatter and line traces
    traces = legend_traces + scatter_traces + line_traces

    # Create dropdown buttons
    buttons = [
        {
            "label": "All",
            "method": "update",
            "args": [
                {"visible": [True]*len(legend_traces) + [True] * len(scatter_traces) + [False] * len(line_traces)},  # Show scatter, hide all lines
                {"title": "Evolution of IMDb Scores for Movies Starring Oscar-Winning Actresses (All Actresses)"}
            ]
        }
    ]

    buttons += [
        {
            "label": actor,
            "method": "update",
            "args": [
                {"visible": [False]*len(legend_traces) + [False] * len(scatter_traces) + [actor == a for a in unique_actors]},
                {"title": f"Evolution of IMDb Scores for Movies Starring {actor}"}
            ]
        }
        for actor in unique_actors
    ]

    # Create layout
    layout = go.Layout(
        title="Evolution of IMDb Scores for Movies Starring Oscar-Winning Actresses/Actors Before and After the Reward(s)",
        xaxis=dict(title="Release Year", range=x_range),
        yaxis=dict(title="IMDb Score"),
        updatemenus=[
            {
                "buttons": buttons,
                "direction": "down",
                "showactive": True,
            }
        ],
        height=700,
        width=1200,
        showlegend=True  # Ensure legend is visible
    )

    # Create figure
    fig = go.Figure(data=traces, layout=layout)

    # Show figure
    fig.show()

def get_actor_genre_distribution(oscar_act_movies_all):
    # First, let's get the genres for each actor
    genre_by_actor = oscar_act_movies_all.groupby('Actor name')['Movie genres'].apply(lambda x: ','.join([str(g) for g in x if pd.notna(g)])).reset_index()

    # Split the genres string and explode to get one row per genre
    genre_by_actor['Movie genres'] = genre_by_actor['Movie genres'].str.split(',')
    genre_by_actor = genre_by_actor.explode('Movie genres')

    # Clean up genres by stripping whitespace and removing empty strings
    genre_by_actor['Movie genres'] = genre_by_actor['Movie genres'].str.strip()
    genre_by_actor = genre_by_actor[genre_by_actor['Movie genres'] != '']

    # Define genre mappings to group similar genres
    genre_mappings = {
        'Drama': ['Drama', 'Family Drama', 'Comedy-drama', 'Melodrama', 'Docudrama'],
        'Comedy': ['Comedy', 'Romantic comedy', 'Comedy-drama', 'Black comedy'],
        'Action/Adventure': ['Action', 'Adventure', 'Action/Adventure', 'Thriller', 'War film'],
        'Crime': ['Crime Fiction', 'Crime film', 'Detective fiction', 'Film noir'],
        'Historical': ['Period piece', 'Historical fiction', 'Biography', 'History'],
        'Romance': ['Romance Film', 'Romantic drama', 'Romantic comedy'],
        'Musical': ['Musical', 'Music film', 'Opera film', 'Concert film'],
        'Horror': ['Horror', 'Supernatural horror', 'Slasher', 'Psychological horror'],
        'Western': ['Western', 'Spaghetti Western', 'Contemporary Western'],
        'SciFi/Fantasy': ['Science Fiction', 'Fantasy', 'Superhero film', 'Space opera'],
        'Documentary': ['Documentary', 'Docudrama', 'Documentary drama'],
        'Animation': ['Animation', 'Anime', 'Stop motion', 'Computer animation'],
        'Other': [] # Will catch any genres not matched above
    }

    # Map genres to their groups
    def map_genre(genre):
        for group, genres in genre_mappings.items():
            if any(g.lower() in genre.lower() for g in genres):
                return group
        return 'Other'

    genre_by_actor['Movie genres'] = genre_by_actor['Movie genres'].apply(map_genre)

    # Count genres for each actor
    genre_counts = genre_by_actor.groupby(['Actor name', 'Movie genres']).size().reset_index(name='count')

    # Filter to only include genres that appear frequently
    min_appearances = 5
    frequent_genres = genre_counts.groupby('Movie genres')['count'].sum().reset_index()
    frequent_genres = frequent_genres[frequent_genres['count'] >= min_appearances]['Movie genres']
    genre_counts = genre_counts[genre_counts['Movie genres'].isin(frequent_genres)]

    return genre_counts


def bubble_graph(winning_actors_info, oscar_winning_actors, oscar_winning_actresses, film_full, character, imdb_ratings, oscar_winning_films):
    oscar_act = pd.concat([oscar_winning_actors, oscar_winning_actresses], axis=0)

    oscar_act_movies_new = pd.merge(oscar_act, film_full, left_on='film_id', right_on='Wikipedia movie ID')
    oscar_act_movies_new.drop(columns=['film_id'], inplace=True)

    oscar_actress_info_new = pd.merge(winning_actors_info, oscar_act_movies_new, left_on='page_id', right_on='Actress id')
    oscar_actors_info_new = pd.merge(winning_actors_info, oscar_act_movies_new, left_on='page_id', right_on='Actors id')
    oscar_act_info_new = pd.concat([oscar_actors_info_new, oscar_actress_info_new], axis=0)

    oscar_act_info_new = pd.merge(oscar_act_info_new, character[['Wikipedia movie ID', 'Actor name', 'Actor age at movie release', 'Actor date of birth', 'Actor ethnicity', 'Freebase actor ID']], on=['Wikipedia movie ID', 'Actor name'])
    oscar_act_info_new['Movie release date'] = oscar_act_info_new['Movie release date'].apply(standardize_date_format)

    oscar_act_new_movies_all = character[character['Freebase actor ID'].isin(oscar_act_info_new['Freebase actor ID'])]
    oscar_act_new_movies_all = oscar_act_new_movies_all.drop(columns=['Freebase movie ID', 'Movie release date'])
    oscar_act_new_movies_all = oscar_act_new_movies_all.merge(film_full, on='Wikipedia movie ID', how='left')
    oscar_act_new_movies_all['Movie release year'] = oscar_act_new_movies_all['Movie release date'].apply(standardize_date_format)

    # Create a set of unique (Actor name, Wikipedia movie ID) combinations for rewards
    best_act_movies = set(
        zip(oscar_act_info_new['Actor name'], oscar_act_info_new['Wikipedia movie ID'])
    )

    # Add a new column indicating if the movie is a Best Actress Reward
    oscar_act_new_movies_all['Best Actress Reward'] = oscar_act_new_movies_all.apply(
        lambda row: (row['Actor name'], row['Wikipedia movie ID']) in best_act_movies,
        axis=1
    )

    imdb_ratings['Movie name'] = imdb_ratings['Movie name'].str.strip()

    filtered_ratings = imdb_ratings[['Movie name', 'Movie release date', 'imdb_score']]
    filtered_oscar_act_new = oscar_act_info_new[['Movie name', 'Movie release date', 'Actor name', 'Movie box office revenue']]

    merged_data = pd.merge(filtered_ratings, filtered_oscar_act_new, on=['Movie name', 'Movie release date'])

    rating_box_office = merged_data[['Actor name', 'Movie name', 'Movie release date', 'imdb_score', 'Movie box office revenue']]
    rating_box_office['Movie release date'] = pd.to_numeric(rating_box_office['Movie release date'], errors='coerce')

    rating_box_office = rating_box_office[rating_box_office['Movie release date'] >= 1980]
    rating_box_office = rating_box_office.dropna(subset=['Movie box office revenue', 'imdb_score'])

    new_film_dataset_oscar = film_full[film_full['Wikipedia movie ID'].isin(oscar_winning_films['Page ID'])]
    new_film_dataset_oscar['Movie release date'] = pd.to_datetime(new_film_dataset_oscar['Movie release date'], errors='coerce').dt.year

    filtered_ratings = imdb_ratings[['Movie name', 'Movie release date', 'imdb_score']]
    filtered_oscar_act_new = new_film_dataset_oscar[['Movie name', 'Movie release date', 'Movie box office revenue', 'nbOscarNominated', 'nbOscarReceived']]

    merged_data = pd.merge(filtered_ratings, filtered_oscar_act_new, on=['Movie name', 'Movie release date'])

    rating_box_office = merged_data[['Movie name', 'Movie release date', 'imdb_score', 'Movie box office revenue', 'nbOscarNominated', 'nbOscarReceived']]

    rating_box_office = rating_box_office[rating_box_office['Movie release date'] >= 1980]
    rating_box_office = rating_box_office.dropna(subset=['Movie box office revenue', 'imdb_score'])

    # Filter out rows with missing or invalid data in critical columns
    rating_box_office = rating_box_office.dropna(subset=['Movie release date', 'imdb_score', 'Movie box office revenue', 'nbOscarNominated'])
    rating_box_office = rating_box_office[rating_box_office['Movie name'] != 'Titanic']
    # Ensure `nbOscarNominated` is numeric
    rating_box_office['nbOscarNominated'] = pd.to_numeric(
        rating_box_office['nbOscarNominated'], errors='coerce'
    )

    return rating_box_office
