import numpy as np
import yfinance as yf
from nltk.sentiment import SentimentIntensityAnalyzer
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from .src.twitter_sentiment import TwitterSentiment
import nltk

# Download required NLTK data
nltk.download('vader_lexicon')

# Load environment variables
load_dotenv()

class StockSentimentAnalyzer:
    def __init__(self):
        # Initialize Sentiment Analyzer
        self.sia = SentimentIntensityAnalyzer()
        self.twitter_sentiment = TwitterSentiment()

    def get_stock_data(self, stock_symbol, days=30):
        """Fetch historical stock data."""
        return yf.Ticker(stock_symbol).history(start=datetime.now() - timedelta(days=days), end=datetime.now())

    def predict_trend(self, stock_symbol):
        """Predict stock trend based on twitter sentiment."""
        return self.twitter_sentiment.get_sentiment(stock_symbol)

def main():
    # Initialize analyzer
    analyzer = StockSentimentAnalyzer()
    
    # Get user input
    stock_symbol = input("Enter stock symbol (e.g., AAPL): ").upper()
    
    try:
        # Get prediction
        prediction = analyzer.predict_trend(stock_symbol)
        print(f"\nAnalysis for {stock_symbol}:")
        print(prediction)
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 