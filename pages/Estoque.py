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

st.table(df)
