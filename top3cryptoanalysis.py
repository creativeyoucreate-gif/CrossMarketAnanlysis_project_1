import mysql.connector
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

def run():
    st.title("🟡 Top 3 Crypto Analysis")
    
    @st.cache_resource(ttl=3600)
    def get_connection():
        return mysql.connector.connect(
            host="localhost", user="root", password="KAvi", 
            database="cross_market_analysis_db", autocommit=True
        )
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Sidebar dates
    with st.sidebar:
        col1, col2 = st.columns(2)
        start_date = col1.date_input("Start Date", datetime.now().date() - timedelta(days=30)).strftime('%Y-%m-%d')
        end_date = col2.date_input("End Date", datetime.now().date()).strftime('%Y-%m-%d')
        st.info(f"🔍 Date Range: {start_date} → {end_date}")
    
    # Row counts
    col1, col2 = st.columns(2)
    cursor.execute("SELECT COUNT(*) FROM cryptocurrencies")
    col1.metric("cryptocurrencies", cursor.fetchone()[0])
    cursor.execute("SELECT COUNT(*) FROM `Crypto_coin_prices`")
    col2.metric("Crypto_coin_prices", cursor.fetchone()[0])
    
    # 1. Top 3 cryptos by market_cap
    cursor.execute("""
        SELECT id, name, symbol, market_cap 
        FROM cryptocurrencies 
        ORDER BY market_cap DESC LIMIT 3
    """)
    top_data = cursor.fetchall()
    top_df = pd.DataFrame(top_data, columns=['coin_id', 'name', 'symbol', 'market_cap'])
    
    col1, col2 = st.columns([1,3])
    with col1: st.subheader("📊 Top 3")
    with col2:
        if not top_df.empty:
            st.dataframe(top_df[['name', 'symbol']], use_container_width=True, hide_index=True)
            top_coin_ids = top_df['coin_id'].tolist()
            st.info(f"**Coin IDs**: {top_coin_ids}")
        else:
            st.error("❌ No crypto data")
            cursor.close()
            return
    
    # 2. Crypto prices with JOIN (FIXED)
    placeholders = ','.join([f"'{cid}'" for cid in top_coin_ids])  # VARCHAR quotes
    cursor.execute(f"""
        SELECT cpp.date, cpp.price, c.name, c.symbol
        FROM `Crypto_coin_prices` cpp
        JOIN cryptocurrencies c ON cpp.coin_id = c.id
        WHERE cpp.coin_id IN ({placeholders})
        AND cpp.date BETWEEN '{start_date}' AND '{end_date}'
        ORDER BY cpp.coin_id, cpp.date
    """)
    prices_data = cursor.fetchall()
    prices_df = pd.DataFrame(prices_data, columns=['date', 'price', 'name', 'symbol'])
    
    col1.metric("📈 Crypto Records", len(prices_df))
    
    if not prices_df.empty:
        # Charts for each coin
        for _, row in top_df.iterrows():
            coin_name = row['name']
            coin_df = prices_df[prices_df['name'] == coin_name].copy()
            if not coin_df.empty:
                st.subheader(f"📈 {coin_name} ({row['symbol']}) Price Trend")
                coin_df['date'] = pd.to_datetime(coin_df['date'])
                fig = px.line(coin_df, x='date', y='price', title=f"{coin_name} Price",
                            labels={'price': 'Price (USD)', 'date': 'Date'})
                fig.update_layout(height=350, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
    
    # 3. Date-filtered tabs
    tab1, tab2, tab3 = st.tabs(["💰 Crypto Prices", "📈 Stocks", "🛢️ Oil"])
    
    with tab1:
        if not prices_df.empty:
            st.dataframe(prices_df, use_container_width=True)
        else:
            st.info("No crypto prices in selected date range")
    
    with tab2:
        cursor.execute(f"""
            SELECT * FROM Stock_prices_history 
            WHERE date BETWEEN '{start_date}' AND '{end_date}'
            ORDER BY date DESC, ticker
        """)
        stock_data = cursor.fetchall()
        if stock_data:
            cursor.execute("DESCRIBE Stock_prices_history")
            cols = [row[0] for row in cursor.fetchall()]
            st.dataframe(pd.DataFrame(stock_data, columns=cols), use_container_width=True)
    
    with tab3:
        cursor.execute(f"""
            SELECT * FROM Oil_prices_history 
            WHERE date BETWEEN '{start_date}' AND '{end_date}'
            ORDER BY date DESC
        """)
        oil_data = cursor.fetchall()
        if oil_data:
            cursor.execute("DESCRIBE Oil_prices_history")
            cols = [row[0] for row in cursor.fetchall()]
            st.dataframe(pd.DataFrame(oil_data, columns=cols), use_container_width=True)
    
    cursor.close()
