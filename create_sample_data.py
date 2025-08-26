import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Create comprehensive stock data for multiple markets
def create_sample_stock_data():
    # Stock data for different markets
    stocks_data = {
        'India': [
            {'Symbol': 'RELIANCE', 'Company': 'Reliance Industries Ltd', 'Sector': 'Energy', 'Market_Cap': 1500000, 'Price': 2450.50, 'Volume': 8500000, 'PE_Ratio': 12.5, 'PB_Ratio': 1.8, 'Dividend_Yield': 0.35, 'ROE': 14.2, 'Debt_to_Equity': 0.25, 'EPS': 196.0, 'Revenue_Growth': 8.5, 'Profit_Margin': 7.2},
            {'Symbol': 'TCS', 'Company': 'Tata Consultancy Services', 'Sector': 'IT Services', 'Market_Cap': 1200000, 'Price': 3520.75, 'Volume': 3200000, 'PE_Ratio': 28.5, 'PB_Ratio': 12.8, 'Dividend_Yield': 1.2, 'ROE': 45.3, 'Debt_to_Equity': 0.05, 'EPS': 123.5, 'Revenue_Growth': 15.2, 'Profit_Margin': 25.1},
            {'Symbol': 'INFY', 'Company': 'Infosys Limited', 'Sector': 'IT Services', 'Market_Cap': 650000, 'Price': 1420.30, 'Volume': 4800000, 'PE_Ratio': 24.8, 'PB_Ratio': 8.9, 'Dividend_Yield': 2.1, 'ROE': 31.2, 'Debt_to_Equity': 0.08, 'EPS': 57.2, 'Revenue_Growth': 12.8, 'Profit_Margin': 22.4},
            {'Symbol': 'HDFCBANK', 'Company': 'HDFC Bank Limited', 'Sector': 'Banking', 'Market_Cap': 850000, 'Price': 1580.40, 'Volume': 12000000, 'PE_Ratio': 18.9, 'PB_Ratio': 2.8, 'Dividend_Yield': 1.0, 'ROE': 17.1, 'Debt_to_Equity': 6.2, 'EPS': 83.6, 'Revenue_Growth': 18.5, 'Profit_Margin': 23.8},
            {'Symbol': 'ICICIBANK', 'Company': 'ICICI Bank Limited', 'Sector': 'Banking', 'Market_Cap': 650000, 'Price': 920.15, 'Volume': 15000000, 'PE_Ratio': 15.4, 'PB_Ratio': 2.1, 'Dividend_Yield': 0.8, 'ROE': 15.8, 'Debt_to_Equity': 5.8, 'EPS': 59.7, 'Revenue_Growth': 16.2, 'Profit_Margin': 21.5},
            {'Symbol': 'BHARTIARTL', 'Company': 'Bharti Airtel Limited', 'Sector': 'Telecom', 'Market_Cap': 450000, 'Price': 825.60, 'Volume': 7500000, 'PE_Ratio': 22.1, 'PB_Ratio': 4.2, 'Dividend_Yield': 0.6, 'ROE': 19.3, 'Debt_to_Equity': 1.4, 'EPS': 37.4, 'Revenue_Growth': 11.8, 'Profit_Margin': 12.5},
            {'Symbol': 'HINDUNILVR', 'Company': 'Hindustan Unilever Ltd', 'Sector': 'FMCG', 'Market_Cap': 520000, 'Price': 2380.90, 'Volume': 2200000, 'PE_Ratio': 58.5, 'PB_Ratio': 18.2, 'Dividend_Yield': 1.4, 'ROE': 82.1, 'Debt_to_Equity': 0.12, 'EPS': 40.7, 'Revenue_Growth': 9.2, 'Profit_Margin': 18.4},
            {'Symbol': 'KOTAKBANK', 'Company': 'Kotak Mahindra Bank', 'Sector': 'Banking', 'Market_Cap': 380000, 'Price': 1820.25, 'Volume': 3800000, 'PE_Ratio': 16.8, 'PB_Ratio': 2.6, 'Dividend_Yield': 0.5, 'ROE': 16.2, 'Debt_to_Equity': 4.9, 'EPS': 108.4, 'Revenue_Growth': 22.1, 'Profit_Margin': 19.8},
            {'Symbol': 'LT', 'Company': 'Larsen & Toubro Limited', 'Sector': 'Infrastructure', 'Market_Cap': 280000, 'Price': 2150.80, 'Volume': 1800000, 'PE_Ratio': 25.6, 'PB_Ratio': 3.1, 'Dividend_Yield': 1.8, 'ROE': 12.8, 'Debt_to_Equity': 0.45, 'EPS': 84.0, 'Revenue_Growth': 14.2, 'Profit_Margin': 8.1},
            {'Symbol': 'SBIN', 'Company': 'State Bank of India', 'Sector': 'Banking', 'Market_Cap': 520000, 'Price': 625.45, 'Volume': 25000000, 'PE_Ratio': 9.8, 'PB_Ratio': 1.1, 'Dividend_Yield': 2.5, 'ROE': 12.4, 'Debt_to_Equity': 8.2, 'EPS': 63.8, 'Revenue_Growth': 8.9, 'Profit_Margin': 18.6}
        ],
        
        'USA': [
            {'Symbol': 'AAPL', 'Company': 'Apple Inc', 'Sector': 'Technology', 'Market_Cap': 2800000, 'Price': 175.25, 'Volume': 45000000, 'PE_Ratio': 28.4, 'PB_Ratio': 45.2, 'Dividend_Yield': 0.5, 'ROE': 147.4, 'Debt_to_Equity': 1.73, 'EPS': 6.16, 'Revenue_Growth': 2.8, 'Profit_Margin': 25.3},
            {'Symbol': 'MSFT', 'Company': 'Microsoft Corporation', 'Sector': 'Technology', 'Market_Cap': 2500000, 'Price': 335.50, 'Volume': 22000000, 'PE_Ratio': 32.1, 'PB_Ratio': 12.8, 'Dividend_Yield': 0.8, 'ROE': 39.1, 'Debt_to_Equity': 0.31, 'EPS': 10.45, 'Revenue_Growth': 12.1, 'Profit_Margin': 36.7},
            {'Symbol': 'GOOGL', 'Company': 'Alphabet Inc', 'Sector': 'Technology', 'Market_Cap': 1650000, 'Price': 138.20, 'Volume': 28000000, 'PE_Ratio': 25.8, 'PB_Ratio': 5.2, 'Dividend_Yield': 0.0, 'ROE': 20.1, 'Debt_to_Equity': 0.11, 'EPS': 5.35, 'Revenue_Growth': 8.4, 'Profit_Margin': 21.2},
            {'Symbol': 'AMZN', 'Company': 'Amazon.com Inc', 'Sector': 'E-commerce', 'Market_Cap': 1450000, 'Price': 140.75, 'Volume': 35000000, 'PE_Ratio': 42.1, 'PB_Ratio': 8.1, 'Dividend_Yield': 0.0, 'ROE': 19.3, 'Debt_to_Equity': 0.54, 'EPS': 3.34, 'Revenue_Growth': 9.4, 'Profit_Margin': 7.8},
            {'Symbol': 'TSLA', 'Company': 'Tesla Inc', 'Sector': 'Automotive', 'Market_Cap': 800000, 'Price': 248.50, 'Volume': 95000000, 'PE_Ratio': 62.5, 'PB_Ratio': 12.4, 'Dividend_Yield': 0.0, 'ROE': 19.3, 'Debt_to_Equity': 0.17, 'EPS': 3.97, 'Revenue_Growth': 18.8, 'Profit_Margin': 8.2},
            {'Symbol': 'NVDA', 'Company': 'NVIDIA Corporation', 'Sector': 'Semiconductors', 'Market_Cap': 1800000, 'Price': 425.60, 'Volume': 38000000, 'PE_Ratio': 65.8, 'PB_Ratio': 55.1, 'Dividend_Yield': 0.1, 'ROE': 83.2, 'Debt_to_Equity': 0.24, 'EPS': 6.47, 'Revenue_Growth': 126.1, 'Profit_Margin': 32.9},
            {'Symbol': 'META', 'Company': 'Meta Platforms Inc', 'Sector': 'Social Media', 'Market_Cap': 850000, 'Price': 325.25, 'Volume': 18000000, 'PE_Ratio': 23.8, 'PB_Ratio': 7.2, 'Dividend_Yield': 0.4, 'ROE': 30.2, 'Debt_to_Equity': 0.12, 'EPS': 13.67, 'Revenue_Growth': 22.1, 'Profit_Margin': 29.1},
            {'Symbol': 'JPM', 'Company': 'JPMorgan Chase & Co', 'Sector': 'Banking', 'Market_Cap': 480000, 'Price': 165.80, 'Volume': 8500000, 'PE_Ratio': 12.4, 'PB_Ratio': 1.8, 'Dividend_Yield': 2.9, 'ROE': 14.5, 'Debt_to_Equity': 1.22, 'EPS': 13.37, 'Revenue_Growth': 22.3, 'Profit_Margin': 32.1},
            {'Symbol': 'V', 'Company': 'Visa Inc', 'Sector': 'Financial Services', 'Market_Cap': 520000, 'Price': 245.90, 'Volume': 6200000, 'PE_Ratio': 31.2, 'PB_Ratio': 13.8, 'Dividend_Yield': 0.8, 'ROE': 44.1, 'Debt_to_Equity': 0.68, 'EPS': 7.88, 'Revenue_Growth': 11.5, 'Profit_Margin': 51.6},
            {'Symbol': 'UNH', 'Company': 'UnitedHealth Group', 'Sector': 'Healthcare', 'Market_Cap': 450000, 'Price': 485.20, 'Volume': 2800000, 'PE_Ratio': 24.1, 'PB_Ratio': 6.2, 'Dividend_Yield': 1.3, 'ROE': 25.7, 'Debt_to_Equity': 0.59, 'EPS': 20.13, 'Revenue_Growth': 14.2, 'Profit_Margin': 6.1}
        ],
        
        'Australia': [
            {'Symbol': 'CBA', 'Company': 'Commonwealth Bank', 'Sector': 'Banking', 'Market_Cap': 180000, 'Price': 108.50, 'Volume': 4200000, 'PE_Ratio': 18.2, 'PB_Ratio': 2.1, 'Dividend_Yield': 4.2, 'ROE': 11.5, 'Debt_to_Equity': 4.8, 'EPS': 5.96, 'Revenue_Growth': 5.8, 'Profit_Margin': 34.2},
            {'Symbol': 'BHP', 'Company': 'BHP Group Limited', 'Sector': 'Mining', 'Market_Cap': 220000, 'Price': 46.80, 'Volume': 8500000, 'PE_Ratio': 12.8, 'PB_Ratio': 2.4, 'Dividend_Yield': 5.8, 'ROE': 18.9, 'Debt_to_Equity': 0.28, 'EPS': 3.66, 'Revenue_Growth': -8.2, 'Profit_Margin': 28.4},
            {'Symbol': 'WBC', 'Company': 'Westpac Banking Corp', 'Sector': 'Banking', 'Market_Cap': 85000, 'Price': 24.60, 'Volume': 12000000, 'PE_Ratio': 15.4, 'PB_Ratio': 1.2, 'Dividend_Yield': 5.2, 'ROE': 7.8, 'Debt_to_Equity': 5.1, 'EPS': 1.60, 'Revenue_Growth': 2.1, 'Profit_Margin': 28.9},
            {'Symbol': 'NAB', 'Company': 'National Australia Bank', 'Sector': 'Banking', 'Market_Cap': 95000, 'Price': 32.40, 'Volume': 8200000, 'PE_Ratio': 16.8, 'PB_Ratio': 1.4, 'Dividend_Yield': 4.8, 'ROE': 8.3, 'Debt_to_Equity': 4.9, 'EPS': 1.93, 'Revenue_Growth': 3.4, 'Profit_Margin': 31.2},
            {'Symbol': 'ANZ', 'Company': 'Australia and New Zealand Banking Group', 'Sector': 'Banking', 'Market_Cap': 78000, 'Price': 26.80, 'Volume': 9500000, 'PE_Ratio': 14.2, 'PB_Ratio': 1.1, 'Dividend_Yield': 5.9, 'ROE': 7.7, 'Debt_to_Equity': 5.3, 'EPS': 1.89, 'Revenue_Growth': 1.8, 'Profit_Margin': 29.6},
            {'Symbol': 'WES', 'Company': 'Wesfarmers Limited', 'Sector': 'Retail', 'Market_Cap': 58000, 'Price': 58.20, 'Volume': 2200000, 'PE_Ratio': 22.8, 'PB_Ratio': 3.8, 'Dividend_Yield': 3.2, 'ROE': 16.7, 'Debt_to_Equity': 0.32, 'EPS': 2.55, 'Revenue_Growth': 6.8, 'Profit_Margin': 4.1},
            {'Symbol': 'MQG', 'Company': 'Macquarie Group Limited', 'Sector': 'Financial Services', 'Market_Cap': 72000, 'Price': 185.40, 'Volume': 1800000, 'PE_Ratio': 15.8, 'PB_Ratio': 1.9, 'Dividend_Yield': 3.1, 'ROE': 12.0, 'Debt_to_Equity': 3.2, 'EPS': 11.73, 'Revenue_Growth': 18.5, 'Profit_Margin': 28.4},
            {'Symbol': 'CSL', 'Company': 'CSL Limited', 'Sector': 'Healthcare', 'Market_Cap': 145000, 'Price': 298.50, 'Volume': 950000, 'PE_Ratio': 35.2, 'PB_Ratio': 5.8, 'Dividend_Yield': 1.2, 'ROE': 16.5, 'Debt_to_Equity': 0.41, 'EPS': 8.48, 'Revenue_Growth': 11.2, 'Profit_Margin': 24.8},
            {'Symbol': 'FMG', 'Company': 'Fortescue Metals Group', 'Sector': 'Mining', 'Market_Cap': 68000, 'Price': 22.15, 'Volume': 15000000, 'PE_Ratio': 8.9, 'PB_Ratio': 1.8, 'Dividend_Yield': 8.2, 'ROE': 20.2, 'Debt_to_Equity': 0.22, 'EPS': 2.49, 'Revenue_Growth': -18.5, 'Profit_Margin': 42.1},
            {'Symbol': 'WOW', 'Company': 'Woolworths Group Limited', 'Sector': 'Retail', 'Market_Cap': 45000, 'Price': 36.80, 'Volume': 3500000, 'PE_Ratio': 26.1, 'PB_Ratio': 4.2, 'Dividend_Yield': 2.8, 'ROE': 16.1, 'Debt_to_Equity': 0.58, 'EPS': 1.41, 'Revenue_Growth': 4.2, 'Profit_Margin': 2.8}
        ]
    }
    
    # Create comprehensive DataFrame
    all_data = []
    for country, stocks in stocks_data.items():
        for stock in stocks:
            stock['Country'] = country
            # Add technical indicators
            stock['RSI'] = round(random.uniform(30, 70), 1)
            stock['50DMA'] = round(stock['Price'] * random.uniform(0.92, 1.08), 2)
            stock['200DMA'] = round(stock['Price'] * random.uniform(0.85, 1.15), 2)
            stock['MACD'] = round(random.uniform(-5, 5), 2)
            stock['Beta'] = round(random.uniform(0.5, 2.0), 2)
            
            # Add risk metrics
            stock['Volatility'] = round(random.uniform(15, 45), 1)
            stock['Sharpe_Ratio'] = round(random.uniform(0.5, 2.5), 2)
            
            # Add recommendation
            pe_score = 5 if stock['PE_Ratio'] < 15 else 3 if stock['PE_Ratio'] < 25 else 1
            roe_score = 5 if stock['ROE'] > 20 else 3 if stock['ROE'] > 15 else 1
            growth_score = 5 if stock['Revenue_Growth'] > 15 else 3 if stock['Revenue_Growth'] > 10 else 1
            
            total_score = pe_score + roe_score + growth_score
            if total_score >= 12:
                stock['Recommendation'] = 'Strong Buy'
            elif total_score >= 9:
                stock['Recommendation'] = 'Buy'
            elif total_score >= 6:
                stock['Recommendation'] = 'Hold'
            else:
                stock['Recommendation'] = 'Sell'
                
            # Add last updated
            stock['Last_Updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            all_data.append(stock)
    
    return pd.DataFrame(all_data)

if __name__ == "__main__":
    # Create the sample data
    df = create_sample_stock_data()
    
    # Save to Excel file
    with pd.ExcelWriter('/Users/anandvardhan/xTrade/stock_market_data.xlsx', engine='openpyxl') as writer:
        # Save all data
        df.to_excel(writer, sheet_name='All_Stocks', index=False)
        
        # Save by country
        for country in ['India', 'USA', 'Australia']:
            country_data = df[df['Country'] == country]
            country_data.to_excel(writer, sheet_name=f'{country}_Stocks', index=False)
        
        # Save by sector
        sectors = df['Sector'].unique()
        for sector in sectors:
            sector_data = df[df['Sector'] == sector]
            if len(sector_data) > 0:
                sheet_name = sector.replace(' ', '_').replace('&', 'and')[:31]  # Excel sheet name limit
                sector_data.to_excel(writer, sheet_name=f'{sheet_name}_Stocks', index=False)
    
    print("Sample stock market data created successfully!")
    print(f"Total stocks: {len(df)}")
    print(f"Countries: {df['Country'].unique()}")
    print(f"Sectors: {df['Sector'].unique()}")
    print("File saved as: stock_market_data.xlsx")
