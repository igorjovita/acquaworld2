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
    quantidade_acqua = st.text_input('Cilindros Acqua')
    quentinha = st.selectbox('Almoço', ['', 'Sim', 'Não'])

with col2:
    nome = st.selectbox('Staff', ['', 'Juarez', 'Glauber', 'Roberta'])
    final = str(st.text_input('Horario do Termino'))
    quantidade_pl = st.text_input('Cilindros PL')

cursor.execute(f"SELECT id FROM staffs WHERE nome = '{nome}'")
id_staff = (str(cursor.fetchone()).translate(str.maketrans('', '', chars)))

situacao = 'Pendente'

if st.button('Lançar no Sistema'):
    cursor.execute("""
        INSERT INTO lancamento_cilindro (data, id_staff, horario_inicio, horario_final, cilindros_acqua, cilindros_pl, almoco, situacao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                   (data, id_staff, inicio, final, quantidade_acqua, quantidade_pl, quentinha, situacao))
    mydb.commit()
    st.success('Lançado no Sistema com Sucesso!')
    st.write(inicio)
    st.write(final)
