import streamlit as st
import mysql.connector
import os
from datetime import timedelta

mydb = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USERNAME"),
    passwd=os.getenv("DB_PASSWORD"),
    db=os.getenv("DB_NAME"),
    autocommit=True,
    ssl_verify_identity=False,
    ssl_ca=r"C:\users\acqua\downloads\cacert-2023-08-22.pem")

st.write('''<style>

[data-testid="column"] {
    width: calc(33.3333% - 1rem) !important;
    flex: 1 1 calc(33.3333% - 1rem) !important;
    min-width: calc(33% - 1rem) !important;
}

</style>''', unsafe_allow_html=True)

chars = "'),([]"
cursor = mydb.cursor()

st.header('Controle Cilindros')

col1, col2 = st.columns(2)
with col1:
    data = st.date_input('Data', format='DD/MM/YYYY')
    inicio = str(st.text_input('Horario de Inicio'))
    quantidade_acqua = st.number_input('Cilindros Acqua', step=1)
    quentinha = st.selectbox('Almoço', ['', 'Sim', 'Não'])

with col2:
    nome = st.selectbox('Staff', ['', 'Juarez', 'Glauber', 'Roberta'])
    final = str(st.text_input('Horario do Termino'))
    quantidade_pl = st.number_input('Cilindros PL', step=1)

cursor.execute(f"SELECT id_staff FROM staffs WHERE nome = '{nome}'")
id_staff = (str(cursor.fetchone()).translate(str.maketrans('', '', chars)))

situacao = 'Pendente'

if st.button('Lançar no Sistema'):
    h1 = inicio.split(':')
    h2 = final.split(':')
    hora_inicio = timedelta(hours=float(h1[0]), minutes=float(h1[1]))
    hora_final = timedelta(hours=float(h2[0]), minutes=float(h2[1]))
    horas_trabalhadas = hora_final - hora_inicio
    h3 = horas_trabalhadas.total_seconds() / 60
    media_cilindro = str((int(h3) / (quantidade_acqua + quantidade_pl))).split('.')


    cursor.execute("""
        INSERT INTO lancamento_cilindro (data, id_staff, horario_inicio, horario_final, cilindros_acqua, cilindros_pl, almoco, situacao, horas_trabalhadas) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                   (data, id_staff, inicio, final, quantidade_acqua, quantidade_pl, quentinha, situacao, horas_trabalhadas))
    mydb.commit()
    st.success('Lançado no Sistema com Sucesso!')
    st.subheader(f'Tempo por Cilindro: {media_cilindro[0]} minutos e {media_cilindro[1]} segundos')

