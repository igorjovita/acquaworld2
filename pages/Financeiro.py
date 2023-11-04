import streamlit as st
import mysql.connector
import os
import pandas as pd

mydb = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USERNAME"),
    passwd=os.getenv("DB_PASSWORD"),
    db=os.getenv("DB_NAME"),
    autocommit=True)

cursor = mydb.cursor(buffered=True)

chars = "'),([]"
chars2 = "')([]"

st.title('Sistema AcquaWorld')

st.header('Financeiro')

st.subheader('Selecione o intervalo da pesquisa')
data1 = st.date_input('Data Inicial', format='DD/MM/YYYY')
data2 = st.date_input('Data Final', format='DD/MM/YYYY')

cursor.execute(f"select data, id_staff, divisao from lancamento_bat where data between '{data1}' and '{data2}'")
lista = str(cursor.fetchall()).translate(str.maketrans('', '', chars)).split()

df = pd.DataFrame(lista, columns=['Data', 'Staff', 'Divisão'])
