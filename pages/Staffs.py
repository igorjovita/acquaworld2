import streamlit as st
import os
import mysql.connector
import pandas as pd

chars = "'),([]"

mydb = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USERNAME"),
    passwd=os.getenv("DB_PASSWORD"),
    db=os.getenv("DB_NAME"),
    autocommit=True)

cursor = mydb.cursor(buffered=True)

st.title('Sistema Acquaworld')

st.header('Staffs')

cursor.execute("Select nome, ocupacao, status FROM staffs")
lista_staffs = str(cursor.fetchall()).translate(str.maketrans('', '', chars)).split()

df = pd.DataFrame(lista_staffs, columns=['Nome', 'Certificação', 'Status'])
st.dataframe(df)

