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

nome = st.text_input('Nome:').capitalize().strip()
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

st.subheader('Cadastro Cilindro')

marca_cilindro = st.selectbox('Marca do Cilindro', ['', 'Luxfer', 'Catalina'])

modelo_cilindro = st.text_input('Modelo do Cilindro')

num_serie_cilindro = st.text_input('Numero de Serie do Cilindro')

data_teste = st.date_input('Data do ultimo teste hidrostático')

situacao_cilindro = st.selectbox('Situação do Cilindro', ['', 'Em uso', 'Parado'])

if st.button('Cadastrar Cilindro'):
    cursor.execute('INSERT INTO cadastro_cilindro( marca, modelo, num_serie, data_teste, situacao) VALUES (%s, %s, %s, %s, %s)',(marca_cilindro, modelo_cilindro, num_serie_cilindro, data_teste, situacao_cilindro))
    st.success('Cilindro Cadastrado com sucesso!')

st.write('---')

st.subheader('Cadastro Colete')

marca_colete = st.text_input('Marca do Colete').capitalize()

modelo_colete = st.text_input('Modelo do Colete').capitalize()

tamanho_colete = st.text_input('Tamanho do Colete').capitalize()

estado_colete = st.selectbox('Estado do Colete', ['', 'Operacional', 'Furado', 'Em manutenção'])

if st.button('Cadastrar Colete'):
    cursor.execute("INSERT INTO cadastro_colete ( marca, modelo, tamanho, estado) VALUES (%s, %s, %s, %s)",(marca_colete, modelo_colete, tamanho_colete, estado_colete))
    st.success('Colete Cadastrado com Sucesso!')

st.write('---')

st.subheader('Cadastro Regulador')

modelo_regulador = st.text_input('Modelo do Regulador')

numercao_regulador = st.text_input('Numeração do Regulador')

estado_regulador = st.selectbox('Estado do Regulador', ['', 'Operacional', 'Com vazamento', 'Em manutenção'])

if st.button('Cadastrar Regulador'):
    cursor.execute("INSERT INTO cadastro_regulador ( modelo, numeracao, estado) VALUES (%s, %s, %s)", (modelo_regulador, numercao_regulador, estado_regulador))
    st.success('Regulador Cadastrado com Sucesso!')

