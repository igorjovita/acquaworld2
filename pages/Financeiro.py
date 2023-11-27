import streamlit as st
import mysql.connector
import os
import pandas as pd
import datetime
from datetime import date, timedelta
mydb = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USERNAME"),
    passwd=os.getenv("DB_PASSWORD"),
    db=os.getenv("DB_NAME"),
    autocommit=True)

cursor = mydb.cursor(buffered=True)

st.write('''<style>

[data-testid="column"] {
    width: calc(33.3333% - 1rem) !important;
    flex: 1 1 calc(33.3333% - 1rem) !important;
    min-width: calc(33% - 1rem) !important;
}

</style>''', unsafe_allow_html=True)


chars = "'),([]"
chars2 = "')([]"

st.title('Sistema AcquaWorld')

st.header('Financeiro')

st.subheader('Selecione o intervalo da pesquisa')
escolha_data = st.radio('Opçoes de filtragem', ['Data Especifica', 'Intervalo entre Datas'])
if escolha_data == 'Intervalo entre Datas':
    mes_atual = date.today().month
    data1 = st.date_input('Data Inicial', format='DD/MM/YYYY', value=datetime.date(year=2023, month=mes_atual, day=0o1))
    data2 = st.date_input('Data Final', format='DD/MM/YYYY')
if escolha_data == 'Data Especifica':
    data1 = st.date_input('Data', format='DD/MM/YYYY')
    data2 = data1
escolha = st.selectbox('Escolha o tipo', ['Comissão Staff', 'Comissão AS', 'Comissão Capitao', 'Comissão Curso', 'Comissão Cilindro'])
if escolha == 'Comissão Curso':
    instrutor = st.selectbox('Instrutor', ['Glauber', 'Martin'])

if escolha == 'Comissão Cilindro':
    nome_staff_cilindro = st.selectbox('Staff Cilindro', options=['Juarez', 'Glauber', 'Roberta'])
botao = st.button('Pesquisar')

