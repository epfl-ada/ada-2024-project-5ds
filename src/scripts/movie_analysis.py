import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import ttest_ind
import pycountry
import pycountry_convert as pc
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report
from imblearn.over_sampling import SMOTE
from sklearn.compose import make_column_transformer
import joblib


# Function to extract only the digits outside parentheses
def extract_digits(value):
    """
    Extracts leading digits from a string and returns them as an integer.
    
    Parameters:
    value (str or any): The input value from which to extract leading digits.
    
    Returns:
    int or any: The extracted leading digits as an integer if the input 
    is a string starting with digits, otherwise the original input value.
    """
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
    """
    Function to create a heatmap of the correlation matrix.

    Parameters:
    corr_matrix (pd.DataFrame): The correlation matrix to visualize.
    title (str): The title of the heatmap.

    Returns:
    showing the heatmap

    """
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
    """
    Creates a table of p-values for the t-test between two groups.

    Parameters:
    pvalues_df (pd.DataFrame): The DataFrame containing the p-values.
    title (str): The title of the table.

    Returns:
    showing the table
    """

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
    """
    Computes the p-values for the t-test between two groups for each column.

    Parameters:
    group1 (pd.DataFrame): The first group for the t-test.
    group2 (pd.DataFrame): The second group for the t-test.
    columns (list): The list of columns for which to compute the p-values.

    Returns:
    dict: A dictionary containing the p-values for each column.
    """
    p_values = {}
    for col in columns:
        stat, p_val = ttest_ind(group1[col], group2[col], alternative='two-sided')
        p_values[col] = p_val
    return p_values

def country_to_continent(country_name):
    """
    Convert a country name to its continent name.
    
    Parameters:
    country_name (str): The name of the country.

    Returns:
    str: The name of the continent.
    """
    country_alpha2 = pc.country_name_to_country_alpha2(country_name)
    country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
    country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
    return country_continent_name

def compute_countries_count(film_full):
    """
    Compute the number of Oscars received by each country.

    Parameters:
    film_full (pd.DataFrame): The full dataset of films.

    Returns:
    pd.DataFrame: A DataFrame containing the number of Oscars received by each country.
    """
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
    """
    Analyze the genres of the films.
    
    Parameters:
    film_full (pd.DataFrame): The full dataset of films.

    Returns:
    pd.DataFrame: A DataFrame containing the genres of the films.
    """

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
    """
    Perform the formatting of the year column.

    Parameters:
    film_full (pd.DataFrame): The full dataset of films.

    Returns:
    pd.DataFrame: A DataFrame containing the formatted year column.
    """
    year_analysis = film_full.dropna(subset = 'release_date')
    year_analysis['year'] = year_analysis['release_date'].apply(lambda s : s[: 4])
    year_analysis[year_analysis['year'] == 'http'] = np.nan
    year_analysis['year'] = year_analysis['year'].astype(int)

    return year_analysis

