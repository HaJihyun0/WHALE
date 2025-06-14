folium
streamlit_folium

# global_top10_stocks.py
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime, timedelta

st.set_page_config(page_title="글로벌 시가총액 TOP10 주가 변화", layout="wide")

top10_tickers = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Saudi Aramco": "2222.SR",
    "NVIDIA": "NVDA",
    "Alphabet (Google)": "GOOGL",
    "Amazon": "AMZN",
    "Meta (Facebook)": "META",
    "Berkshire Hathaway": "BRK-B",
    "TSMC": "TSM",
    "Eli Lilly": "LLY"
}

end_date = datetime.today()
start_date = end_date - timedelta(days=365)

st.title("📊 글로벌 시가총액 TOP10 기업의 최근 1년 주가 변화")
st.markdown("데이터 출처: [Yahoo Finance](https://finance.yahoo.com)")

selected_companies = st.multiselect("기업을 선택하세요", options=top10_tickers.keys(), default=list(top10_tickers.keys())[:5])

if selected_companies:
    fig = go.Figure()

    for company in selected_companies:
        ticker = top10_tickers[company]
        data = yf.download(ticker, start=start_date, end=end_date)
        if not data.empty:
            fig.add_trace(go.Scatter(x=data.index, y=data['Adj Close'], mode='lines', name=company))

    fig.update_layout(title="최근 1년간 주가 변화 (조정 종가 기준)",
                      xaxis_title="날짜",
                      yaxis_title="주가 (USD)",
                      template="plotly_dark",
                      height=600)

    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("하나 이상의 기업을 선택하세요.")

streamlit
yfinance
pandas
plotly
