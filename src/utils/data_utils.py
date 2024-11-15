import pandas as pd
import os 
import sys

def save_dataframe_to_csv(df, csv_filename) :
    """
    Save the panda dataframe in the file named data
    """
    # Get the current directory where the file is located
    current_directory = os.getcwd()
    data_directory =  os.path.abspath(os.path.join(current_directory, 'data'))
    csv_file_path = os.path.join(data_directory, csv_filename)

    #Save the file
    df.to_csv(csv_file_path, index=False)

def load_dataframe_from_csv(file_name) :
    """
    Load a panda dataframe in the file named data given file_name
    """
    # Get the current directory where the file is located
    current_directory = os.getcwd()
    data_directory =  os.path.abspath(os.path.join(current_directory, 'data'))
    csv_file_path = os.path.join(data_directory, file_name)

    #Load the file
    df_loaded = pd.read_csv(csv_file_path)
    return df_loaded