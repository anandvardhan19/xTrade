import gradio as gr
import pandas as pd
from main import get_copilot_suggested_stocks, fetch_stock_data

def get_stock_suggestions(country, suggestion_type, num_stocks):
    """Get stock suggestions and data"""
    prompt = f"Top {num_stocks} stocks for {country} based on {suggestion_type} indicators"
    stocks = get_copilot_suggested_stocks(prompt, country)[:num_stocks]
    
    if not stocks:
        return "No stock suggestions available.", None
    
    country_data = []
    for symbol in stocks:
        data = fetch_stock_data(symbol, country)
        country_data.append(data)
    
    df = pd.DataFrame(country_data)
    
    # Format the results for display
    result_text = f"AI-suggested stocks for {country} ({suggestion_type} analysis):\n\n"
    for _, row in df.iterrows():
        result_text += f"🏢 {row['Symbol']}: "
        result_text += f"💰 ${row['Price']:.2f}" if row['Price'] else "💰 N/A"
        result_text += f" | 📊 Volume: {row['Volume']:,}" if row['Volume'] else " | 📊 Volume: N/A"
        result_text += f" | 📈 PE: {row['PE Ratio']:.1f}" if row['PE Ratio'] else " | 📈 PE: N/A"
        result_text += "\n"
    
    return result_text, df

# Create Gradio interface
with gr.Blocks(title="🚀 xTradeStockAI", theme=gr.themes.Soft()) as app:
    gr.Markdown(
        """
        # 🚀 xTradeStockAI
        ## AI-Powered Stock Suggestions for India, USA & Australia
        
        Get intelligent stock recommendations based on technical and fundamental analysis!
        """
    )
    
    with gr.Row():
        with gr.Column(scale=1):
            country = gr.Dropdown(
                choices=["India", "USA", "Australia"],
                label="🌍 Select Country",
                value="India"
            )
            
            suggestion_type = gr.Radio(
                choices=["technical", "fundamental", "both"],
                label="📊 Analysis Type",
                value="both"
            )
            
            num_stocks = gr.Slider(
                minimum=1,
                maximum=20,
                value=10,
                step=1,
                label="🔢 Number of Stocks"
            )
            
            submit_btn = gr.Button("🎯 Get Stock Suggestions", variant="primary")
        
        with gr.Column(scale=2):
            result_text = gr.Textbox(
                label="📋 Results",
                lines=15,
                max_lines=20
            )
            
            result_table = gr.Dataframe(
                label="📊 Detailed Data",
                interactive=False
            )
    
    # Event handler
    submit_btn.click(
        fn=get_stock_suggestions,
        inputs=[country, suggestion_type, num_stocks],
        outputs=[result_text, result_table]
    )
    
    gr.Markdown(
        """
        ### 💡 Features:
        - 🤖 AI-powered stock suggestions using OpenAI (with fallback data)
        - 🌏 Support for India, USA, and Australia markets
        - 📈 Real-time data from Yahoo Finance and NSE
        - 📊 Technical and fundamental analysis options
        - 💾 Downloadable results
        
        ### 🔧 Tech Stack:
        - **Frontend**: Gradio (Latest & Simplest)
        - **Backend**: Python + OpenAI API
        - **Data**: yfinance, nsetools
        """
    )

if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True  # Creates public shareable link
    )
