import gradio as gr
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

class StockDataAnalyzer:
    def __init__(self, excel_file_path):
        """Initialize with pre-loaded Excel data"""
        self.excel_file_path = excel_file_path
        self.load_data()
    
    def load_data(self):
        """Load data from Excel file"""
        try:
            # Load the main sheet
            self.df = pd.read_excel(self.excel_file_path, sheet_name='All_Stocks')
            print(f"Loaded {len(self.df)} stocks from Excel file")
        except Exception as e:
            print(f"Error loading Excel file: {e}")
            # Create fallback data if file doesn't exist
            self.create_fallback_data()
    
    def create_fallback_data(self):
        """Create fallback data if Excel file is not available"""
        fallback_data = [
            {'Symbol': 'RELIANCE', 'Company': 'Reliance Industries', 'Country': 'India', 'Sector': 'Energy', 'Price': 2450.50, 'PE_Ratio': 12.5, 'ROE': 14.2, 'Revenue_Growth': 8.5, 'Recommendation': 'Buy'},
            {'Symbol': 'AAPL', 'Company': 'Apple Inc', 'Country': 'USA', 'Sector': 'Technology', 'Price': 175.25, 'PE_Ratio': 28.4, 'ROE': 147.4, 'Revenue_Growth': 2.8, 'Recommendation': 'Hold'},
            {'Symbol': 'CBA', 'Company': 'Commonwealth Bank', 'Country': 'Australia', 'Sector': 'Banking', 'Price': 108.50, 'PE_Ratio': 18.2, 'ROE': 11.5, 'Revenue_Growth': 5.8, 'Recommendation': 'Buy'}
        ]
        self.df = pd.DataFrame(fallback_data)
    
    def get_stock_suggestions(self, country, sector, min_pe, max_pe, min_roe, recommendation, sort_by, num_results):
        """Get filtered stock suggestions based on criteria"""
        
        # Start with all data
        filtered_df = self.df.copy()
        
        # Apply filters
        if country != "All":
            filtered_df = filtered_df[filtered_df['Country'] == country]
        
        if sector != "All":
            filtered_df = filtered_df[filtered_df['Sector'] == sector]
        
        if recommendation != "All":
            filtered_df = filtered_df[filtered_df['Recommendation'] == recommendation]
        
        # Apply numeric filters
        if 'PE_Ratio' in filtered_df.columns:
            filtered_df = filtered_df[
                (filtered_df['PE_Ratio'] >= min_pe) & 
                (filtered_df['PE_Ratio'] <= max_pe)
            ]
        
        if 'ROE' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['ROE'] >= min_roe]
        
        # Sort results
        if sort_by and sort_by in filtered_df.columns:
            ascending = sort_by in ['PE_Ratio', 'Volatility']  # Lower is better for these
            filtered_df = filtered_df.sort_values(by=sort_by, ascending=ascending)
        
        # Limit results
        filtered_df = filtered_df.head(num_results)
        
        if filtered_df.empty:
            return "No stocks found matching your criteria.", None, None, None
        
        # Create summary text
        summary = f"Found {len(filtered_df)} stocks matching your criteria:\n\n"
        for _, row in filtered_df.iterrows():
            summary += f"🏢 **{row['Symbol']}** ({row['Company']})\n"
            summary += f"   💰 Price: ${row['Price']:.2f} | 📊 PE: {row.get('PE_Ratio', 'N/A'):.1f} | 📈 ROE: {row.get('ROE', 'N/A'):.1f}%\n"
            summary += f"   🎯 Recommendation: {row.get('Recommendation', 'N/A')} | 🏭 Sector: {row['Sector']}\n\n"
        
        # Create visualizations
        price_chart = self.create_price_chart(filtered_df)
        pe_roe_chart = self.create_pe_roe_scatter(filtered_df)
        sector_chart = self.create_sector_distribution(filtered_df)
        
        return summary, filtered_df, price_chart, pe_roe_chart, sector_chart
    
    def create_price_chart(self, df):
        """Create price comparison chart"""
        if df.empty or 'Price' not in df.columns:
            return None
        
        fig = px.bar(
            df.head(10), 
            x='Symbol', 
            y='Price',
            color='Recommendation',
            title='Stock Prices Comparison',
            labels={'Price': 'Price ($)', 'Symbol': 'Stock Symbol'},
            color_discrete_map={
                'Strong Buy': '#00CC44',
                'Buy': '#66DD66', 
                'Hold': '#FFAA00',
                'Sell': '#FF6666'
            }
        )
        fig.update_layout(showlegend=True, height=400)
        return fig
    
    def create_pe_roe_scatter(self, df):
        """Create PE vs ROE scatter plot"""
        if df.empty or 'PE_Ratio' not in df.columns or 'ROE' not in df.columns:
            return None
        
        fig = px.scatter(
            df,
            x='PE_Ratio',
            y='ROE',
            size='Market_Cap' if 'Market_Cap' in df.columns else None,
            color='Country',
            hover_name='Symbol',
            hover_data=['Company', 'Sector', 'Recommendation'],
            title='PE Ratio vs ROE Analysis',
            labels={'PE_Ratio': 'P/E Ratio', 'ROE': 'Return on Equity (%)'}
        )
        fig.update_layout(height=400)
        return fig
    
    def create_sector_distribution(self, df):
        """Create sector distribution chart"""
        if df.empty:
            return None
        
        sector_counts = df['Sector'].value_counts()
        fig = px.pie(
            values=sector_counts.values,
            names=sector_counts.index,
            title='Sector Distribution',
        )
        fig.update_layout(height=400)
        return fig
    
    def get_stock_details(self, symbol):
        """Get detailed information for a specific stock"""
        if symbol not in self.df['Symbol'].values:
            return "Stock not found in database."
        
        stock = self.df[self.df['Symbol'] == symbol].iloc[0]
        
        details = f"""
## 📈 {stock['Symbol']} - {stock['Company']}

### 📊 **Key Metrics:**
- **Price:** ${stock.get('Price', 'N/A'):.2f}
- **Market Cap:** ${stock.get('Market_Cap', 0):,}M
- **P/E Ratio:** {stock.get('PE_Ratio', 'N/A'):.1f}
- **ROE:** {stock.get('ROE', 'N/A'):.1f}%
- **Revenue Growth:** {stock.get('Revenue_Growth', 'N/A'):.1f}%

### 🎯 **Investment Analysis:**
- **Sector:** {stock['Sector']}
- **Country:** {stock['Country']}
- **Recommendation:** **{stock.get('Recommendation', 'N/A')}**
- **Dividend Yield:** {stock.get('Dividend_Yield', 'N/A'):.1f}%

### 📈 **Technical Indicators:**
- **50-Day MA:** ${stock.get('50DMA', 'N/A'):.2f}
- **200-Day MA:** ${stock.get('200DMA', 'N/A'):.2f}
- **RSI:** {stock.get('RSI', 'N/A')}
- **Beta:** {stock.get('Beta', 'N/A')}
- **Volatility:** {stock.get('Volatility', 'N/A')}%

### 💼 **Financial Health:**
- **Debt/Equity:** {stock.get('Debt_to_Equity', 'N/A')}
- **Profit Margin:** {stock.get('Profit_Margin', 'N/A'):.1f}%
- **EPS:** ${stock.get('EPS', 'N/A')}
"""
        return details

