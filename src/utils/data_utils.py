import pandas as pd
import os 
import sys
sys.path.append('/Users/williamjallot/Desktop/ADA/ada-2024-project-5ds/src/utils')


def save_dataframe_to_csv(df, csv_filename) :

    csv_file_path = os.path.join('/Users/williamjallot/Desktop/ADA/ada-2024-project-5ds/data', csv_filename)

    df.to_csv(csv_file_path, index=False)

def load_dataframe_from_csv(file_name) :
    # Get the current directory where the script or notebook is located
    data_directory = os.path.abspath(os.path.join('..', '/Users/williamjallot/Desktop/ADA/ada-2024-project-5ds/data'))
    csv_file_path = os.path.join('/Users/williamjallot/Desktop/ADA/ada-2024-project-5ds/data', file_name)
    df_loaded = pd.read_csv(csv_file_path)
    return df_loaded