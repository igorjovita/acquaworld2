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

with st.expander('Divisão diferente'):
    staffd1 = st.text_input('Staff1 - Lance o staff , quantidade').capitalize()
    staffd2 = st.text_input('Staff2 - Lance o staff , quantidade').capitalize()

apoio_superficie = st.selectbox('Apoio de Superficie', ['', 'Juarez', 'Miranda', 'Glauber', 'Roberta'])

equipagens = st.text_input('Equipagens')

mestre = st.selectbox('Mestre', ['', 'Risadinha', 'Marquinhos', 'Freelancer'])

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

    texto_p1 = f"""
            *Divisão:*

            *{data_formatada[2]}/{data_formatada[1]}/{data_formatada[0]}*
            """
    texto_p2 = f"""{divisao} - {lista_final}
            {apoio_superficie} - {equipagens} equipagens
            {mestre} - {embarques} embarques
            """
    texto_curso = f"{instrutor} - {quantidade} {curso} {pratica}"
    texto_curso2 = f"{instrutor2} - {quantidade2} {curso2} {pratica2}"

    if instrutor == '' and staffd1 == '': # Somente batismo sem staff extra
        st.code(texto_p1 + texto_p2)

    if instrutor != '' and staffd1 == '' and instrutor2 == '' and staffd2 == '': # 1  curso
        texto_curso = f"""
            {instrutor} - {quantidade} {curso} {pratica}
            
            {divisao} - {lista_final}
            {apoio_superficie} - {equipagens} equipagens
            {mestre} - {embarques} embarques"""
        st.code(texto_p1 + texto_curso)

    if instrutor2 != '' and staffd1 == '' and staffd2 == '': # 2 cursos
        texto_curso_total = f"""
            {instrutor} - {quantidade} {curso} {pratica}
            {instrutor2} - {quantidade2} {curso2} {pratica2}
            
            """
        st.code(texto_p1 + texto_curso_total + texto_p2)

    if staffd1 != '' and staffd2 == '' and instrutor == '' and instrutor2 == '': # 1 staff extra
        staffd1_formatado = staffd1.split(',')
        texto_staff = f"""
            {staffd1_formatado[1]} - {staffd1_formatado[0]}
            {divisao} - {lista_final}
            {apoio_superficie} - {equipagens} equipagens
            {mestre} - {embarques} embarques"""
        st.code(texto_p1 + texto_staff)

    if staffd1 != '' and staffd2 != '' and instrutor == '' and instrutor2 == '': # 2 staffs extras e 1 curso
        staffd1_formatado = staffd1.split(',')
        staffd2_formatado = staffd2.split(',')
        texto_staff2 = f"""
            {staffd1_formatado[1]} - {staffd1_formatado[0]}
            {staffd2_formatado[1]} - {staffd2_formatado[0]}
            {divisao} - {lista_final}
            {apoio_superficie} - {equipagens} equipagens
            {mestre} - {embarques} embarques"""
        st.code(texto_p1 + texto_staff2)

    if staffd1 != '' and instrutor != '' and staffd2 == '' and instrutor2 == '':  # 1 staff extra e 1 curso
        staffd1_formatado = staffd1.split(',')
        texto_staff = f"""
            {instrutor} - {quantidade} {curso} {pratica}
            
            {staffd1_formatado[1]} - {staffd1_formatado[0]}
            """
        st.code(texto_p1 + texto_staff + texto_p2)

    if staffd1 != '' and instrutor != '' and instrutor2 != '' and staffd2 == '': # 1 staff extra e 2 cursos
        staffd1_formatado = staffd1.split(',')
        texto_staff = f"""
            {instrutor} - {quantidade} {curso} {pratica}
            {instrutor2} - {quantidade2} {curso2} {pratica2}
            
            {staffd1_formatado[1]} - {staffd1_formatado[0]}
            """
        st.code(texto_p1 + texto_staff + texto_p2)

    if staffd1 != '' and staffd2 != '' and instrutor != '' and instrutor2 != '': # 2 staffs extra e 2 cursos
        staffd1_formatado = staffd1.split(',')
        staffd2_formatado = staffd2.split(',')
        texto_staff_curso2 = f"""
            {instrutor} - {quantidade} {curso} {pratica}
            {instrutor2} - {quantidade2} {curso2} {pratica2}
            
            {staffd1_formatado[1]} - {staffd1_formatado[0]}
            {staffd2_formatado[1]} - {staffd2_formatado[0]}
            """
        st.code(texto_p1 + texto_staff_curso2 + texto_p2)

    if staffd1 != '' and staffd2 != '' and instrutor != '' and instrutor2 == '': # 1 curso e 2 staffs extras
        staffd1_formatado = staffd1.split(',')
        staffd2_formatado = staffd2.split(',')
        texto_staff_curso = f"""
            {instrutor} - {quantidade} {curso} {pratica}

            {staffd1_formatado[1]} - {staffd1_formatado[0]}
            {staffd2_formatado[1]} - {staffd2_formatado[0]}
            """
        st.code(texto_p1 + texto_staff_curso + texto_p2)

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
