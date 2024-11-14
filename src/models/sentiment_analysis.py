from nltk.sentiment import SentimentIntensityAnalyzer
from nltk import tokenize
from nltk.sentiment.util import *

class SentimentAnalysis:

    def __init__(self, text):
        self.text_sentences = tokenize.sent_tokenize(text)
        self.sentim_analyzer = SentimentIntensityAnalyzer()

    def get_sentiment(self):
        for sentence in self.text_sentences:
            sentiment_score = self.sentim_analyzer.polarity_scores(sentence)
            print(sentiment_score)
            print("\n")
    

    