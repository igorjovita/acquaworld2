import streamlit as st
import mysql.connector
import os
from datetime import timedelta

from database import DataBaseMysql
from repository import MainRepository

st.write('''<style>

[data-testid="column"] {
    width: calc(33.3333% - 1rem) !important;
    flex: 1 1 calc(33.3333% - 1rem) !important;
    min-width: calc(33% - 1rem) !important;
}

</style>''', unsafe_allow_html=True)

chars = "'),([]"

st.header('Controle Cilindros')

col1, col2 = st.columns(2)
with col1:
    data = st.date_input('Data', format='DD/MM/YYYY')
    inicio = str(st.text_input('Horario de Inicio'))
    quantidade_acqua = st.number_input('Cilindros Acqua', step=1)
    quentinha = st.selectbox('Almoço', ['Sim', 'Não'], index=None)

with col2:
    nome = st.selectbox('Staff', ['Juninho', 'Glauber', 'Roberta'], index=None)
    final = str(st.text_input('Horario do Termino'))
    quantidade_pl = st.number_input('Cilindros PL', step=1)

situacao = 'Pendente'

if st.button('Lançar no Sistema'):

    h1 = inicio.split(':')
    h2 = final.split(':')
    hora_inicio = timedelta(hours=float(h1[0]), minutes=float(h1[1]))
    hora_final = timedelta(hours=float(h2[0]), minutes=float(h2[1]))
    horas_trabalhadas = hora_final - hora_inicio

    h3 = horas_trabalhadas.total_seconds() / 60
    media_cilindro = (int(h3) / (quantidade_acqua + quantidade_pl))
    m = str(f'{float(media_cilindro):.2f}').split('.')
    m1 = f'{m[0], m[1]}'
    db = DataBaseMysql()
    repo = MainRepository(db)
    id_staff = repo.select_id_staff_por_nome(nome)
    repo.insert_lancamento_cilindro(data, id_staff, inicio, final, quantidade_acqua, quantidade_pl, situacao, h3, m1)

    if quentinha == 'Sim':
        repo.insert_controle_quentinhas(data, id_staff)

    st.success('Lançado no Sistema com Sucesso!')
    st.subheader(f'Tempo Médio : {m[0]} min e {m[1]} s')
