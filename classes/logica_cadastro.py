
import streamlit as st
from database import DataBaseMysql
from repository import MainRepository


db = DataBaseMysql()
repo = MainRepository(db)


class LogicaCadastro:
    
    
    def __init__(self):
        pass


    def inputs_cadastro():

        st.subheader('Cadastro de Staff')

        col1, col2 = st.columns(2)

        with col1:
            nome = st.text_input('Nome:').capitalize().strip()
            ocupação = st.selectbox('Função', ['Instrutor', 'Divemaster', 'Gopro', 'AS', 'Capitão'], index=None)
            tipo = st.selectbox('Tipo', ['FREELANCER', 'FIXO'], index=None)

        with col2:
            telefone = st.text_input('Telefone')
            comissão = st.text_input('Valor da comissão')
            
            if tipo == 'FIXO':
                salario = st.text_input('Valor do Salario')
            else:
                salario = 0

        if st.button('Cadastrar Staff'):
            
            try:
                repo.insert_staff(nome, telefone, ocupação, tipo, salario, comissão, 'Ativo')
            
            finally:
                st.success('Staff Cadastrado com Sucesso!')
