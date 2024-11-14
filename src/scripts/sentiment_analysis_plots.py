import sys
sys.path.append('D:/UNIV/MASTER-EPFL/ADA/applied-project/ada-2024-project-5ds/src/models')
sys.path.append('D:/UNIV/MASTER-EPFL/ADA/applied-project/ada-2024-project-5ds/src/utils')
sys.path.append('D:/UNIV/MASTER-EPFL/ADA/applied-project/ada-2024-project-5ds/src/data')
from dataloader import load_initial_dataset
from loading_utils import save_dataframe_to_csv, load_dataframe_from_csv
from sentiment_analysis import get_sentiment_string
import pandas as pd



def get_sentiment_from_dataframe(df, column_name, name_csv):
    """
    Function to get the sentiment of a given text
    :param df: dataframe
    :return
    df: dataframe
    composed of the usual columns following those new columns
    - sentiment_compound: float
    - sentiment_positive: float
    - sentiment_negative: float
    - sentiment_neutral: float
    """
    print("Entering sentiment analysis function")
    sentiments = df[column_name].apply(get_sentiment_string)
    df['sentiment_compound'] = sentiments.apply(lambda x: x['compound'])
    df['sentiment_negative'] = sentiments.apply(lambda x: x['neg'])
    df['sentiment_neutral'] = sentiments.apply(lambda x: x['neu'])
    df['sentiment_positive'] = sentiments.apply(lambda x: x['pos'])
    print("Finished sentiment analysis")
    
    save_dataframe_to_csv(df, name_csv)
    return df 