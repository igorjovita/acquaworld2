import streamlit as st
import os
import mysql.connector
import pandas as pd
import time

chars = "')([]"
chars2 = "'),([]"



mydb = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USERNAME"),
    passwd=os.getenv("DB_PASSWORD"),
    db=os.getenv("DB_NAME"),
    autocommit=True)

cursor = mydb.cursor(buffered=True)

st.title('Sistema Acquaworld')

st.header('Staffs')

cursor.execute("Select nome, status FROM staffs")
nome_staffs = cursor.fetchall()

cursor.execute("SELECT nome FROM staffs")
cert_staffs = str(cursor.fetchall()).translate(str.maketrans('', '', chars2)).split()


def seleciona_status(nome):
    mydb.connect()
    cursor.execute(f"SELECT status FROM staffs where nome = {nome}")
    status_staffs = str(cursor.fetchall()).translate(str.maketrans('', '', chars)).split()
    mydb.close()
    return status_staffs

st.write('''<style>

[data-testid="column"] {
    width: calc(33.3333% - 1rem) !important;
    flex: 1 1 calc(33.3333% - 1rem) !important;
    min-width: calc(33% - 1rem) !important;
}

</style>''', unsafe_allow_html=True)


colunas = st.columns((2, 2, 2, 1))
campos = ['Nome', 'Status', 'Excluir']
for col, campo_nome in zip(colunas, campos):
    col.write(campo_nome)

for item in nome_staffs:
    col1, col2, col3 = st.columns((1, 1, 1))
    with col1:
        st.write(item[0])

    with col2:
        st.write(item[1])

    with col3:
        excluir_botao = col3.empty()
        on_click_excluir = excluir_botao.button('🗑️', 'btnExcluir' + item[0])


    if on_click_excluir:
        mydb.connect()
        cursor.execute(f"DELETE FROM staffs WHERE nome = '{item[0]}'")
        mydb.commit()
        mydb.close()
        st.success('Staff Excluido com Sucesso')

st.write('---')

st.subheader('Atualizar Status')

nome = st.selectbox('Staff', cert_staffs)

status = st.selectbox('Status', ['Ativo', 'Inativo'])

if st.button('Atualizar Status'):
    mydb.connect()
    cursor.execute(f"Update staffs set status = '{status}' where nome = '{nome}'")
    mydb.commit()
    mydb.close()


