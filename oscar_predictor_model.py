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


film_full =  load_dataframe_from_csv('film_full_2.csv')
film_full = clean_film_full(film_full)
film_full['nbOscarReceived'] = pd.to_numeric(film_full['nbOscarReceived'], errors='coerce')
print(film_full['nbOscarReceived'].isna().sum())
film_full['nbOscarReceived'] = film_full['nbOscarReceived'].fillna(0)


# Create the target variable: Did the movie win an Oscar? (1 if nbOscarsReceived > 0, else 0)
film_full['Oscar_Win'] = np.where(film_full['nbOscarReceived'] > 0, 1, 0)

# Extract release month and year from the release date
film_full['release_date'] = pd.to_datetime(film_full['release_date'], errors='coerce')  # Convert to datetime
film_full['release_month'] = film_full['release_date'].dt.month  # Extract month
film_full['release_year'] = film_full['release_date'].dt.year  # Extract year

# Filter the dataset
filtered_data = film_full[
    (film_full['nbOscarNominated'] > 0) | (film_full['box_office'] > 10000000)
]

# Step 3: Define Features and Target
features = ['box_office', 'runtime', 'reviewScores', 'capitalCost', 'genres', 'release_month', 'release_year']
target = 'Oscar_Win'

# One-hot encode genres and fill missing values for numerical columns
categorical_features = ['genres', 'release_month']
numerical_features = ['box_office', 'runtime', 'reviewScores', 'capitalCost', 'release_year']

# Define a column transformer for preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        ('num', Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ]), numerical_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ]
)

# Step 4: Train-Test Split
X = filtered_data[features]
y = filtered_data[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

# Step 5: Define the Model Pipeline
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(random_state=42, n_estimators=100, class_weight='balanced'))
])

# Step 6: Train the Model
model.fit(X_train, y_train)

# Step 7: Evaluate the Model
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]  # Probability of winning an Oscar

# Classification metrics
print("Accuracy:", accuracy_score(y_test, y_pred))
print("AUC-ROC Score:", roc_auc_score(y_test, y_proba))
print("Classification Report:\n", classification_report(y_test, y_pred))

# Feature importance (only for RandomForest)
if hasattr(model.named_steps['classifier'], 'feature_importances_'):
    feature_importances = model.named_steps['classifier'].feature_importances_
    feature_names = preprocessor.transformers_[0][2] + list(
        model.named_steps['preprocessor'].transformers_[1][1].get_feature_names_out()
    )
    importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': feature_importances})
    print("\nTop Features:")
    print(importance_df.sort_values(by='Importance', ascending=False).head(10))

# Save the model (optional)
joblib.dump(model, "oscar_prediction_model.pkl")