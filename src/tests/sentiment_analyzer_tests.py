import sys
sys.path.append('D:/UNIV/MASTER-EPFL/ADA/applied-project/ada-2024-project-5ds/src/models')
sys.path.append('D:/UNIV/MASTER-EPFL/ADA/applied-project/ada-2024-project-5ds/src/scripts')
sys.path.append('D:/UNIV/MASTER-EPFL/ADA/applied-project/ada-2024-project-5ds/src/data')
sys.path.append('D:/UNIV/MASTER-EPFL/ADA/applied-project/ada-2024-project-5ds/src/utils')
from dataloader import load_initial_dataset
from sentiment_analysis_plots import get_sentiment_from_dataframe
from sentiment_analysis import get_sentiment_string
from data_utils import save_dataframe_to_csv, load_dataframe_from_csv
    
def test_get_sentiment():
    text = "I am happy."
    get_sentiment_string(text)  
    return True


