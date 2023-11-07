import streamlit as st
import mysql.connector
import os
import pandas as pd
import datetime

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
data1 = st.date_input('Data Inicial', format='DD/MM/YYYY', value=datetime.date(year=2023, month=11, day=0o1))
data2 = st.date_input('Data Final', format='DD/MM/YYYY')

cursor.execute(f" select id_staff, sum(divisao) from lancamento_bat where data between '{data1}' and '{data2}' group by id_staff")
lista = cursor.fetchall()
df = pd.DataFrame(lista, columns=['Staff', 'Divisão'])
st.dataframe(df)

for item in lista:
    id_staff = item[0]
    divisao = item[1]
    mydb.connect()
    nome_staff = cursor.execute(f"SELECT nome from staffs where id_staff = {id_staff}")
    mydb.close()
    st.write(nome_staff)
    st.write(id_staff)


