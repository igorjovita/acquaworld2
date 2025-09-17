import streamlit as st
from database import SupabaseDB
from classes import LogicaCadastro
from repository import MainRepository


logica = LogicaCadastro()
db = SupabaseDB()
repo = MainRepository(db)

logica.inputs_cadastro()





# st.write('---')

# st.subheader('Cadastro Cilindro')

# col1, col2 = st.columns(2)

# with col1:
#     marca_cilindro = st.selectbox('Marca do Cilindro', ['', 'Luxfer', 'Catalina'])
#     num_serie_cilindro = st.text_input('Numero de Serie do Cilindro')
#     situacao_cilindro = st.selectbox('Situação do Cilindro', ['', 'Em uso', 'Parado'])

# with col2:
#     modelo_cilindro = st.text_input('Modelo do Cilindro')
#     data_teste = st.date_input('Data do ultimo teste hidrostático', format='DD/MM/YYYY')

# if st.button('Cadastrar Cilindro'):
#     cursor.execute(
#         'INSERT INTO cadastro_cilindro( marca, modelo, num_serie, data_teste, situacao) VALUES (%s, %s, %s, %s, %s)',
#         (marca_cilindro, modelo_cilindro, num_serie_cilindro, data_teste, situacao_cilindro))
#     st.success('Cilindro Cadastrado com sucesso!')

# st.write('---')

# st.subheader('Cadastro Colete')

# col1, col2 = st.columns(2)

# with col1:
#     marca_colete = st.text_input('Marca do Colete').capitalize()
#     tamanho_colete = st.text_input('Tamanho do Colete').capitalize()
# with col2:
#     modelo_colete = st.text_input('Modelo do Colete').capitalize()
#     estado_colete = st.selectbox('Estado do Colete', ['', 'Operacional', 'Furado', 'Em manutenção'])

# if st.button('Cadastrar Colete'):
#     cursor.execute("INSERT INTO cadastro_colete ( marca, modelo, tamanho, estado) VALUES (%s, %s, %s, %s)",
#                    (marca_colete, modelo_colete, tamanho_colete, estado_colete))
#     st.success('Colete Cadastrado com Sucesso!')

# st.write('---')

# st.subheader('Cadastro Regulador')

# col1, col2 = st.columns(2)

# with col1:
#     modelo_regulador = st.text_input('Modelo do Regulador')
#     estado_regulador = st.selectbox('Estado do Regulador', ['', 'Operacional', 'Com vazamento', 'Em manutenção'])

# with col2:
#     numercao_regulador = st.text_input('Numeração do Regulador')

# if st.button('Cadastrar Regulador'):
#     cursor.execute("INSERT INTO cadastro_regulador ( modelo, numeracao, estado) VALUES (%s, %s, %s)",
#                    (modelo_regulador, numercao_regulador, estado_regulador))
#     st.success('Regulador Cadastrado com Sucesso!')
