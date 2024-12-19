import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import ttest_ind
import pycountry
import pycountry_convert as pc


# Function to extract only the digits outside parentheses
def extract_digits(value):
    if isinstance(value, str): 
        match = re.match(r'^\d+', value) 
        return int(match.group()) if match else None
    return value 

def clean_film_full(film_full):
    """"
    Clean the film_full dataframe by removing the columns that are not useful for the analysis
    Input:
    film_full: pandas DataFrame containing the full dataset
    Output:
    film_full: cleaned DataFrame
    """
    film_full.loc[film_full['nbOscarNominated'].isna(), 'nbOscarNominated'] = 0
    film_full.loc[film_full['nbOscarReceived'].isna(), 'nbOscarReceived'] = 0


    #clean the columns before handling nan and transforming to integers
    film_full['nbOscarReceived'] = film_full['nbOscarReceived'].apply(extract_digits)
    film_full['nbOscarNominated'] = film_full['nbOscarNominated'].apply(extract_digits)



    film_full['nbOscarNominated'] = pd.to_numeric(film_full['nbOscarNominated'], errors='coerce').astype('Int64')
    film_full['nbOscarReceived'] = pd.to_numeric(film_full['nbOscarReceived'], errors='coerce').astype('Int64')

    film_full.loc[film_full['nbOscarNominated'].isna(), 'nbOscarNominated'] = 0
    film_full.loc[film_full['nbOscarReceived'].isna(), 'nbOscarReceived'] = 0

    #A film had an oscar if it received at least one 
    film_full['oscar'] = film_full['nbOscarReceived'] > 0 

    #add the title length as a column
    film_full['title_length'] = film_full['title'].apply(lambda s : len(s))

    #drop not significant movies
    film_full = film_full.dropna(thresh=film_full.shape[1] - 8)

    return film_full

# Function to create heatmap
def create_heatmap(corr_matrix, title):
    continuous_cols = ['box_office', 'runtime', 'reviewScores', 'capitalCost', 'nbOscarReceived', 'nbOscarNominated']

    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=continuous_cols,
        y=continuous_cols,
        colorscale='RdBu',
        zmin=-1,
        zmax=1,
        colorbar=dict(title="Correlation Coefficient")
    ))

    # Add annotations
    for i in range(len(corr_matrix)):
        for j in range(len(corr_matrix)):
            fig.add_annotation(
                x=continuous_cols[j],
                y=continuous_cols[i],
                text=f"{corr_matrix.values[i][j]:.2f}",
                showarrow=False,
                font=dict(color='black' if abs(corr_matrix.values[i][j]) < 0.5 else 'white')
            )

    fig.update_layout(
        title=title,
        xaxis_title="Variables",
        yaxis_title="Variables",
        yaxis=dict(autorange='reversed'),
        width=600,
        height=600
    )

    fig.show()


def create_pvalue_table(pvalues_df, title):
    fig = go.Figure(data=[go.Table(
        header=dict(values=["Variable", "P-Value"],
                    fill_color='lightgray',
                    align='center',
                    font=dict(size=14, color='black')),
        cells=dict(values=[pvalues_df.index, pvalues_df['p-value']],
                   align='center',
                   font=dict(size=12, color='black')))
    ])

    fig.update_layout(
        title=title,
        width=500,
        height=400
    )
    fig.show()

def compute_pvalues(group1, group2, columns):
    p_values = {}
    for col in columns:
        stat, p_val = ttest_ind(group1[col], group2[col], alternative='two-sided')
        p_values[col] = p_val
    return p_values

def country_to_continent(country_name):
    country_alpha2 = pc.country_name_to_country_alpha2(country_name)
    country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
    country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
    return country_continent_name

def compute_countries_count(film_full):
    #Remove Na values in the countries column
    countries = film_full.dropna(subset=['countries'])
    #Handle the formatting of the columns
    countries['countries'] = countries['countries'].str.strip('[]')
    countries['countries'] = countries['countries'].map(lambda s : s.split(','))

    #Explode the list of all countries for each film in order to count the number of time one country appear 
    countries = countries.explode(column='countries')
    countries['countries'] = countries['countries'].map(lambda s : s.strip())

    #Plotly doesn't recognize hong kong as hong kong but as china
    countries['countries'] = countries['countries'].map(lambda s : 'China' if s in ['Hong Kong'] else s)
    count = countries.groupby('countries').agg({'nbOscarReceived' : 'sum'}).reset_index()

    #List of iso alpha not recognised
    iso_alpha_not_recognised = {'Hong Kong' : 'HKG', 'Italy' : 'ITA', 'India' : 'IND', 'Germany' : 'DEU', 'New Zealand' : 'NZL', 'Belgium' : 'BEL', 'Canada' : 'CAN'}

    # Function to convert country names to ISO Alpha-3 codes
    def get_iso_alpha(country_name):
        try:
            if country_name in iso_alpha_not_recognised.keys() : 
                return iso_alpha_not_recognised[country_name]
            else :
                return pycountry.countries.lookup(country_name).alpha_3
        except LookupError:
            return np.nan

    # Apply the function to convert to iso alpha
    count['iso_alpha'] = count['countries'].apply(get_iso_alpha)
    count.dropna(inplace=True)

    count['continent'] = count['iso_alpha'].dropna().map(lambda s : country_to_continent(s))

    count = count.groupby(['iso_alpha'], as_index=False).agg({'nbOscarReceived': 'max','countries': 'first',  'continent': 'first'})
    return count

