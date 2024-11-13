import pandas as pd
import os 

def save_dataframe_to_csv(df, csv_filename) :
    # Get the current working directory
    current_directory = os.getcwd()

    cleaned_data_directory = os.path.abspath(os.path.join(current_directory, '..', 'cleaned_data'))


    os.makedirs(cleaned_data_directory, exist_ok=True)  

    csv_file_path = os.path.join(cleaned_data_directory, csv_filename)

    df.to_csv(csv_file_path, index=False)

def load_dataframe_from_csv(file_name) :
    # Get the current directory where the script or notebook is located
    current_directory = os.getcwd()

    cleaned_data_directory = os.path.abspath(os.path.join(current_directory, '..', 'cleaned_data'))
    csv_file_path = os.path.join(cleaned_data_directory, file_name)
    df_loaded = pd.read_csv(csv_file_path)
    return df_loaded