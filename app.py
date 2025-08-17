import streamlit as st
import pandas as pd
from main import get_copilot_suggested_stocks, fetch_stock_data

st.set_page_config(page_title="xTradeStockAI Mobile Simulator", layout="centered")
st.title("📱 xTradeStockAI - Mobile App Simulator")


# Enhanced UI for prompt selection





# Country selection as single select dropdown
country_options = {
    "India": "🇮🇳 India",
    "USA": "🇺🇸 USA",
    "Australia": "🇦🇺 Australia"
}
country_names = list(country_options.keys())
selected_country = st.selectbox(
    "Select country:",
    options=country_names,
    format_func=lambda x: country_options[x]
)


# Technical/Fundamental selection as buttons
col1, col2, col3 = st.columns(3)
suggestion_type = None
if col1.button("Technical"):
    suggestion_type = "technical"
if col2.button("Fundamental"):
    suggestion_type = "fundamental"
if col3.button("Both"):
    suggestion_type = "both"

num_stocks = st.number_input("How many top stocks do you want to see?", min_value=1, max_value=50, value=10)

# Prompt button to show suggestions
if st.button("Show Suggestions") and suggestion_type and selected_country:
    prompt = f"Top {num_stocks} stocks for {selected_country} based on {suggestion_type} indicators"
    st.subheader(f"Copilot-suggested stocks for {country_options[selected_country]} ({suggestion_type})")
    stocks = get_copilot_suggested_stocks(prompt, selected_country)[:num_stocks]
    data_list = []
    exchange = "NSE" if selected_country == "India" else ("NASDAQ" if selected_country == "USA" else ("ASX" if selected_country == "Australia" else "Unknown"))
    for symbol in stocks:
        data = fetch_stock_data(symbol, selected_country)
        data['Exchange'] = exchange
        data_list.append(data)
    df = pd.DataFrame(data_list)
    st.dataframe(df)
    st.download_button("Download CSV", df.to_csv(index=False), f"copilot_suggested_stocks_{selected_country}.csv", "text/csv")

st.info("This is a mobile app simulator. For best experience, open in mobile browser or resize your window.")
