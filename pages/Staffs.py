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

cursor.execute("Select nome, ocupacao, status FROM staffs")
nome_staffs = cursor.fetchall()

cursor.execute("SELECT ocupacao FROM staffs")
cert_staffs = str(cursor.fetchall()).translate(str.maketrans('', '', chars)).split()

cursor.execute("SELECT status FROM staffs")
status_staffs = str(cursor.fetchall()).translate(str.maketrans('', '', chars)).split()

colunas = st.columns((2, 2, 2, 1, 1))
campos = ['Nome', 'Certificação', 'Status']
for col, campo_nome in zip(colunas, campos):
    col.write(campo_nome)

for item in nome_staffs:
    col1, col2, col3, col4, col5 = st.columns((2, 2, 2, 1, 1))
    with col1:
        st.write(item[0])

    with col2:
        st.write(item[1])

    with col3:
        st.write(item[2])

    with col4:
        excluir_botao = col4.empty()
        on_click_excluir = excluir_botao.button('🗑️', 'btnExcluir' + item[0])

    with col5:
        status_botao = col5.empty()
        on_click_status = status_botao.button('✅', 'btnStatus' + item[0])

    if on_click_excluir:
        cursor.execute(f"DELETE FROM staffs WHERE nome = '{item[0]}'")
        mydb.commit()
        st.success('Staff Excluido com Sucesso')

    if on_click_status:
        cursor.execute(f"SELECT status from staffs WHERE nome = '{item[0]}'")
        status = str(cursor.fetchone()).translate(str.maketrans('', '', chars2))
        st.write(status)
        if status == 'Ativo':
            cursor.execute(f"UPDATE staffs set status = 'Inativo' WHERE nome = '{item[0]}'")
            mydb.commit()
            st.success('Status Atualizado com Sucesso')
            time.sleep(0.5)
            st.experimental_rerun()
        if status == 'Inativo':
            cursor.execute(f"UPDATE staffs set status = 'Ativo' WHERE nome = '{item[0]}'")
            mydb.commit()
            st.success('Status Atualizado com Sucesso')
            time.sleep(0.5)
            st.experimental_rerun()
