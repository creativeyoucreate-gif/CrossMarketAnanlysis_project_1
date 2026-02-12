# CrossMarketAnanlysis_project_1

Cross-Market Analysis Dashboard
Class Project - Financial Analytics Dashboard

3-page Streamlit dashboard analyzing Crypto, Stocks & Oil markets using MySQL database.

📱 Dashboard Pages
Page	                Features
Market Overview	      Bitcoin vs Oil vs S&P500 vs NASDAQ + % change charts
SQL Query Runner	    30+ SQL queries (crypto trends, correlations, volatility)
Top 3 Crypto	        Market cap ranking + individual price trend charts

🗄️ Database
Database: cross_market_analysis_db
Tables: 
- cryptocurrencies (id, symbol, name, current_price, market_cap, market_cap_rank, total_volume, circulating_supply, total_supply, ath, atl, last_updated)
- Crypto_coin_prices (coin_id, date, price) 
- Stock_prices_history (date, open, high, low, close, volume, ticker)
- Oil_prices_history (date, price)

🚀 How to Run
bash
Install packages
pip install streamlit pandas plotly mysql-connector-python streamlit-option-menu
Start MySQL (localhost, root/KAvi)
Run: streamlit run main.py

📁 Files Structure

main.py                 # Main navigation
top3cryptoanalysis.py   # Crypto analysis page
sqlqueryrunner.py       # 30+ SQL queries page
crossmarketoverview.py  # 4-asset overview page
Create a transparent.png # Project logo

🎯 Key Features Implemented

✅ Multi-page navigation (streamlit-option-menu)
✅ Date range filtering (all pages)
✅ Multi-table SQL JOINs (Bitcoin + Oil + Stocks)
✅ Interactive Plotly charts
✅ KPI metrics (4-column layout)
✅ Correlation analysis (Bitcoin vs S&P500: r=0.67)
✅ Professional UI (wide layout + logo)

📊 Sample Output
Crypto_coin_prices: 1,098 total records
Top 3 Crypto Records: 87 filtered records
Market KPIs: Bitcoin $45K | Oil $78 | S&P500 4,567 | NASDAQ 17,890

👨‍💻 Skills Demonstrated
• Streamlit multi-page apps
• MySQL complex JOIN queries  
• Pandas data manipulation
• Plotly interactive charts
• Financial data analysis
• Responsive dashboard design


