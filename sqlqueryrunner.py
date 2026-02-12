import mysql.connector
import streamlit as st
import pandas as pd



def run():
     
    conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="KAvi",
    database="cross_market_analysis_db"
    )
    # st.write("Connected to the database successfully!")
    cursor = conn.cursor()

    st.markdown(
        "<h1 style='text-align: center; color: green;'>Cross Market Analysis</h1>",
        unsafe_allow_html=True
    )



    option = st.selectbox(    
        "SQL Query Runner:", 
        
        (
        
        "-- Select an option --",
        "1. Find the top 3 cryptocurrencies by market cap.",
        "2. List all coins where circulating supply exceeds 90% of total supply.",
        "3. Get coins that are within 10% of their all-time-high (ATH).",
        "4. Find the average market cap rank of coins with volume above $1B.",    
        "5. Get the most recently updated coin.",
        "6. Find the highest daily price of Bitcoin in the last 365 days.",     
        "7. Calculate the average daily price of Ethereum in the past 1 year.",
        "8. Show the daily price trend of Bitcoin in February 2025.",
        "9. Find the coin with the highest average price over 1 year." ,
        "10. Get the % change in Bitcoin's price between Feb 2025 and Feb 2026.",
        "11. Find the highest oil price in the last 5 years.",
        "12. Get the average oil price per year",
        "13. Show oil prices during COVID crash (March to April 2020).",
        "14. Find the lowest price of oil in the last 10 years.",
        "15. Calculate the volatility of oil prices (max-min difference per year).",
        "16. Get all stock prices for a given ticker",
        "17. Find the highest closing price for NASDAQ (^IXIC)",
        "18. List top 5 days with highest price difference (high - low) for S&P 500 (^GSPC)",
        "19. Get monthly average closing price for each ticker",
        "20. Get average trading volume of given ticker in 2024",
        "21. Compare Bitcoin vs Oil average price in 2025.",   
        "22. Check if Bitcoin moves with S&P 500 (correlation idea).",
        "23. Compare Ethereum and NASDAQ daily prices for 2025.",
        "24. Find days when oil price spiked and compare with Bitcoin price change.",
        "25. Compare top 3 coins daily price trend vs (^DJI, ^GSPC,^IXIC).",
        "26. Compare stock prices (^GSPC) with crude oil prices on the same dates",
        "27. Correlate Bitcoin closing price with crude oil closing price (same date)",
        "28. Compare NASDAQ (^IXIC) with Ethereum price trends.",
        "29. Join top 3 crypto coins with stock indices for 2025.",
        "30. Multi-join: stock prices, oil prices, and Bitcoin prices for daily comparison"
        )
            )
    
    if option == "-- Select an option --":
        st.write("Please choose a query from the dropdown.")

    elif option == "1. Find the top 3 cryptocurrencies by market cap.":
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

    elif option == "4. Find the average market cap rank of coins with volume above $1B.":
        query = """
            SELECT AVG(market_cap_rank) AS avg_rank
            FROM cryptocurrencies
            WHERE total_volume > 1000000000;
        """
        cursor.execute(query)
        result = cursor.fetchone()

        st.write("Average Market Cap Rank of Coins with Volume above $1B:")
        st.write(f"Average Rank: {result[0]:.2f}")

    elif option == "5. Get the most recently updated coin.":
        query = """
            SELECT name, date
            FROM cryptocurrencies
            ORDER BY date DESC
            LIMIT 1;
        """
        cursor.execute(query)
        result = cursor.fetchone()

        st.write("Most Recently Updated Coin:")
        st.write(f"Name: {result[0]}")
        st.write(f"Last Updated: {result[1]}")

    elif option == "6. Find the highest daily price of Bitcoin in the last 365 days.":  
        query = """
            SELECT MAX(price) AS highest_daily_price
            FROM crypto_coin_prices
            WHERE coin_id = 'bitcoin' AND date >= CURDATE() - INTERVAL 365 DAY;
        """
        cursor.execute(query)
        result = cursor.fetchone()

        st.write("Highest Daily Price of Bitcoin in the Last 365 Days:")
        st.write(f"Highest Daily Price: ₹ {result[0]:.2f}")

    elif option == "7. Calculate the average daily price of Ethereum in the past 1 year.":
        query = """
            SELECT AVG(price) AS average_daily_price
            FROM crypto_coin_prices
            WHERE coin_id = 'ethereum' AND date >= CURDATE() - INTERVAL 1 YEAR;
        """
        cursor.execute(query)
        result = cursor.fetchone()

        st.write("Average Daily Price of Ethereum in the Past 1 Year:")
        st.write(f"Average Daily Price: ₹ {result[0]:.2f}")

    elif option == "8. Show the daily price trend of Bitcoin in February 2025.":
        query = """
            SELECT date, price
            FROM crypto_coin_prices
            WHERE coin_id = 'bitcoin' AND MONTH(date) = 2 AND YEAR(date) = 2025
            ORDER BY date;
        """
        cursor.execute(query)
        results = cursor.fetchall()

        df=pd.DataFrame(results, columns=["Date", "Price"])

        # Format price with rupee symbol for display
        df['Price_INR'] = df['Price'].apply(lambda x: f"₹{x:,.2f}")

        st.write("Daily Price Trend of Bitcoin in February 2025:")
        st.dataframe(df[['Date', 'Price_INR']])  # shows table with ₹
        st.line_chart(df.set_index("Date")["Price"])

    elif option == "9. Find the coin with the highest average price over 1 year.":
        query = """
            SELECT coin_id, AVG(price) AS average_price
            FROM crypto_coin_prices
            WHERE date >= CURDATE() - INTERVAL 1 YEAR
            GROUP BY coin_id
            ORDER BY average_price DESC
            LIMIT 1;
        """
        cursor.execute(query)
        result = cursor.fetchone()

        st.write("Coin with the Highest Average Price over 1 Year:")
        st.write(f"Coin ID: {result[0]}")
        st.write(f"Average Price: ₹ {result[1]:.2f}")

    elif option == "10. Get the % change in Bitcoin's price between Feb 2025 and Feb 2026.":
        query = """
            SELECT  
                (SELECT price 
                FROM crypto_coin_prices 
                WHERE coin_id = 'bitcoin' AND date = '2025-02-11' 
                LIMIT 1) AS price_feb_2025,
                (SELECT price 
                FROM crypto_coin_prices 
                WHERE coin_id = 'bitcoin' AND date = '2026-02-10' 
                LIMIT 1) AS price_feb_2026;
        """
        cursor.execute(query)
        result = cursor.fetchone()

        price_feb_2025 = result[0]
        price_feb_2026 = result[1]

        if price_feb_2025 and price_feb_2026:
            percent_change = ((price_feb_2026 - price_feb_2025) / price_feb_2025) * 100
            st.write("Percentage Change in Bitcoin's Price between Feb 2025 and Feb 2026:")
            st.write(f"Price on Feb 11, 2025: ₹ {price_feb_2025:.2f}")
            st.write(f"Price on Feb 10, 2026: ₹ {price_feb_2026:.2f}")
            st.write(f"Percentage Change: {percent_change:.2f}%")
        else:
            st.write("Price data for the specified dates is not available.")


    elif option == "11. Find the highest oil price in the last 5 years.":
        query = """
            SELECT MAX(price) AS highest_oil_price
            FROM oil_prices_history
            WHERE date >= CURDATE() - INTERVAL 5 YEAR;
        """
        cursor.execute(query)
        result = cursor.fetchone()

        st.write("Highest Oil Price in the Last 5 Years:")
        st.write(f"🛢️ Highest Oil Price: ₹ {result[0]:.2f}")

    elif option == "12. Get the average oil price per year":
        query = """
            SELECT YEAR(date) AS year, AVG(price) AS average_price
            FROM oil_prices_history
            GROUP BY year
            ORDER BY year;
        """
        cursor.execute(query)
        results = cursor.fetchall()

        st.write("Average Oil Price Per Year:")
        
        df = pd.DataFrame(results, columns=["Year", "Average Price"])
        df['Average Price'] = df['Average Price'].apply(lambda x: f"₹{x:,.2f}")
        df.index = range(1, len(df) + 1)
        st.dataframe(df)

    elif option == "13. Show oil prices during COVID crash (March to April 2020).":
        query = """
            SELECT date, price
            FROM oil_prices_history
            WHERE date BETWEEN '2020-03-01' AND '2020-04-30'
            ORDER BY date;
        """
        cursor.execute(query)
        results = cursor.fetchall()

        st.write("Oil Prices During COVID Crash (March to April 2020):")
        
        df = pd.DataFrame(results, columns=["Date", "Price"])
        df['Price'] = df['Price'].apply(lambda x: f"₹{x:,.2f}")
        df.index = range(1, len(df) + 1)
        st.dataframe(df)

    elif option == "14. Find the lowest price of oil in the last 10 years.":
        query = """
            SELECT MIN(price) AS lowest_oil_price
            FROM oil_prices_history
            WHERE date >= CURDATE() - INTERVAL 10 YEAR;
        """
        cursor.execute(query)
        result = cursor.fetchone()

        st.write("Lowest Oil Price in the Last 10 Years:")
        st.write(f"🛢️ Lowest Oil Price: ₹ {result[0]:.2f}")

    elif option == "15. Calculate the volatility of oil prices (max-min difference per year).":
        query = """
            SELECT YEAR(date) AS year, 
            MAX(price) - MIN(price) AS volatility
            FROM oil_prices_history
            GROUP BY year
            ORDER BY year;
        """
        cursor.execute(query)
        results = cursor.fetchall()

        st.write("Volatility of Oil Prices (Max-Min Difference Per Year):")

        # Build DataFrame
        df = pd.DataFrame(results, columns=["Year", "Volatility"])
        df['Volatility'] = df['Volatility'].apply(lambda x: f"₹{x:,.2f}")
        df.index = range(1, len(df) + 1)    
        st.dataframe(df)

    
    elif option == "16. Get all stock prices for a given ticker":
        ticker = st.text_input("Enter the stock ticker symbol (e.g.,^GSPC, ^DJI):")
        
        if ticker:

            ticker = "^" + ticker.strip().upper()  # Ensure ticker is uppercase and prefixed with ^ 

            query = """
                SELECT date, open, high, low, close, volume
                FROM stock_prices_history
                WHERE ticker = %s
                ORDER BY date DESC;
            """
            cursor.execute(query, (ticker.upper(),))
            results = cursor.fetchall()

            if results:
                df = pd.DataFrame(results, columns=["Date", "Open", "High", "Low", "Close", "Volume"])
                df['Open'] = df['Open'].apply(lambda x: f"₹{x:,.2f}")
                df['High'] = df['High'].apply(lambda x: f"₹{x:,.2f}")
                df['Low'] = df['Low'].apply(lambda x: f"₹{x:,.2f}")
                df['Close'] = df['Close'].apply(lambda x: f"₹{x:,.2f}")
                
                st.write(f"Stock Prices for {ticker.upper()}:")
                st.dataframe(df)
            else:
                st.write(f"No data found for ticker symbol '{ticker.upper()}'. Please check the symbol and try again.")

    elif option == "17. Find the highest closing price for NASDAQ (^IXIC)":
        query = """
            SELECT MAX(close) AS highest_closing_price
            FROM stock_prices_history
            WHERE ticker = '^IXIC';
        """
        cursor.execute(query)
        result = cursor.fetchone()

        st.write("Highest Closing Price for NASDAQ (^IXIC):")
        st.write(f"Highest Closing Price: ₹ {result[0]:.2f}")

    elif option == "18. List top 5 days with highest price difference (high - low) for S&P 500 (^GSPC)":
        query = """
            SELECT date, high - low AS price_difference
            FROM stock_prices_history
            WHERE ticker = '^GSPC'
            ORDER BY price_difference DESC
            LIMIT 5;
        """
        cursor.execute(query)
        results = cursor.fetchall()

        st.write("Top 5 Days with Highest Price Difference (High - Low) for S&P 500 (^GSPC):")
        
        df = pd.DataFrame(results, columns=["Date", "Price Difference"])
        df['Price Difference'] = df['Price Difference'].apply(lambda x: f"₹{x:,.2f}")
        df.index = range(1, len(df) + 1)
        st.dataframe(df)

    elif option == "19. Get monthly average closing price for each ticker":
        query = """
            SELECT ticker, DATE_FORMAT(date, '%Y-%m') AS month, AVG(close) AS avg_closing_price
            FROM stock_prices_history
            GROUP BY ticker, month
            ORDER BY ticker, month;
        """
        cursor.execute(query)
        results = cursor.fetchall()

        
        df = pd.DataFrame(results, columns=["Ticker", "Month", "Average Closing Price"])
        df["Average Closing Price"] = pd.to_numeric(df["Average Closing Price"], errors="coerce")
        df['Average Closing Price'] = df['Average Closing Price'].round(2)
        df.index = range(1, len(df) + 1)

        st.write("Monthly Average Closing Price for Each Ticker:")
        st.dataframe(df.style.format({"Average Closing Price": "₹{:,.2f}"}))

    elif option == "20. Get average trading volume of given ticker in 2024":
        # Sidebar input for ticker
        ticker = st.text_input("Enter the stock ticker symbol:")

        if ticker:
            # Normalize ticker input
            ticker = "^" + ticker.strip().upper()

            # Query for average trading volume
            query = """
                SELECT AVG(volume) AS avg_trading_volume
                FROM stock_prices_history
                WHERE ticker = %s AND YEAR(date) = 2024;
            """
            cursor.execute(query, (ticker,))
            result = cursor.fetchone()

            st.write(f"Average Trading Volume of {ticker} in 2024:")

            if result and result[0] is not None:
                st.write(f"Average Trading Volume: {result[0]:,.0f} shares")
            else:
                st.write("No trading volume data found for this ticker in 2024.")
        else:
            st.write("Please enter a stock ticker symbol to get the average trading volume for 2024.")
        
    elif option == "21. Compare Bitcoin vs Oil average price in 2025.":
        query = """
        SELECT 
            (SELECT AVG(price) 
            FROM crypto_coin_prices 
            WHERE coin_id = 'bitcoin' AND YEAR(date) = 2025) AS avg_bitcoin_price,
            (SELECT AVG(price) 
            FROM oil_prices_history 
            WHERE YEAR(date) = 2025) AS avg_oil_price;
        """
        
        cursor.execute(query)
        avg_bitcoin_price, avg_oil_price = cursor.fetchone()

        st.subheader("📊 Average Price Comparison: Bitcoin vs Oil (2025)")

        if avg_bitcoin_price:
            st.write(f"🪙 Bitcoin (2025 Average): ₹ {avg_bitcoin_price:,.2f}")
        else:
            st.warning("No Bitcoin price data for 2025.")

        if avg_oil_price:
            st.write(f"🛢️ Oil (2025 Average): ₹ {avg_oil_price:,.2f}")
        else:
            st.warning("No Oil price data for 2025.")

    elif option == "22. Check if Bitcoin moves with S&P 500 (correlation idea).":
        query = """
        SELECT c.date, c.price AS bitcoin_price, s.close AS sp500_close
        FROM crypto_coin_prices c
        JOIN stock_prices_history s
        ON c.date = s.date
        WHERE c.coin_id = 'bitcoin'
        AND s.ticker = '^GSPC'
        AND YEAR(c.date) = 2025;
        """

        df = pd.read_sql(query, conn)

        st.subheader("📈 Correlation Check: Bitcoin vs S&P 500 (2025)")

        if not df.empty:
            corr = df['bitcoin_price'].corr(df['sp500_close'])
            st.write(f"🔗 Correlation coefficient (2025): **{corr:.2f}**")
        else:
            st.warning("No overlapping data found for Bitcoin and S&P 500 in 2025.")

    elif option == "23. Compare Ethereum and NASDAQ daily prices for 2025.":
        query = """
        SELECT 
            c.date, 
            c.price AS ethereum_price, 
            s.close AS nasdaq_close
        FROM crypto_coin_prices c
        JOIN stock_prices_history s ON c.date = s.date
        WHERE c.coin_id = 'ethereum' 
        AND s.ticker = '^IXIC' 
        AND YEAR(c.date) = 2025;
        """

        df = pd.read_sql(query, conn)
        df.index = range(1, len(df) + 1)

        st.subheader("📊 Daily Price Comparison: Ethereum vs NASDAQ (2025)")

        if not df.empty:
            st.dataframe(df)
            
        else:
            st.warning("No overlapping data found for Ethereum and NASDAQ in 2025.")

    elif option == "24. Find days when oil price spiked and compare with Bitcoin price change.":
        query = """
        SELECT o.date, o.price AS oil_price, c.price AS bitcoin_price
        FROM oil_prices_history o
        JOIN crypto_coin_prices c ON o.date = c.date
        WHERE YEAR(o.date) = 2025
        AND o.price > (SELECT AVG(price) 
                        FROM oil_prices_history 
                        WHERE YEAR(date) = 2025) * 1.10
        AND c.coin_id = 'bitcoin';
        """

        df = pd.read_sql(query, conn)
        df.index = range(1, len(df) + 1)

        st.subheader("📈 Oil Price Spikes and Bitcoin Price Change (2025)")

        if not df.empty:
            st.dataframe(df)
        else:
            st.warning("No significant oil price spikes found in 2025 or no overlapping Bitcoin data.")

    elif option == "25. Compare top 3 coins daily price trend vs (^DJI, ^GSPC,^IXIC).":

        ticker = st.selectbox(
        "Select Stock Index",
        ["^DJI", "^GSPC", "^IXIC"]  # adjust names to match DB
    )

        query = f"""

        SELECT c.date, c.coin_id, c.price AS coin_price, s.close AS index_close
        FROM (
            SELECT coin_id
            FROM crypto_coin_prices
            WHERE YEAR(date) = 2025
            GROUP BY coin_id
            ORDER BY AVG(price) DESC
            LIMIT 3
        ) top_coins
        JOIN crypto_coin_prices c ON c.coin_id = top_coins.coin_id
        LEFT JOIN stock_prices_history s 
            ON c.date = s.date AND s.ticker = '{ticker}'
        WHERE YEAR(c.date) = 2025;
        """

        df = pd.read_sql(query, conn)
        df.index = range(1, len(df) + 1)

        st.subheader(f"📊 Top 3 Coins Daily Price Trend vs {ticker} (2025)")

        if not df.empty:
            st.dataframe(df)
        else:
            st.warning(f"No data found for top 3 coins or {ticker} in 2025.")

    elif option == "26. Compare stock prices (^GSPC) with crude oil prices on the same dates":
        query = """
        SELECT s.date, s.close AS sp500_close, o.price AS oil_price
        FROM stock_prices_history s
        JOIN oil_prices_history o ON s.date = o.date
        WHERE s.ticker = '^GSPC' AND YEAR(s.date) = 2025;
        """

        df = pd.read_sql(query, conn)
        df.index = range(1, len(df) + 1)

        st.subheader("📈 S&P 500 (^GSPC) vs Crude Oil Prices (2025)")

        if not df.empty:
            st.dataframe(df)
        else:
            st.warning("No overlapping data found for S&P 500 and crude oil in 2025.")

    elif option == "27. Correlate Bitcoin closing price with crude oil closing price (same date)":
        query = """
        SELECT c.date, c.price AS bitcoin_price, o.price AS oil_price
        FROM crypto_coin_prices c
        JOIN oil_prices_history o ON c.date = o.date
        WHERE c.coin_id = 'bitcoin' AND YEAR(c.date) = 2025;
        """

        df = pd.read_sql(query, conn)

        st.subheader("🔗 Correlation: Bitcoin Closing Price vs Crude Oil Price (2025)")

        if not df.empty:
            corr = df['bitcoin_price'].corr(df['oil_price'])
            st.write(f"Correlation coefficient (2025): **{corr:.2f}**")
            st.dataframe(df)
        else:
            st.warning("No overlapping data found for Bitcoin and crude oil in 2025.")
    
    elif option == "28. Compare NASDAQ (^IXIC) with Ethereum price trends.":
            query = """ 
            SELECT c.date, c.price AS ethereum_price, s.close AS nasdaq_close 
            FROM crypto_coin_prices c 
            JOIN stock_prices_history s ON c.date = s.date
            WHERE c.coin_id = 'ethereum' AND s.ticker = '^IXIC' AND YEAR(c.date) = 2025; 
            """ 
            df = pd.read_sql(query, conn) 
            df.index = range(1, len(df) + 1) 
            st.subheader("📊 NASDAQ (^IXIC) vs Ethereum Price Trends (2025)") 
            if not df.empty: st.dataframe(df) 
            else: st.warning("No overlapping data found for NASDAQ and Ethereum in 2025.")

    elif option == "29. Join top 3 crypto coins with stock indices for 2025.":
            query = """ 
            SELECT c.date, c.coin_id, c.price AS coin_price, s.ticker, s.close AS index_close 
            FROM ( SELECT coin_id FROM crypto_coin_prices 
            WHERE YEAR(date) = 2025 
            GROUP BY coin_id 
            ORDER BY AVG(price) DESC 
            LIMIT 3 ) 
            top_coins 
            JOIN crypto_coin_prices c ON c.coin_id = top_coins.coin_id 
            LEFT JOIN stock_prices_history s ON c.date = s.date AND YEAR(s.date) = 2025; 
            """ 
            df = pd.read_sql(query, conn) 
            df.index = range(1, len(df) + 1) 
            st.subheader("📊 Top 3 Crypto Coins Joined with Stock Indices (2025)") 
            if not df.empty: st.dataframe(df) 
            else: st.warning("No data found for top 3 coins or stock indices in 2025.") 

    elif option == "30. Multi-join: stock prices, oil prices, and Bitcoin prices for daily comparison":
            query = """ 
            SELECT s.date, s.ticker, s.close AS stock_close, o.price AS oil_price, c.price AS bitcoin_price 
            FROM stock_prices_history s 
            JOIN oil_prices_history o ON s.date = o.date 
            JOIN crypto_coin_prices c ON s.date = c.date AND c.coin_id = 'bitcoin' 
            WHERE YEAR(s.date) = 2025; 
            """ 
            df = pd.read_sql(query, conn) 
            df.index = range(1, len(df) + 1) 
            st.subheader("📊 Multi-Join: Stock Prices, Oil Prices, and Bitcoin Prices (2025)") 
            if not df.empty: st.dataframe(df) 
            else: st.warning("No overlapping data found for stocks, oil, and Bitcoin in 2025.")