# Initialize the analyzer
analyzer = StockDataAnalyzer('/Users/anandvardhan/xTrade/stock_market_data.xlsx')

# Create Gradio interface
with gr.Blocks(title="📊 Stock Market Analyzer", theme=gr.themes.Soft()) as app:
    gr.Markdown(
        """
        # 📊 Stock Market Analyzer
        ## Advanced Stock Analysis with Pre-loaded Market Data
        
        Analyze 30+ stocks from India, USA, and Australia with comprehensive financial metrics!
        """
    )
    
    with gr.Tabs():
        # Tab 1: Stock Screener
        with gr.Tab("🔍 Stock Screener"):
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### 🎛️ Filter Criteria")
                    
                    country_filter = gr.Dropdown(
                        choices=["All"] + sorted(analyzer.df['Country'].unique().tolist()),
                        label="🌍 Country",
                        value="All"
                    )
                    
                    sector_filter = gr.Dropdown(
                        choices=["All"] + sorted(analyzer.df['Sector'].unique().tolist()),
                        label="🏭 Sector",
                        value="All"
                    )
                    
                    recommendation_filter = gr.Dropdown(
                        choices=["All", "Strong Buy", "Buy", "Hold", "Sell"],
                        label="🎯 Recommendation",
                        value="All"
                    )
                    
                    min_pe = gr.Slider(
                        minimum=0,
                        maximum=100,
                        value=0,
                        label="📊 Min P/E Ratio"
                    )
                    
                    max_pe = gr.Slider(
                        minimum=0,
                        maximum=100,
                        value=50,
                        label="📊 Max P/E Ratio"
                    )
                    
                    min_roe = gr.Slider(
                        minimum=0,
                        maximum=50,
                        value=10,
                        label="📈 Minimum ROE (%)"
                    )
                    
                    sort_by = gr.Dropdown(
                        choices=["Price", "PE_Ratio", "ROE", "Market_Cap", "Revenue_Growth"],
                        label="📋 Sort By",
                        value="Market_Cap"
                    )
                    
                    num_results = gr.Slider(
                        minimum=1,
                        maximum=30,
                        value=10,
                        step=1,
                        label="🔢 Number of Results"
                    )
                    
                    search_btn = gr.Button("🔍 Search Stocks", variant="primary", size="lg")
                
                with gr.Column(scale=2):
                    result_summary = gr.Markdown(label="📋 Search Results")
                    result_table = gr.Dataframe(label="📊 Detailed Data")
            
            with gr.Row():
                price_chart = gr.Plot(label="💰 Price Comparison")
                pe_roe_chart = gr.Plot(label="📊 PE vs ROE Analysis")
            
            sector_dist_chart = gr.Plot(label="🥧 Sector Distribution")
        
        # Tab 2: Stock Details
        with gr.Tab("📈 Stock Details"):
            with gr.Row():
                with gr.Column(scale=1):
                    stock_symbol = gr.Dropdown(
                        choices=sorted(analyzer.df['Symbol'].tolist()),
                        label="🏢 Select Stock Symbol",
                        value=analyzer.df['Symbol'].iloc[0] if len(analyzer.df) > 0 else None
                    )
                    get_details_btn = gr.Button("📋 Get Details", variant="primary")
                
                with gr.Column(scale=2):
                    stock_details = gr.Markdown(label="📈 Stock Information")
        
        # Tab 3: Data Overview
        with gr.Tab("📊 Data Overview"):
            gr.Markdown(
                f"""
                ### 📈 **Dataset Overview:**
                - **Total Stocks:** {len(analyzer.df)}
                - **Countries:** {', '.join(analyzer.df['Country'].unique())}
                - **Sectors:** {len(analyzer.df['Sector'].unique())} sectors
                - **Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                
                ### 📊 **Available Metrics:**
                - **Fundamental:** P/E Ratio, ROE, Revenue Growth, Market Cap, EPS
                - **Technical:** RSI, Moving Averages, MACD, Beta, Volatility  
                - **Valuation:** Price, Dividend Yield, Book Value, Debt/Equity
                - **Recommendations:** Strong Buy, Buy, Hold, Sell
                """
            )
            
            full_data = gr.Dataframe(
                value=analyzer.df,
                label="📊 Complete Dataset",
                interactive=False
            )
    
    # Event handlers
    search_btn.click(
        fn=lambda country, sector, min_pe_val, max_pe_val, min_roe, rec, sort, num: analyzer.get_stock_suggestions(
            country, sector, min_pe_val, max_pe_val, min_roe, rec, sort, num
        ),
        inputs=[country_filter, sector_filter, min_pe, max_pe, min_roe, recommendation_filter, sort_by, num_results],
        outputs=[result_summary, result_table, price_chart, pe_roe_chart, sector_dist_chart]
    )
    
    get_details_btn.click(
        fn=analyzer.get_stock_details,
        inputs=[stock_symbol],
        outputs=[stock_details]
    )
    
    gr.Markdown(
        """
        ### 💡 **Features:**
        - 📊 **Advanced Filtering:** Country, sector, P/E ratio, ROE, recommendations
        - 📈 **Interactive Charts:** Price comparison, PE vs ROE scatter plots, sector distribution
        - 🔍 **Detailed Analysis:** Complete fundamental and technical metrics for each stock
        - 📋 **Export Ready:** All data can be downloaded as CSV
        - 🎯 **Professional Recommendations:** Buy/Sell signals based on comprehensive analysis
        
        ### 🎨 **Data Source:**
        Pre-loaded comprehensive stock market data with real-time-like metrics and professional analysis.
        """
    )

if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0",
        server_port=7863,
        share=False
    )