def run_time_analysis(year_analysis):
    """
    Perform the analysis of the run time of the films.
    
    Parameters:
    year_analysis (pd.DataFrame): The DataFrame containing the year analysis.

    Returns:
    pd.DataFrame: A DataFrame containing the mean run time per year.
    """
    # Filter out films with runtime greater than 1000 minutes
    run_time_analysis = year_analysis[year_analysis['runtime'] <= 1000]

    # Calculate mean runtime per year for films that did not receive an Oscar
    mean_run_time_per_year_not_oscar = run_time_analysis[run_time_analysis['nbOscarReceived'] == 0].groupby(['year']).agg({'runtime': 'mean'}).reset_index()
    # Calculate mean runtime per year for films that received at least one Oscar
    mean_run_time_oscar = run_time_analysis[run_time_analysis['nbOscarReceived'] > 0].groupby('year').agg({'runtime': 'mean'}).reset_index()

    # Determine the minimum and maximum year for films that received an Oscar
    min_year_oscar = mean_run_time_oscar['year'].min()
    max_year_oscar = mean_run_time_oscar['year'].max()

    # Filter the non-Oscar films to match the year range of Oscar films
    mean_run_time_per_year_not_oscar = mean_run_time_per_year_not_oscar[mean_run_time_per_year_not_oscar['year'] >= min_year_oscar]
    mean_run_time_per_year_not_oscar = mean_run_time_per_year_not_oscar[mean_run_time_per_year_not_oscar['year'] <= max_year_oscar]

    # Rename columns for clarity
    mean_run_time_per_year_not_oscar = mean_run_time_per_year_not_oscar.rename(columns={'runtime': 'mean run time without oscar'})
    mean_run_time_oscar = mean_run_time_oscar.rename(columns={'runtime': 'mean run time with oscar'})

    # Merge the two DataFrames on the year column
    mean_run_time = pd.merge(mean_run_time_oscar, mean_run_time_per_year_not_oscar, on='year', how='outer')

    # Calculate mean title length per year for films that did not receive an Oscar
    mean_title_length_per_year_not_oscar = year_analysis[year_analysis['nbOscarReceived'] == 0].groupby(['year']).agg({'title_length': 'mean'}).reset_index()
    # Calculate mean title length per year for films that received at least one Oscar
    mean_title_length_oscar = year_analysis[year_analysis['nbOscarReceived'] > 0].groupby('year').agg({'title_length': 'mean'}).reset_index()

    # Rename columns for clarity
    mean_title_length_per_year_not_oscar = mean_title_length_per_year_not_oscar.rename(columns={'title_length': 'title length without oscar'})
    mean_title_length_oscar = mean_title_length_oscar.rename(columns={'title_length': 'mean title length with oscar'})

    # Determine the minimum and maximum year for films that received an Oscar
    min_year_oscar = mean_title_length_oscar['year'].min()
    max_year_oscar = mean_run_time_per_year_not_oscar['year'].max()

    # Filter the non-Oscar films to match the year range of Oscar films
    mean_title_length_per_year_not_oscar = mean_title_length_per_year_not_oscar[mean_title_length_per_year_not_oscar['year'] >= min_year_oscar]
    mean_title_length_per_year_not_oscar = mean_title_length_per_year_not_oscar[mean_title_length_per_year_not_oscar['year'] <= max_year_oscar]

    # Merge the two DataFrames on the year column
    mean_title_length = pd.merge(mean_title_length_oscar, mean_title_length_per_year_not_oscar, on='year', how='outer')

    return mean_run_time, mean_title_length

def sentiment_analysis(plot_summaries, year_analysis):
    """
    Perform the sentiment analysis of the plot summaries.

    Parameters:
    plot_summaries (pd.DataFrame): The DataFrame containing the plot summaries.
    year_analysis (pd.DataFrame): The DataFrame containing the year analysis.

    Returns:
    pd.DataFrame: A DataFrame containing the mean sentiment scores per year.
    """
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

