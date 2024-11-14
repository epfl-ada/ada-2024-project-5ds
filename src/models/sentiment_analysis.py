import nltk
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.sentiment.util import *

def get_sentiment_string(text):
    """
    Function to get the sentiment of a given text
    :param text: string
    :return
    sentiment_score: dict
    composed of the following
    - compound: float
    - positive: float
    - negative: float
    - neutral: float
    """
    sia = SentimentIntensityAnalyzer()
    sentiment_score = sia.polarity_scores(text)
    
    return sentiment_score
    

    