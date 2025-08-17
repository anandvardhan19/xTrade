import streamlit as st
import pandas as pd
from main import get_copilot_suggested_stocks, fetch_stock_data

st.set_page_config(page_title="xTradeStockAI Mobile Simulator", layout="centered")
st.title("📱 xTradeStockAI - Mobile App Simulator")


# Enhanced UI for prompt selection

country = st.selectbox("Select country:", ["India", "USA", "Australia"])
suggestion_type = st.selectbox("Select stock suggestion type:", ["technical", "fundamental", "both"])
num_stocks = st.number_input("How many top stocks do you want to see?", min_value=1, max_value=50, value=10)

prompt = f"Top {num_stocks} stocks for {country} based on {suggestion_type} indicators"
suggestion_btn_label = f"Suggest for {country} ({suggestion_type})"

if st.button(suggestion_btn_label):
    st.subheader(f"Copilot-suggested stocks for {country} ({prompt})")
    stocks = get_copilot_suggested_stocks(prompt, country)[:num_stocks]
    data_list = []
    for symbol in stocks:
        if country == "India":
            exchange = "NSE"
        elif country == "USA":
            exchange = "NASDAQ"
        elif country == "Australia":
            exchange = "ASX"
        else:
            exchange = "Unknown"
        data = fetch_stock_data(symbol, country)
        data['Exchange'] = exchange
        data_list.append(data)
    df = pd.DataFrame(data_list)
    st.dataframe(df)
    st.download_button("Download CSV", df.to_csv(index=False), f"copilot_suggested_stocks_{country}.csv", "text/csv")

st.info("This is a mobile app simulator. For best experience, open in mobile browser or resize your window.")
