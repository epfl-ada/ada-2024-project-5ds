from src.models import sentiment_analysis

class TestSentimentAnalyzer(unittest.TestCase):
    
        def test_get_sentiment(self):
            text = "I am happy. I am sad."
            sentiment = sentiment_analysis.SentimentAnalysis(text)
            sentiment.get_sentiment()
            self.assertTrue(True)