import streamlit as st
import mysql.connector
import os


mydb = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USERNAME"),
    passwd=os.getenv("DB_PASSWORD"),
    db=os.getenv("DB_NAME"),
    autocommit=True,
    ssl_verify_identity=False,
    ssl_ca=r"C:\users\acqua\downloads\cacert-2023-08-22.pem")

cursor = mydb.cursor()

st.subheader('Cadastro de Staff')

nome = st.text_input('Nome:')
telefone = st.text_input('Telefone')
ocupação = st.text_input('Ocupação')
tipo = st.selectbox('Tipo', ['', 'FREELANCER', 'FIXO'])
if tipo == 'FIXO':
    salario = st.text_input('Valor do Salario')
else:
    salario = 0
comissão = st.text_input('Valor da comissão')

if st.button('Cadastrar Staff'):
    cursor.execute("""
        INSERT INTO staffs (nome, telefone, ocupacao, tipo, salario, comissao) VALUES (%s, %s, %s, %s, %s, %s)
    """, (nome, telefone, ocupação, tipo, salario, comissão))
    mydb.commit()
    st.success('Staff Cadastrado com Sucesso!')