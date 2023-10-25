import os
import streamlit as st
import MySQLdb
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
mydb = MySQLdb.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USERNAME"),
    passwd=os.getenv("DB_PASSWORD"),
    db=os.getenv("DB_NAME"),
    autocommit=True,
    ssl_mode="VERIFY_IDENTITY",
    ssl={
        "ca": "C:\ssl\certs\cacert.pem"
    }
)

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
st.write('---')

st.subheader('Teste Divisao staffs')

data = st.date_input('Data:', format='DD/MM/YYYY')
st.text('STAFFS:')
col1, col2, col3, col4 = st.columns(4)

with col1:
    staff1 = st.checkbox('Glauber')
    staff5 = st.checkbox('Cauã')
with col2:
    staff2 = st.checkbox('Roberta')
    staff6 = st.checkbox('Thiago')
with col3:
    staff3 = st.checkbox('Martin')

with col4:
    staff4 = st.checkbox('Veridiana')
divisao = st.text_input('Divisão')
chars = "'),([]"
chars2 = "')([]"

apoio_superficie = st.text_input('Apoio de Superficie').capitalize()
equipagens = st.text_input('Equipagens')
mestre = st.text_input('Mestre').capitalize()
embarques = st.text_input('Embarques')

instrutor = st.selectbox('Instrutor', ['', 'Glauber', 'Martin'])
curso = st.selectbox('Curso', ['', 'OWD', 'ADV', 'REVIEW', 'RESCUE', 'PRIMEIROS SOCORROS', 'DIVEMASTER'])
quantidade = st.text_input('Quantidade')
pratica = st.selectbox('Pratica', ['', 'Pratica 1', 'Pratica 2'])
with st.expander('Segundo Curso'):
    instrutor2 = st.selectbox('Instrutor2', ['', 'Glauber', 'Martin'])
    curso2 = st.selectbox('Curso2', ['', 'OWD', 'ADV', 'REVIEW', 'RESCUE', 'PRIMEIROS SOCORROS', 'DIVEMASTER'])
    quantidade2 = st.text_input('Quantidade2')
    pratica2 = st.selectbox('Pratica2', ['', 'Pratica 1', 'Pratica 2'])

cursor.execute(f"SELECT id FROM staffs WHERE nome = '{apoio_superficie}'")
id_as = (str(cursor.fetchone()).translate(str.maketrans('', '', chars)))

