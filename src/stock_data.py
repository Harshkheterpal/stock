import yfinance as yf
from datetime import datetime, timedelta
import time
from requests.exceptions import HTTPError

class StockDataFetcher:
    def get_stock_data(self, stock_symbol, max_retries=3, retry_delay=5):
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    time.sleep(retry_delay)
                
                stock = yf.Ticker(stock_symbol)
                
                try:
                    current_price = stock.info.get('currentPrice')
                    currency = stock.info.get('currency', 'USD')
                    history = stock.history(period="30d")
                    history_data = history[['Close']]
                    history_data['Date'] = history_data.index
                    formatted_history = [{'date': row['Date'].strftime('%Y-%m-%d'), 'price': row['Close']} for _, row in history_data.iterrows()]
                    if current_price is None:
                        raise ValueError(f"Could not get current price for {stock_symbol}")
                        
                    return {
                        'success': True,
                        'data': {
                            'currency': currency,
                            'current_price': current_price,
                            'history': formatted_history
                        }
                    }
                    
                except HTTPError as e:
                    if e.response.status_code == 429:
                        print(f"Rate limit hit, attempt {attempt + 1} of {max_retries}")
                        if attempt == max_retries - 1:
                            raise ValueError("Rate limit exceeded. Please try again later.")
                        continue
                    raise
                
            except Exception as e:
                print(f"Error fetching stock data (attempt {attempt + 1}): {str(e)}")
                if attempt == max_retries - 1:
                    return {
                        'success': False,
                        'error': f"Failed to fetch stock data for {stock_symbol} after {max_retries} attempts: {str(e)}"
                    }
                continue 