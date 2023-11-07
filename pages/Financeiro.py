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
escolha = st.selectbox('Escolha o tipo', ['Comissão Staff', 'Comissao AS', 'Comisao Capitao', 'Comissao Cilindro'])
botao = st.button('Pesquisar')

if botao:
    if escolha == 'Comissao Staff':
        cursor.execute(f" select id_staff, sum(divisao) as divisao from lancamento_bat where data between '{data1}' and '{data2}' group by id_staff order by divisao desc")
        lista = cursor.fetchall()

        for item in lista:
            id_staff = item[0]
            divisao = item[1]
            col1, col2, col3 = st.columns(3)
            with col1:
                mydb.connect()
                cursor.execute(f"SELECT nome from staffs where id_staff = {id_staff}")
                nome_staff = (str(cursor.fetchall()).translate(str.maketrans('', '', chars)))
                mydb.close()
                st.subheader(nome_staff)

            with col2:
                st.subheader(divisao)

            with col3:
                mydb.connect()
                cursor.execute(f"SELECT comissao from staffs where id_staff = '{id_staff}'")
                comissao_staff = (str(cursor.fetchall()).translate(str.maketrans('', '', chars)))
                mydb.close()
                valor_pagar = float(divisao) * int(comissao_staff)
                st.subheader(f'R$ {valor_pagar}')
    if escolha == 'Comissao AS':
        cursor.execute(
            f" select id_staff, sum(equipagens) as equipagens from lancamento_as where data between '{data1}' and '{data2}' group by id_staff order by equipagens desc")
        lista = cursor.fetchall()

        for item in lista:
            id_staff = item[0]
            equipagens = item[1]
            col1, col2 = st.columns(2)

            with col1:
                mydb.connect()
                cursor.execute(f"SELECT nome from staffs where id_staff = {id_staff}")
                nome_as = (str(cursor.fetchall()).translate(str.maketrans('', '', chars)))
                mydb.close()
                st.subheader(nome_as)

            with col2:
                st.subheader(equipagens)


    if escolha == 'Comissao Capitao':
        cursor.execute(f" select id_staff, sum(embarques) as embarques from lancamento_mestre where data between '{data1}' and '{data2}' group by id_staff order by embarques desc")
        lista = cursor.fetchall()

        for item in lista:
            id_staff = item[0]
            embarques = item[1]
            col1, col2 = st.columns(2)

            with col1:
                mydb.connect()
                cursor.execute(f"SELECT nome from staffs where id_staff = {id_staff}")
                nome_as = (str(cursor.fetchall()).translate(str.maketrans('', '', chars)))
                mydb.close()
                st.subheader(nome_as)

            with col2:
                st.subheader(embarques)