if st.button('Lançar no Sistema'):

    if apoio_superficie != '':
        situacao = 'PENDENTE'
        cursor.execute("INSERT INTO lancamento_as(data, id_staff, equipagens, situacao) VALUES (%s, %s, %s, %s)",
                       (data, id_as, equipagens, situacao))
        st.write(id_as)
        mydb.commit()
    if mestre != '':
        cursor.execute(f"SELECT id FROM staffs WHERE nome = '{mestre}'")
        id_staff = (str(cursor.fetchone()).translate(str.maketrans('', '', chars)))
        situacao = 'PENDENTE'
        cursor.execute("INSERT INTO lancamento_mestre(data, id_staff, embarques, situacao) VALUES (%s, %s, %s, %s)",
                       (data, id_staff, embarques, situacao))
        mydb.commit()

    if curso != '':
        cursor.execute(f"SELECT id FROM staffs WHERE nome = '{instrutor}'")
        id_staff = (str(cursor.fetchone()).translate(str.maketrans('', '', chars)))
        situacao = 'PENDENTE'
        cursor.execute("INSERT INTO lancamento_curso(data, id_staff, curso, quantidade, pratica, situacao) VALUES ("
                       "%s, %s, %s, %s, %s, %s)",
                       (data, id_staff, curso, quantidade, pratica, situacao))
        mydb.commit()

    if curso2 != '':
        cursor.execute(f"SELECT id FROM staffs WHERE nome = '{instrutor2}'")
        id_staff = (str(cursor.fetchone()).translate(str.maketrans('', '', chars)))
        situacao = 'PENDENTE'
        cursor.execute("INSERT INTO lancamento_curso(data, id_staff, curso, quantidade, pratica, situacao) VALUES ("
                       "%s, %s, %s, %s, %s, %s)",
                       (data, id_staff, curso2, quantidade2, pratica2, situacao))
        mydb.commit()

    if staff1:
        nome = 'Glauber'
        cursor.execute(f"SELECT id FROM staffs WHERE nome = '{nome}'")
        id_staff = (str(cursor.fetchone()).translate(str.maketrans('', '', chars)))
        cursor.execute(f"SELECT comissao FROM staffs WHERE nome = '{nome}'")
        situacao = 'PENDENTE'

        cursor.execute(
            'INSERT INTO lancamento_bat (data, id_staff, divisao,situacao) VALUES (%s, %s, %s, %s)',
            (data, id_staff, divisao, situacao))
        mydb.commit()

    if staff2:
        nome = 'Roberta'
        cursor.execute(f"SELECT id FROM staffs WHERE nome = '{nome}'")
        id_staff = (str(cursor.fetchone()).translate(str.maketrans('', '', chars)))
        cursor.execute(f"SELECT comissao FROM staffs WHERE nome = '{nome}'")
        situacao = 'PENDENTE'
        st.write(id_staff)
        cursor.execute(
            'INSERT INTO lancamento_bat (data, id_staff, divisao, situacao) VALUES (%s, %s, %s, %s)',
            (data, id_staff, divisao, situacao))
        mydb.commit()

    if staff3:
        nome = 'Martin'
        cursor.execute(f"SELECT id FROM staffs WHERE nome = '{nome}'")
        id_staff = (str(cursor.fetchone()).translate(str.maketrans('', '', chars)))
        cursor.execute(f"SELECT comissao FROM staffs WHERE nome = '{nome}'")
        situacao = 'PENDENTE'
        st.write(id_staff)
        cursor.execute(
            'INSERT INTO lancamento_bat (data, id_staff, divisao, situacao) VALUES (%s, %s, %s, %s)',
            (data, id_staff, divisao, situacao))
        mydb.commit()

    if staff4:
        nome = 'Veridiana'
        cursor.execute(f"SELECT id FROM staffs WHERE nome = '{nome}'")
        id_staff = (str(cursor.fetchone()).translate(str.maketrans('', '', chars)))
        cursor.execute(f"SELECT comissao FROM staffs WHERE nome = '{nome}'")
        situacao = 'PENDENTE'
        st.write(id_staff)
        cursor.execute(
            'INSERT INTO lancamento_bat (data, id_staff, divisao, situacao) VALUES (%s, %s, %s, %s)',
            (data, id_staff, divisao, situacao))
        mydb.commit()

    if staff5:
        nome = 'Cauã'
        cursor.execute(f"SELECT id FROM staffs WHERE nome = '{nome}'")
        id_staff = (str(cursor.fetchone()).translate(str.maketrans('', '', chars)))
        cursor.execute(f"SELECT comissao FROM staffs WHERE nome = '{nome}'")
        situacao = 'PENDENTE'
        st.write(id_staff)
        cursor.execute(
            'INSERT INTO lancamento_bat (data, id_staff, divisao, situacao) VALUES (%s, %s, %s, %s)',
            (data, id_staff, divisao, situacao))
        mydb.commit()

    if staff6:
        nome = 'Thiago'
        cursor.execute(f"SELECT id FROM staffs WHERE nome = '{nome}'")
        id_staff = (str(cursor.fetchone()).translate(str.maketrans('', '', chars)))
        cursor.execute(f"SELECT comissao FROM staffs WHERE nome = '{nome}'")
        situacao = 'PENDENTE'
        st.write(id_staff)
        cursor.execute(
            'INSERT INTO lancamento_bat (data, id_staff, divisao, situacao) VALUES (%s, %s, %s, %s)',
            (data, id_staff, divisao, situacao))
        mydb.commit()
    st.success('Divisão Lançada no Sistema')

cursor.execute("SELECT * FROM lancamento_bat")
df = pd.DataFrame(cursor.fetchall(), columns=['ID', 'Data', 'Id_staff', 'Divisao', 'Situação'])
st.dataframe(df)

cursor.execute("SELECT * FROM lancamento_as")
df2 = pd.DataFrame(cursor.fetchall())
st.dataframe(df2)

cursor.execute("SELECT * FROM lancamento_mestre")
df3 = pd.DataFrame(cursor.fetchall())
st.dataframe(df3)

cursor.execute("SELECT * FROM lancamento_curso")
df4 = pd.DataFrame(cursor.fetchall())
st.dataframe(df4)

cursor.execute("SELECT * FROM staffs")
df5 = pd.DataFrame(cursor.fetchall())
st.dataframe(df5)
