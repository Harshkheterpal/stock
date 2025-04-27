from flask import Flask, render_template, request, jsonify
from stock_data import StockDataFetcher 
import os
from dotenv import load_dotenv
from stock_sentiment import StockSentimentAnalyzer

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize analyzers to use stock sentiment analyzer
stock_fetcher = StockDataFetcher()
sentiment_analyzer = StockSentimentAnalyzer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # Get stock symbol from form
        stock_symbol = request.form.get('stock_symbol', '').upper()
        # Get stock trend prediction
        prediction = sentiment_analyzer.predict_trend(stock_symbol)
        
        # Get stock data
        stock_data = stock_fetcher.get_stock_data(stock_symbol)

        # Combine the data
        result = {
            'stock_symbol': stock_symbol,
            'sentiment': sentiment_data,
            'stock_data': stock_data
        }
        
        return jsonify(result) 
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 