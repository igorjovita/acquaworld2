from database import DataBaseMysql
from repository import MainRepository
import pandas as pd
import streamlit as st

db = DataBaseMysql()
repository = MainRepository(db)

st.subheader('Cilindros')

select_cilindros = repository.select_cilindros_cadastrados()
df = pd.DataFrame(select_cilindros, columns=['Marca', 'Numero de Serie', 'Teste', 'Situação'])

df['Teste'] = pd.to_datetime(df['Teste']).dt.strftime('%d/%m/%Y')

cilindro_parado = 0
cilindro_em_uso = 0
for cilindro in select_cilindros:
    if cilindro[3] == 'Em uso':
        cilindro_em_uso += 1
    elif cilindro[3] == 'Parado':
        cilindro_parado += 1

st.text(f'Cilindros em uso : {cilindro_em_uso}')
st.text(f'Cilindros parados : {cilindro_parado}')

st.table(df)