def analyze_genres(film_full):
    # Drop rows with NaN in the 'categories' column
    genres_analyzed = film_full.dropna(subset=['categories'])

    # Clean the 'categories' column
    genres_analyzed['categories'] = (
        genres_analyzed['categories']
        .str.strip('[]')  # Remove square brackets
        .str.replace("'", '')  # Remove single quotes
        .str.replace('"', '')  # Remove double quotes
        .str.strip()  # Remove leading and trailing spaces
    )

    genres_analyzed['categories'] = genres_analyzed['categories'].apply(
        lambda s: [x.strip() for x in s.split(',')] if isinstance(s, str) else []
    )


    genres_analyzed['categories'] = genres_analyzed['categories'].apply(
        lambda s: list(set(filter(None, s)))  # Remove empty strings 
    )


    genres_analyzed['categories'] = genres_analyzed['categories'].apply(
        lambda s: [x.lower().capitalize() for x in s]  
    )

    #Explode the list of all genres  for each film in order to count the number of time one genre appear 
    genres_analyzed = genres_analyzed.explode('categories')
    
    return genres_analyzed

def year_formatting(film_full):
    year_analysis = film_full.dropna(subset = 'release_date')
    year_analysis['year'] = year_analysis['release_date'].apply(lambda s : s[: 4])
    year_analysis[year_analysis['year'] == 'http'] = np.nan
    year_analysis['year'] = year_analysis['year'].astype(int)

    return year_analysis

def run_time_analysis(year_analysis):
    run_time_analysis = year_analysis[year_analysis['runtime'] <= 1000]

    mean_run_time_per_year_not_oscar = run_time_analysis[run_time_analysis['nbOscarReceived'] == 0].groupby(['year']).agg({'runtime' : 'mean'}).reset_index()
    mean_run_time_oscar = run_time_analysis[run_time_analysis['nbOscarReceived'] > 0].groupby('year').agg({'runtime' : 'mean'}).reset_index()


    min_year_oscar = mean_run_time_oscar['year'].min()
    max_year_oscar = mean_run_time_oscar['year'].max()

    mean_run_time_per_year_not_oscar =  mean_run_time_per_year_not_oscar[mean_run_time_per_year_not_oscar['year'] >= min_year_oscar]
    mean_run_time_per_year_not_oscar =  mean_run_time_per_year_not_oscar[mean_run_time_per_year_not_oscar['year'] <= max_year_oscar]

    mean_run_time_per_year_not_oscar = mean_run_time_per_year_not_oscar.rename(columns={'runtime' : 'mean run time without oscar'})
    mean_run_time_oscar = mean_run_time_oscar.rename(columns={'runtime' : 'mean run time with oscar'})

    mean_run_time = pd.merge(mean_run_time_oscar, mean_run_time_per_year_not_oscar, on='year', how='outer')

    mean_title_length_per_year_not_oscar = year_analysis[year_analysis['nbOscarReceived'] == 0].groupby(['year']).agg({'title_length' : 'mean'}).reset_index()
    mean_title_length_oscar = year_analysis[year_analysis['nbOscarReceived'] > 0].groupby('year').agg({'title_length' : 'mean'}).reset_index()

    mean_title_length_per_year_not_oscar = mean_title_length_per_year_not_oscar.rename(columns={'title_length' : 'title length without oscar'})
    mean_title_length_oscar  = mean_title_length_oscar.rename(columns={'title_length' : 'mean title length with oscar'})


    min_year_oscar = mean_title_length_oscar['year'].min()
    max_year_oscar = mean_run_time_per_year_not_oscar['year'].max()

    mean_title_length_per_year_not_oscar=  mean_title_length_per_year_not_oscar[mean_title_length_per_year_not_oscar['year'] >= min_year_oscar]
    mean_title_length_per_year_not_oscar=  mean_title_length_per_year_not_oscar[mean_title_length_per_year_not_oscar['year'] <= max_year_oscar]

    mean_title_length = pd.merge(mean_title_length_oscar , mean_title_length_per_year_not_oscar, on='year', how='outer')

    return mean_run_time, mean_title_length

def sentiment_analysis(plot_summaries, year_analysis):
    summary_analysis = pd.merge(year_analysis, plot_summaries, left_on='wikipedia_id', right_on='Wikipedia movie ID')

    mean_positive_per_year_not_oscar = summary_analysis[summary_analysis['oscar']].groupby(['year']).agg({'sentiment_positive' : 'mean', 'sentiment_negative' : 'mean', 'sentiment_compound' : 'mean'}).reset_index()
    mean_positive_per_year_not_oscar.columns = ['year', 'mean_positive_not_oscar', 'mean_negative_not_oscar', 'mean_compound_not_oscar']
    mean_positive_oscar = summary_analysis[summary_analysis['oscar'] == False].groupby('year').agg({'sentiment_positive' : 'mean', 'sentiment_negative' : 'mean',  'sentiment_compound' : 'mean'} ).reset_index()
    mean_positive_oscar.columns = ['year', 'mean_positive_oscar', 'mean_negative_oscar', 'mean_compound_oscar']

    min_year_oscar = summary_analysis['year'].min()
    max_year_oscar = summary_analysis['year'].max()

    mean_positive_per_year_not_oscar =  mean_positive_per_year_not_oscar[mean_positive_per_year_not_oscar['year'] >= min_year_oscar]
    mean_positive_per_year_not_oscar=  mean_positive_per_year_not_oscar[mean_positive_per_year_not_oscar['year'] <= max_year_oscar]

    mean_positive = pd.merge(mean_positive_oscar ,mean_positive_per_year_not_oscar , on='year', how='outer')

    mean_positive.dropna(subset=['mean_positive_oscar', 'mean_positive_not_oscar'], inplace=True)
    
    return mean_positive, summary_analysis