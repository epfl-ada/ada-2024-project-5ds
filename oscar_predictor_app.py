import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, roc_auc_score, accuracy_score
from sklearn.impute import SimpleImputer
import datetime
import streamlit as st
import pandas as pd
import joblib
from src.utils.data_utils import load_dataframe_from_csv
from src.scripts.movie_analysis import clean_film_full



# Load the pre-trained model
model = joblib.load("oscar_prediction_model.pkl")

# Title of the app
st.title("Oscar Probability Predictor")

# Create input fields for user to provide movie details
st.header("Enter Movie Details")

box_office = st.number_input("Box Office Revenue (in millions)", min_value=0.0, step=0.1)
runtime = st.number_input("Movie Runtime (in minutes)", min_value=30, max_value=300, step=1)
review_scores = st.slider("Review Scores (0-100)", min_value=0, max_value=100, step=1)
capital_cost = st.number_input("Capital Cost (in millions)", min_value=0.0, step=0.1)
genres = st.selectbox("Genre", ["Action", "Drama", "Comedy", "Horror", "Sci-Fi", "Romance"])
release_month = st.selectbox("Release Month", list(range(1, 13)))
release_year = st.number_input("Release Year", min_value=1900, max_value=2024, step=1)

# Create a dictionary of the user input
input_data = pd.DataFrame({
    'box_office': [box_office],
    'runtime': [runtime],
    'reviewScores': [review_scores],
    'capitalCost': [capital_cost],
    'genres': [genres],
    'release_month': [release_month],
    'release_year': [release_year]
})


if st.button("Predict"):
    with st.spinner("Calculating probability..."):
        probability = model.predict_proba(input_data)[0, 1]
        st.success(f"Probability of Winning an Oscar: {probability:.2%}")    


@st.cache_data
def load_model():
    return joblib.load("oscar_prediction_model.pkl")
model = load_model()
