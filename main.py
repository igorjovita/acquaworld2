import os
import streamlit as st
import MySQLdb
from dotenv import load_dotenv
import pandas as pd
import mysql.connector

conn = st.experimental_connection('mysql', type='sql')

df = conn.query('SELECT * from lancamento_bat;', ttl=600)

# Print results.
for row in df.itertuples():
    st.write(f"{row.name} has a :{row.pet}:")

