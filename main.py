import streamlit as st
from streamlit_option_menu import option_menu
import sqlqueryrunner  # import your file
import crossmarketoverview as marketoverview # import your file
import top3cryptoanalysis as top3cryptoanalysis # import your file

st.set_page_config(layout='wide')
col1, col2 = st.columns([1, 5])

with col1:
    st.image("C:\\Users\\hemhe\\Documents\\GUVIproject\\project1\\Create a transparent.png", width=350)


with st.sidebar:
    select = option_menu('Main Menu', ['Market Overview', 'SQL Query Runner', 'Top 3 Crypto Analysis'])

if select == 'Market Overview':
    marketoverview.run() # 👈 Call function from crossmarketoverview.py

elif select == 'SQL Query Runner':
    sqlqueryrunner.run()   # 👈 Call function from sqlqueryrunner.py

elif select == 'Top 3 Crypto Analysis':
    top3cryptoanalysis.run()   # 👈 Call function from top3cryptoanalysis.py
