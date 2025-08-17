import requests
import pandas as pd

# Placeholder for AI Copilot stock suggestion logic
# In production, replace with actual AI/LLM API integration

def get_copilot_suggested_stocks(prompt, country):
    # Dummy data for demonstration
    sample_stocks = {
        'India': ['RELIANCE', 'TCS', 'INFY', 'HDFCBANK', 'ICICIBANK', 'SBIN', 'BHARTIARTL', 'HINDUNILVR', 'KOTAKBANK', 'LT'],
        'USA': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NVDA', 'JPM', 'V', 'UNH'],
        'Australia': ['CBA', 'BHP', 'WBC', 'NAB', 'ANZ', 'WES', 'MQG', 'CSL', 'FMG', 'WOW']
    }
    return sample_stocks.get(country, [])

# Placeholder for fetching stock data
# Replace with actual API calls (e.g., Yahoo Finance, Alpha Vantage, etc.)
def fetch_stock_data(symbol, country):
    # Fetch real-time data from Yahoo Finance using yfinance
    if country == 'India':
        # Try nsetools first, fallback to yfinance if it fails
        try:
            from nsetools import Nse
            nse = Nse()
            data = nse.get_quote(symbol)
            if not data or 'lastPrice' not in data:
                raise Exception("No NSE data")
            price = data.get('lastPrice', None)
            volume = data.get('quantityTraded', None)
            pe_ratio = data.get('pE', None)
            dma_50 = None # Not available
            dma_200 = None # Not available
            return {
                'Symbol': symbol,
                'Price': price,
                'Volume': volume,
                'PE Ratio': pe_ratio,
                '50DMA': dma_50,
                '200DMA': dma_200,
                'Source': 'NSE'
            }
        except Exception as e:
            # Fallback to Yahoo Finance
            import yfinance as yf
            try:
                ticker = yf.Ticker(symbol + ".NS")
                info = ticker.info
                hist = ticker.history(period="1y")
                price = info.get('regularMarketPrice', None)
                volume = info.get('regularMarketVolume', None)
                pe_ratio = info.get('trailingPE', None)
                dma_50 = hist['Close'].rolling(window=50).mean().iloc[-1] if not hist.empty else None
                dma_200 = hist['Close'].rolling(window=200).mean().iloc[-1] if not hist.empty else None
                return {
                    'Symbol': symbol,
                    'Price': price,
                    'Volume': volume,
                    'PE Ratio': pe_ratio,
                    '50DMA': dma_50,
                    '200DMA': dma_200,
                    'Source': 'Yahoo Finance'
                }
            except Exception as e2:
                return {
                    'Symbol': symbol,
                    'Price': None,
                    'Volume': None,
                    'PE Ratio': None,
                    '50DMA': None,
                    '200DMA': None,
                    'Error': f"NSE error: {str(e)} | Yahoo error: {str(e2)}"
                }
    else:
        # Use Yahoo Finance for USA and Australia
        import yfinance as yf
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            hist = ticker.history(period="1y")
            price = info.get('regularMarketPrice', None)
            volume = info.get('regularMarketVolume', None)
            pe_ratio = info.get('trailingPE', None)
            dma_50 = hist['Close'].rolling(window=50).mean().iloc[-1] if not hist.empty else None
            dma_200 = hist['Close'].rolling(window=200).mean().iloc[-1] if not hist.empty else None
            return {
                'Symbol': symbol,
                'Price': price,
                'Volume': volume,
                'PE Ratio': pe_ratio,
                '50DMA': dma_50,
                '200DMA': dma_200
            }
        except Exception as e:
            return {
                'Symbol': symbol,
                'Price': None,
                'Volume': None,
                'PE Ratio': None,
                '50DMA': None,
                '200DMA': None,
                'Error': str(e)
            }

def main():
    while True:
        print("Select country:")
        print("1. India")
        print("2. USA")
        print("3. Australia")
        country_choice = input("Enter 1, 2, or 3: ").strip()
        if country_choice == "1":
            countries = ['India']
            break
        elif country_choice == "2":
            countries = ['USA']
            break
        elif country_choice == "3":
            countries = ['Australia']
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

    while True:
        print("Select stock suggestion type:")
        print("1. Technical")
        print("2. Fundamental")
        print("3. Both")
        type_choice = input("Enter 1, 2, or 3: ").strip()
        if type_choice == "1":
            suggestion_type = "technical"
            break
        elif type_choice == "2":
            suggestion_type = "fundamental"
            break
        elif type_choice == "3":
            suggestion_type = "both"
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

    while True:
        try:
            num_stocks = int(input("How many top stocks do you want to see? (default 10): ").strip())
            if num_stocks > 0:
                break
            else:
                print("Please enter a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    for country in countries:
        prompt = f"Top {num_stocks} stocks for {country} based on {suggestion_type} indicators"
        print(f"\nCopilot-suggested stocks for {country} ({prompt}):")
        stocks = get_copilot_suggested_stocks(prompt, country)[:num_stocks]
        country_data = []
        for symbol in stocks:
            data = fetch_stock_data(symbol, country)
            country_data.append(data)
            print(f"{symbol}: Price={data['Price']}, Volume={data['Volume']}, PE={data['PE Ratio']}, 50DMA={data['50DMA']}, 200DMA={data['200DMA']}")
        # Optionally, save to CSV
        df = pd.DataFrame(country_data)
        df.to_csv(f'copilot_suggested_stocks_{country}.csv', index=False)
        print(f"\nStock data saved to copilot_suggested_stocks_{country}.csv")

if __name__ == "__main__":
    main()
