import streamlit as st
import mysql.connector
import os
from datetime import datetime


mydb = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USERNAME"),
    passwd=os.getenv("DB_PASSWORD"),
    db=os.getenv("DB_NAME"),
    autocommit=True,
    ssl_verify_identity=False,
    ssl_ca=r"C:\users\acqua\downloads\cacert-2023-08-22.pem")

cursor = mydb.cursor()
now = datetime.now()
data = st.date_input
staff = st.selectbox('Staff', ['', 'Juarez', 'Glauber', 'Roberta'])
hora_inicio = str(st.text_input('Horario de Inicio'))
hora_final = str(st.text_input('Horario do Termino'))
segundos = ':00'
inicio = hora_inicio + segundos
final = hora_final + segundos
quantidade_acqua = st.text_input('Cilindros Acqua')
quantidade_pl = st.text_input('Cilindros PL')
quentinha = st.selectbox('Almoço', ['', 'Sim', 'Não'])
situacao = 'Pendente'



if st.button('Lançar no Sistema'):
    cursor.execute("INSERT INTO lancamento_cilindro (data, id_staff, horario_inicio, horario_final, cilindros_acqua, clindros_pl, almoço, situacao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",(data, staff, inicio, final, quantidade_acqua, quantidade_pl, quentinha, situacao))
    mydb.commit()
    st.success('Lançado no Sistema com Sucesso!')
    st.write(inicio)
    st.write(final)
