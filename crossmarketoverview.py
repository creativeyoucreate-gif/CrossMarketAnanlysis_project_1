import streamlit as st
import pandas as pd
import mysql.connector

def run():

    # ---- Database Connection ----
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="KAvi",
        database="cross_market_analysis_db"
    )

    cursor = conn.cursor()

    st.title("📊 Cross Market Overview")
    st.caption("Crypto • Oil • Stock Market Analysis")

    # ---- Date Filters ----
    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input("Start Date")

    with col2:
        end_date = st.date_input("End Date")

    if start_date > end_date:
        st.error("Start date must be before End date")
        return

    # ---- SQL Query ----
    query = """
    SELECT 
        cp.date,
        cp.price AS bitcoin_price,
        o.price AS oil_price,
        sp.close AS sp500,
        nf.close AS NASDAQ
    FROM Crypto_coin_prices cp

    JOIN cryptocurrencies c 
        ON cp.coin_id = c.id

    LEFT JOIN Oil_prices_history o 
        ON cp.date = o.date

    LEFT JOIN Stock_prices_history sp 
        ON cp.date = sp.date AND sp.ticker = '^GSPC'

    LEFT JOIN Stock_prices_history nf 
        ON cp.date = nf.date AND nf.ticker = '^IXIC'

    WHERE c.symbol = 'btc'
    AND cp.date BETWEEN %s AND %s

    ORDER BY cp.date;
    """

    cursor.execute(query, (start_date, end_date))
    results = cursor.fetchall()

    if not results:
        st.warning("No data available for selected date range.")
        return

    # ---- Convert to DataFrame ----
    columns = ["Date", "Bitcoin Price", "Oil Price", "S&P 500", "NASDAQ"]
    df = pd.DataFrame(results, columns=columns)

    st.divider()

    # ---- KPI Section ----
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("₿ Bitcoin Avg ($)", f"{df['Bitcoin Price'].mean():,.2f}")

    with col2:
        st.metric("🛢 Oil Avg ($)", f"{df['Oil Price'].mean():,.2f}")

    with col3:
        st.metric("📈 S&P 500 Avg", f"{df['S&P 500'].mean():,.2f}")

    with col4:
        st.metric("📊 NASDAQ Avg", f"{df['NASDAQ'].mean():,.2f}")

    st.divider()

    # ---- Daily Snapshot Table ----
    st.subheader("📋 Daily Market Snapshot")
    st.dataframe(df, use_container_width=True)

    # ---- Limit Data (Last 60 Days) ----
    df = df.tail(60)

    # ---- Trend Charts ----
    st.subheader("📈 Market % Change")

    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")

    # Filter by selected date range
    df = df[(df["Date"] >= pd.to_datetime(start_date)) & 
            (df["Date"] <= pd.to_datetime(end_date))]

    # Convert columns to numeric
    cols = ["Bitcoin Price", "Oil Price", "S&P 500", "NASDAQ"]

    for col in cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.fillna(method="ffill")

    pct_df = df.set_index("Date")[cols].pct_change() * 100
    pct_df = pct_df.dropna()

    if pct_df.empty:
        st.warning("No data available for selected date range.")
    else:
        st.line_chart(pct_df)




