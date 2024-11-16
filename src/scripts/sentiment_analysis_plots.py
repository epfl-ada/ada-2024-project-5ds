import sys
import os
#Add upper directories to the system to ensure working importatons
current_directory = os.getcwd()
utils_directory = os.path.join(current_directory,'src', 'utils')
data_directory = os.path.join(current_directory, 'src', 'data')
model_directory = os.path.join(current_directory, 'src', 'models')

sys.path.append(os.path.abspath(utils_directory))
sys.path.append(os.path.abspath(data_directory))
sys.path.append(os.path.abspath(model_directory))

from dataloader import load_initial_dataset
from data_utils import save_dataframe_to_csv, load_dataframe_from_csv
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

def get_sentiment_from_plot(df, column_name, name_csv):
    print("Entering test function")
    df = get_sentiment_from_dataframe(df, column_name, name_csv)
    save_dataframe_to_csv(df, "plot_summaries.csv")
    print("Finished test function")

plot_summaries = load_dataframe_from_csv("plot_summaries.csv")

get_sentiment_from_plot(plot_summaries, "Summary", "plot_summaries.csv")