if botao:

    if escolha == 'Comissão Staff':
        cursor.execute(f" select id_staff, sum(divisao) as divisao from lancamento_bat where data between '{data1}' and '{data2}' group by id_staff order by divisao desc")
        lista = cursor.fetchall()

        for item in lista:
            id_staff = item[0]
            divisao = item[1]
            col1, col2, col3 = st.columns(3)
            with col1:
                mydb.connect()
                cursor.execute(f"SELECT nome from staffs where id_staff = {id_staff}")
                nome_staff = (str(cursor.fetchall()).translate(str.maketrans('', '', chars)))
                mydb.close()
                st.subheader(nome_staff)

            with col2:
                st.subheader(divisao)

            with col3:
                mydb.connect()
                cursor.execute(f"SELECT comissao from staffs where id_staff = '{id_staff}'")
                comissao_staff = (str(cursor.fetchall()).translate(str.maketrans('', '', chars)))
                mydb.close()
                valor_pagar = float(divisao) * int(comissao_staff)
                st.subheader(str(f'R$ {float(valor_pagar):.2f}').replace('.', ','))
    if escolha == 'Comissão AS':
        cursor.execute(
            f" select id_staff, sum(equipagens) as equipagens from lancamento_as where data between '{data1}' and '{data2}' group by id_staff order by equipagens desc")
        lista = cursor.fetchall()

        for item in lista:
            id_staff = item[0]
            equipagens = item[1]
            col1, col2 = st.columns(2)

            with col1:
                mydb.connect()
                cursor.execute(f"SELECT nome from staffs where id_staff = {id_staff}")
                nome_as = (str(cursor.fetchall()).translate(str.maketrans('', '', chars)))
                mydb.close()
                st.subheader(nome_as)

            with col2:
                st.subheader(equipagens)


    if escolha == 'Comissão Capitao':
        cursor.execute(f" select id_staff, sum(embarques) as embarques from lancamento_mestre where data between '{data1}' and '{data2}' group by id_staff order by embarques desc")
        lista = cursor.fetchall()

        for item in lista:
            id_staff = item[0]
            embarques = item[1]
            col1, col2 = st.columns(2)

            with col1:
                mydb.connect()
                cursor.execute(f"SELECT nome from staffs where id_staff = {id_staff}")
                nome_as = (str(cursor.fetchall()).translate(str.maketrans('', '', chars)))
                mydb.close()
                st.subheader(nome_as)

            with col2:
                st.subheader(embarques)



    if escolha == 'Comissão Cilindro':
        mydb.connect()
        cursor.execute(f"SELECT id_staff FROM staffs WHERE nome = '{nome_staff_cilindro}'")
        id_staff_cilindro = (str(cursor.fetchone()).translate(str.maketrans('', '', chars)))
        cursor.execute(f"SELECT count(id_staff), id_staff, sum(cilindros_acqua), sum(cilindros_pl) from lancamento_cilindro where data between '{data1}' and '{data2}' and id_staff = {id_staff_cilindro}")
        lista = cursor.fetchall()
        mydb.close()


        for item in lista:
            diarias = item[0]
            id_staff = item[1]
            cilindros_acqua = item[2]
            cilindros_pl = item[3]
            mydb.connect()
            if id_staff is None:
                st.error(f"Nenhum lançamento de {nome_staff_cilindro} na data informada")
            else:
                cursor.execute(f"SELECT nome from staffs where id_staff = {id_staff}")
                staff_cilindro = (str(cursor.fetchall()).translate(str.maketrans('', '', chars)))

                cursor.execute(f"select count(almoco) from lancamento_cilindro where data between '{data1}' and '{data2}' and almoco = 'Sim' and id_staff = {id_staff_cilindro}")
                quentinhas = (str(cursor.fetchall()).translate(str.maketrans('', '', chars)))
                if nome_staff_cilindro == 'Juarez':
                    valor_total = (int(diarias)*50) + int(cilindros_acqua) + int(cilindros_pl) + (int(quentinhas)*17)
                else:
                    valor_total = int(cilindros_acqua) + int(cilindros_pl) + (int(quentinhas) * 17)
                cursor.execute(f"select horario_inicio from lancamento_cilindro where data between '{data1}' and '{data2}'")
                horario_inicial = (str(cursor.fetchone()).translate(str.maketrans('', '', chars)))
                cursor.execute(f"SELECT horario_final from lancamento_cilindro where data between '{data1}' and '{data2}'")
                horario_final = (str(cursor.fetchone()).translate(str.maketrans('', '', chars)))
                cursor.execute(f"select sum(horas_trabalhadas) from lancamento_cilindro where data between '{data1}' and '{data2}'")
                minutos = float((str(cursor.fetchone()).translate(str.maketrans('', '', chars))))
                mydb.close()
                horario_total = str(timedelta(minutes=minutos)/60).split(':')
                media_cilindro = (int(minutos) / (cilindros_acqua + cilindros_pl))
                min = str(f'{float(media_cilindro):.2f}').split('.')

                seg = str(int(min[1]) * 60)

                col1, col2 = st.columns(2)
                if escolha_data == 'Data Especifica':
                    with col1:
                        st.subheader('Staff :')
                        st.subheader('Cilindros Acqua :')
                        st.subheader('Cilindros PL :')
                        st.subheader('Quentinhas :')
                        st.subheader(f'Horario Inicial :')
                        st.subheader(f'Horario Final :')
                        st.subheader(f'Total de Horas :')
                        st.subheader(f'Tempo Médio :')
                        st.header(f'Valor a pagar :')


                    with col2:
                        st.subheader(staff_cilindro)
                        st.subheader(cilindros_acqua)
                        st.subheader(cilindros_pl)
                        st.subheader(quentinhas)
                        st.subheader(horario_inicial)
                        st.subheader(horario_final)
                        st.subheader(f'{horario_total[1]} horas e {horario_total[2]} min')
                        if seg != '0':
                            st.subheader(f'{min[0]} min e {seg[0]}{seg[1]} s')
                        else:
                            st.subheader(f'{min[0]} min e {seg[0]} s')
                        st.header(f'R$ {valor_total}')



                if escolha_data == 'Intervalo entre Datas':
                    with col1:
                        st.subheader('Staff :')
                        st.subheader('Diárias :')
                        st.subheader('Cilindros Acqua :')
                        st.subheader('Cilindros PL :')
                        st.subheader('Quentinhas :')
                        st.subheader(f'Total de Horas :')
                        st.subheader(f'Tempo Médio :')
                        st.header(f'Valor a pagar :')

                    with col2:
                        st.subheader(staff_cilindro)
                        st.subheader(diarias)
                        st.subheader(cilindros_acqua)
                        st.subheader(cilindros_pl)
                        st.subheader(quentinhas)
                        st.subheader(f'{horario_total[1]} horas e {horario_total[2]} min')
                        st.subheader(f'{min[0]} min e {seg[0]}{seg[1]} s')
                        st.header(f'R$ {valor_total}')


    if escolha == 'Comissão Curso':
        mydb.connect()
        cursor.execute(f"Select id_staff from staffs where nome = '{instrutor}'")
        id_instrutor = (str(cursor.fetchone()).translate(str.maketrans('', '', chars)))
        cursor.execute(f"SELECT data, curso, quantidade, pratica from lancamento_curso where data between '{data1}' and '{data2}' and id_staff = {id_instrutor}")
        cursos = cursor.fetchall()
        mydb.close()
        df = pd.DataFrame(cursos, columns=['Data', 'Curso', 'Quantidade', 'Pratica'])
        st.dataframe(df)

