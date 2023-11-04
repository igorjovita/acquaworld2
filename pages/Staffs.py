import streamlit as st
import os
import mysql.connector


mydb = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USERNAME"),
    passwd=os.getenv("DB_PASSWORD"),
    db=os.getenv("DB_NAME"),
    autocommit=True)

cursor = mydb.cursor(buffered=True)


st.title('Sistema Acquaworld')

st.header('Staffs')

chars = "'),([]"
cursor.execute("SELECT nome FROM staffs")
lista = cursor.fetchall()
staffs = []

data = st.date_input('Data:', format='DD/MM/YYYY')


for i, item in enumerate(lista):
    col1, col2, _ = st.columns([0.05, 0.8, 0.15])
    done = col1.checkbox("a", key=str(i), label_visibility="hidden")

    col2.markdown(item, unsafe_allow_html=True)

    if done:
        staffs.append(str(item))

divisao = st.text_input('Divisao')

if st.button('Lançar no Sistema'):
    for i in staffs:
        nome = str(item)
        cursor.execute(f"SELECT id FROM staffs WHERE nome = '{nome}'")
        id_staff = (str(cursor.fetchone()).translate(str.maketrans('', '', chars)))
        cursor.execute(f"SELECT comissao FROM staffs WHERE nome = '{nome}'")
        situacao = 'PENDENTE'
        cursor.execute(
            'INSERT INTO lancamento_bat (data, id_staff, divisao,situacao) VALUES (%s, %s, %s, %s)',
            (data, id_staff, divisao, situacao))
        mydb.commit()


