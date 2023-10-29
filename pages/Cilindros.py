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

chars = "'),([]"
cursor = mydb.cursor()

st.header('Controle Cilindros')
data = st.date_input('Data',format='DD/MM/YYYY')
nome = st.selectbox('Staff', ['', 'Juarez', 'Glauber', 'Roberta'])

cursor.execute(f"SELECT id FROM staffs WHERE nome = '{nome}'")
id_staff = (str(cursor.fetchone()).translate(str.maketrans('', '', chars)))


inicio = str(st.text_input('Horario de Inicio'))
final = str(st.text_input('Horario do Termino')3)




quantidade_acqua = st.text_input('Cilindros Acqua')
quantidade_pl = st.text_input('Cilindros PL')
quentinha = st.selectbox('Almoço', ['', 'Sim', 'Não'])
situacao = 'Pendente'



if st.button('Lançar no Sistema'):
    cursor.execute("""
        INSERT INTO lancamento_cilindro (data, id_staff, horario_inicio, horario_final, cilindros_acqua, cilindros_pl, almoco, situacao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", (data, id_staff, inicio, final, quantidade_acqua, quantidade_pl, quentinha, situacao))
    mydb.commit()
    st.success('Lançado no Sistema com Sucesso!')
    st.write(inicio)
    st.write(final)
