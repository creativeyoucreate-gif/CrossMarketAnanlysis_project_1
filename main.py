import streamlit as st
import mysql.connector
import pandas as pd

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="KAvi",
    database="CMADB"
)
# st.write("Connected to the database successfully!")
cursor = conn.cursor()


import streamlit as st

# Create layout with columns
col1, col2, col3 = st.columns([1, 2, 1])

# Place image in the rightmost column
with col3:
    st.image("C:/Users/hemhe/Documents/GUVIproject/project1/CPYoUJqK-hcl-guvi.webp", width=200)

import streamlit as st

st.markdown(
    "<h1 style='text-align: center; color: #2E86C1;'>Cross Market Analysis</h1>",
    unsafe_allow_html=True
)

option = st.selectbox (
    "SQL Query Runner: Select a query to run", (
     "1. Find the top 3 cryptocurrencies by market cap.",
     "2. List all coins where circulating supply exceeds 90% of total supply.",
     "3. Get coins that are within 10% of their all-time-high (ATH)."
     
     
     
     
     
     
     
     
     
     
     
     
     )
)

if option == "1. Find the top 3 cryptocurrencies by market cap.":
    query = "SELECT name, market_cap FROM cryptocurrencies ORDER BY market_cap DESC LIMIT 3;"
    cursor.execute(query)
    results = cursor.fetchall()
    st.write("Top 3 Cryptocurrencies by Market Cap:")
    df = pd.DataFrame(results, columns=["Name", "Market Cap"])  
    df.index = range(1, len(df) + 1)
    st.write(df)

elif option == "2. List all coins where circulating supply exceeds 90% of total supply.":
    query = """
    SELECT name, circulating_supply, total_supply 
    FROM cryptocurrencies 
    WHERE circulating_supply > 0.9 * total_supply;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    
    st.write("Coins where Circulating Supply exceeds 90% of Total Supply:")
    
    df = pd.DataFrame(results, columns=["Name", "Circulating Supply", "Total Supply"])  
    df.index = range(1, len(df) + 1)
    st.write(df)

elif option == "3. Get coins that are within 10% of their all-time-high (ATH).":
    query = """
        SELECT name, current_price, ath
        FROM cryptocurrencies
        WHERE current_price BETWEEN 0.9 * ath AND 1.1 * ath;
    """
    cursor.execute(query)
    results = cursor.fetchall()

    st.write("Coins within 10% of their All-Time-High (ATH):")

    df = pd.DataFrame(results, columns=["Name", "Current Price", "ATH Price"])
    df.index = range(1, len(df) + 1)
    st.write(df)