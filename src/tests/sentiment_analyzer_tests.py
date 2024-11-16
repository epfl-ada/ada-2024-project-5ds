import sys
import os

current_directory = os.getcwd()
utils_directory = os.path.join(current_directory,'src', 'utils')
data_directory = os.path.join(current_directory, 'src', 'data')
model_directory = os.path.join(current_directory, 'src', 'models')
script_directory = os.path.join(current_directory, 'src', 'scripts')
sys.path.append(os.path.abspath(utils_directory))
sys.path.append(os.path.abspath(data_directory))
sys.path.append(os.path.abspath(model_directory))
sys.path.append(os.path.abspath(script_directory))

from dataloader import load_initial_dataset
from sentiment_analysis_plots import get_sentiment_from_dataframe
from sentiment_analysis import get_sentiment_string
from data_utils import save_dataframe_to_csv, load_dataframe_from_csv
    
def test_get_sentiment():
    text = "I am happy."
    get_sentiment_string(text)  
    return True


