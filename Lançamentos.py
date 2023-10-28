import streamlit as st
import pandas as pd
import os
import mysql.connector
import MySQLdb


mydb = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USERNAME"),
    passwd=os.getenv("DB_PASSWORD"),
    db=os.getenv("DB_NAME"),
    autocommit=True)


cursor = mydb.cursor(buffered=True)

chars = "'),([]"
chars2 = "')([]"

st.subheader('Divisão Diaria')

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

lista = []
if st.button('Lançar no Sistema'):

    if apoio_superficie != '':
        situacao = 'PENDENTE'
        cursor.execute("INSERT INTO lancamento_as(data, id_staff, equipagens, situacao) VALUES (%s, %s, %s, %s)",
                       (data, id_as, equipagens, situacao))
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
        lista.append('Glauber')

    if staff2:
        nome = 'Roberta'
        cursor.execute(f"SELECT id FROM staffs WHERE nome = '{nome}'")
        id_staff = (str(cursor.fetchone()).translate(str.maketrans('', '', chars)))
        cursor.execute(f"SELECT comissao FROM staffs WHERE nome = '{nome}'")
        situacao = 'PENDENTE'
        cursor.execute(
            'INSERT INTO lancamento_bat (data, id_staff, divisao, situacao) VALUES (%s, %s, %s, %s)',
            (data, id_staff, divisao, situacao))
        mydb.commit()
        lista.append('Roberta')

    if staff3:
        nome = 'Martin'
        cursor.execute(f"SELECT id FROM staffs WHERE nome = '{nome}'")
        id_staff = (str(cursor.fetchone()).translate(str.maketrans('', '', chars)))
        cursor.execute(f"SELECT comissao FROM staffs WHERE nome = '{nome}'")
        situacao = 'PENDENTE'
        cursor.execute(
            'INSERT INTO lancamento_bat (data, id_staff, divisao, situacao) VALUES (%s, %s, %s, %s)',
            (data, id_staff, divisao, situacao))
        mydb.commit()
        lista.append('Martin')
    if staff4:
        nome = 'Veridiana'
        cursor.execute(f"SELECT id FROM staffs WHERE nome = '{nome}'")
        id_staff = (str(cursor.fetchone()).translate(str.maketrans('', '', chars)))
        cursor.execute(f"SELECT comissao FROM staffs WHERE nome = '{nome}'")
        situacao = 'PENDENTE'
        cursor.execute(
            'INSERT INTO lancamento_bat (data, id_staff, divisao, situacao) VALUES (%s, %s, %s, %s)',
            (data, id_staff, divisao, situacao))
        mydb.commit()
        lista.append('Veridiana')
    if staff5:
        nome = 'Cauã'
        cursor.execute(f"SELECT id FROM staffs WHERE nome = '{nome}'")
        id_staff = (str(cursor.fetchone()).translate(str.maketrans('', '', chars)))
        cursor.execute(f"SELECT comissao FROM staffs WHERE nome = '{nome}'")
        situacao = 'PENDENTE'
        cursor.execute(
            'INSERT INTO lancamento_bat (data, id_staff, divisao, situacao) VALUES (%s, %s, %s, %s)',
            (data, id_staff, divisao, situacao))
        mydb.commit()
        lista.append('Cauã')

    if staff6:
        nome = 'Thiago'
        cursor.execute(f"SELECT id FROM staffs WHERE nome = '{nome}'")
        id_staff = (str(cursor.fetchone()).translate(str.maketrans('', '', chars)))
        cursor.execute(f"SELECT comissao FROM staffs WHERE nome = '{nome}'")
        situacao = 'PENDENTE'
        cursor.execute(
            'INSERT INTO lancamento_bat (data, id_staff, divisao, situacao) VALUES (%s, %s, %s, %s)',
            (data, id_staff, divisao, situacao))
        mydb.commit()
        lista.append('Thiago')
    st.success('Divisão Lançada no Sistema')

    data_formatada = str(data).translate(str.maketrans('', '', chars)).split('-')
    st.write('---')
    lista_final = str(lista).translate(str.maketrans('', '', chars2))

    st.text_area('Whatsapp', value=f'Data {data_formatada[2]}/{data_formatada[1]}/{data_formatada[0]}\n'
                                   f'Staffs: {lista_final}\n'
                                   f'Divisão: {divisao}\n'
                                   f'AS: {apoio_superficie} - {equipagens} equipagens\n'
                                   f'Capitão: {mestre} - {embarques} embarques', height=300)


    st.header('Divisão')
    st.subheader(f'Data :  {data_formatada[2]}/{data_formatada[1]}/{data_formatada[0]}')
    st.subheader(f'Staffs : {lista_final}')
    st.subheader(f'Divisão : {divisao}')
    st.subheader(f'Apoio de Superficie : {apoio_superficie}')
    st.subheader(f'Equipagens : {equipagens}')
    st.subheader(f'Capitão : {mestre}')
    st.subheader(f'Embarques : {embarques}')

    st.write('---')

    if instrutor != '':
        st.header('Curso')
        st.subheader(f'Instrutor: {instrutor}')
        st.subheader(f'Curso: {curso}')
        st.subheader(f'Quantidade: {quantidade}')
        st.subheader(f'Prática: {pratica}')

    if instrutor2 != '':
        st.write('---')
        st.header('Curso 2')
        st.subheader(f'Instrutor: {instrutor2}')
        st.subheader(f'Curso: {curso2}')
        st.subheader(f'Quantidade: {quantidade2}')
        st.subheader(f'Prática: {pratica2}')
# cursor.execute("SELECT * FROM lancamento_bat")
# df = pd.DataFrame(cursor.fetchall(), columns=['ID', 'Data', 'Id_staff', 'Divisao', 'Situação'])
# st.dataframe(df)
#
# cursor.execute("SELECT * FROM lancamento_as")
# df2 = pd.DataFrame(cursor.fetchall())
# st.dataframe(df2)
#
# cursor.execute("SELECT * FROM lancamento_mestre")
# df3 = pd.DataFrame(cursor.fetchall())
# st.dataframe(df3)
#
# cursor.execute("SELECT * FROM lancamento_curso")
# df4 = pd.DataFrame(cursor.fetchall())
# st.dataframe(df4)
#
# cursor.execute("SELECT * FROM staffs")
# df5 = pd.DataFrame(cursor.fetchall())
# st.dataframe(df5)
