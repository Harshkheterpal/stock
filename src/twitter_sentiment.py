import tweepy, os
from nltk.sentiment import SentimentIntensityAnalyzer
from dotenv import load_dotenv

load_dotenv()

class TwitterApi:
    def __init__(self):
        self.client = tweepy.Client(
            bearer_token=os.getenv('TWITTER_BEARER_TOKEN'),
            consumer_key=os.getenv('TWITTER_API_KEY'),
            consumer_secret=os.getenv('TWITTER_API_SECRET'),
            access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
            access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        )
        

    def get_tweets(self, ticker, max_results = 100):
        query = f"#{ticker} -is:retweet"
        response = self.client.search_recent_tweets(query=query, max_results=max_results)
        if response and response.data:
            return [tweet.text for tweet in response.data]
        return []
        
class TwitterSentiment:
    def __init__(self):
        self.twitter_api = TwitterApi()
        self.sia = SentimentIntensityAnalyzer()

    def get_sentiment(self, ticker, max_results = 100):
        tweets = self.twitter_api.get_tweets(ticker, max_results)
        sentiments = []
        for tweet in tweets:
            sentiment = self.sia.polarity_scores(tweet)['compound']
            sentiments.append(sentiment)
        
        if sentiments:
            return sum(sentiments) / len(sentiments)
        return 0.0
    