def process_and_train(data, output_dir='.'):
      """
      Preprocess data, train an SVM model, and save artifacts.
  
      Parameters:
          data (pd.DataFrame): Input dataset containing 'categories', 'nbOscarReceived', 'title_length', 'box_office', and 'runtime'.
          output_dir (str): Directory to save the trained model and preprocessing objects.
  
      Returns:
          dict: Dictionary containing the best parameters, cross-validation scores, and classification report.
      """
      # Drop rows with NaN in the 'categories' column
      data = data.dropna(subset=['categories'])
  
      # Create target column 'oscar'
      data['oscar'] = data['nbOscarReceived'] >= 1
  
      # Select relevant columns
      data = data[['oscar', 'title_length', 'categories', 'box_office', 'runtime']]
  
      # Clean the 'categories' column
      data['categories'] = (
          data['categories']
          .str.strip('[]')
          .str.replace("'", '')
          .str.replace('"', '')
          .str.strip()
      )
  
      # Process categories column into clean lists
      data['categories'] = data['categories'].apply(lambda s: [x.strip() for x in s.split(',')] if isinstance(s, str) else [])
      data['categories'] = data['categories'].apply(lambda s: list(set(filter(None, s))))
      data['categories'] = data['categories'].apply(lambda s: [x.lower().capitalize() for x in s])
  
      # Explode categories and drop NA rows
      data = data.explode('categories')
      data = data.dropna(subset=['oscar', 'title_length', 'categories', 'box_office', 'runtime'])
  
      # Features and target
      y = data['oscar']
      X = data[['title_length', 'categories', 'box_office', 'runtime']]
  
      # Preprocess categorical and numerical features before SMOTE
      pre_smote_preprocessor = make_column_transformer(
          (StandardScaler(with_mean=False), ['title_length', 'box_office', 'runtime']),
          (OneHotEncoder(drop='first', sparse_output=True), ['categories'])
      )
  
      # Apply preprocessing before SMOTE
      X_preprocessed = pre_smote_preprocessor.fit_transform(X)
  
      # Resample data using SMOTE
      smote = SMOTE(random_state=42)
      X_resampled, y_resampled = smote.fit_resample(X_preprocessed, y)
  
      # Define preprocessing for the pipeline
      pipeline_preprocessor = ColumnTransformer(
          transformers=[
              ('num', StandardScaler(with_mean=False), slice(0, X_resampled.shape[1]))
          ]
      )
  
      # Create the SVM pipeline with RBF kernel
      svm_pipeline = Pipeline(steps=[
          ('preprocessor', pipeline_preprocessor),
          ('svm', SVC(kernel='rbf', class_weight='balanced', probability=True, random_state=42))
      ])
  
      # Hyperparameter tuning
      param_grid = {
          'svm__C': [10],
          'svm__gamma': [24]
      }
      grid_search = GridSearchCV(svm_pipeline, param_grid, cv=5, scoring='balanced_accuracy', verbose=2, n_jobs=-1)
      grid_search.fit(X_resampled, y_resampled)
  
      # Best parameters
      best_params = grid_search.best_params_
  
      # Evaluate the best model
      best_model = grid_search.best_estimator_
      cv_scores = cross_val_score(best_model, X_resampled, y_resampled, cv=5, scoring='recall')
  
      # Fit the model and generate predictions
      best_model.fit(X_resampled, y_resampled)
      y_pred = best_model.predict(pre_smote_preprocessor.transform(X))
  
      # Compute confusion matrix
      cm = confusion_matrix(y, y_pred)
      disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=best_model.named_steps['svm'].classes_)
      disp.plot(cmap='Blues')
      plt.title('Confusion Matrix (RBF Kernel)')
      plt.show()
  
      # Classification report
      report = classification_report(y, y_pred, output_dict=True)
  
      # Save artifacts
      joblib.dump(pre_smote_preprocessor, f'{output_dir}/pre_smote_preprocessor.pkl')
      joblib.dump(smote, f'{output_dir}/smote.pkl')
      joblib.dump(best_model, f'{output_dir}/svm_model.pkl')
  
      print("Preprocessor, SMOTE, and model saved successfully.")
  
      return {
          'best_params': best_params,
          'cv_scores': cv_scores,
          'mean_cv_score': np.mean(cv_scores),
          'classification_report': report
      }

def load_and_predict(film, input_dir ="data/", preprocessor_path='pre_smote_preprocessor.pkl', 
                     smote_path='smote.pkl', model_path='svm_model.pkl'):
    """
    Load pre-trained components and make predictions for a given film.

    Parameters:
        film (list): List containing the film data [title_length, categories, box_office, runtime].
        preprocessor_path (str): Path to the saved preprocessor.
        smote_path (str): Path to the saved SMOTE object.
        model_path (str): Path to the saved model.

    Returns:
        dict: Dictionary containing predictions and probabilities.
    """
    # Load saved components
    loaded_preprocessor = joblib.load(input_dir+ preprocessor_path)
    loaded_smote = joblib.load(input_dir + smote_path)
    loaded_model = joblib.load( input_dir + model_path)

    print("Components loaded successfully.")

    # Prepare the film data
    film_data = pd.DataFrame([film], columns=['title_length', 'categories', 'box_office', 'runtime'])

    # Preprocess the new data
    X_new_preprocessed = loaded_preprocessor.transform(film_data)

    # Generate predictions and probabilities using the loaded model
    new_predictions = loaded_model.predict(X_new_preprocessed)
    new_probabilities = loaded_model.predict_proba(X_new_preprocessed)

    return new_predictions, new_probabilities