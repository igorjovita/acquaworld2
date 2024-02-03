import streamlit as st
import mysql.connector
import os
import pandas as pd
import datetime
from datetime import date, timedelta
from functions import obter_comissao
from babel.numbers import format_currency
from datetime import datetime

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
    data1 = st.date_input('Data Inicial', format='DD/MM/YYYY', value=None)
    data2 = st.date_input('Data Final', format='DD/MM/YYYY', value=None)
if escolha_data == 'Data Especifica':
    data1 = st.date_input('Data', format='DD/MM/YYYY')
    data2 = data1
escolha = st.selectbox('Escolha o tipo',
                       ['Comissão Staff', 'Comissão AS', 'Comissão Capitao', 'Comissão Curso', 'Comissão Cilindro'])
if escolha == 'Comissão Curso':
    instrutor = st.selectbox('Instrutor', ['Glauber', 'Martin'])

if escolha == 'Comissão Cilindro':
    nome_staff_cilindro = st.selectbox('Staff Cilindro', options=['Juninho', 'Glauber', 'Roberta'])
botao = st.button('Pesquisar')

if botao:
    total_divisao = 0
    total_valor_pagar = 0
    if escolha == 'Comissão Staff':
        cursor.execute(
            f" select id_staff, sum(quantidade) as quantidade from lancamentos_barco where data between '{data1}' and '{data2}' and funcao = 'BAT' group by id_staff order by quantidade desc")
        lista = cursor.fetchall()

        for item in lista:
            id_staff = item[0]
            divisao = item[1]

            total_divisao += divisao

            cursor.execute(f"SELECT nome, comissao from staffs where id_staff = {id_staff}")
            info_staff = cursor.fetchone()
            nome_staff = info_staff[0]
            comissao_staff = info_staff[1]
            valor_pagar = float(divisao) * int(comissao_staff)
            total_valor_pagar += valor_pagar
            valor_formatado = str(f'R$ {float(valor_pagar):.2f}').replace('.', ',')
            data1_split = str(data1).split('-')
            data1_formatada = f'{data1_split[2]}/{data1_split[1]}/{data1_split[0]}'
            data2_split = str(data2).split('-')
            data2_formatada = f'{data2_split[2]}/{data2_split[1]}/{data2_split[0]}'

            st.markdown(
                f"<span style='font-size:20px;'>{nome_staff} - {divisao} Bat do dia {data1_formatada} a {data2_formatada} - {valor_formatado}</span>",
                unsafe_allow_html=True)

        st.subheader("Total Divisão: {}".format(total_divisao))
        st.subheader("Total Valor a Pagar: R$ {:.2f}".format(total_valor_pagar))
    if escolha == 'Comissão AS':
        cursor.execute(
            f" select id_staff, sum(quantidade) as quantidade from lancamentos_barco where data between '{data1}' and '{data2}' and funcao = 'AS' group by id_staff order by quantidade desc")
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
        cursor.execute(
            f" select id_staff, sum(quantidade) as embarques from lancamentos_barco where data between '{data1}' and '{data2}' and funcao = 'CAPITAO'group by id_staff order by embarques desc")
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
        cursor.execute(
            f"SELECT count(id_staff), id_staff, sum(cilindros_acqua), sum(cilindros_pl) from lancamento_cilindro where data between '{data1}' and '{data2}' and id_staff = {id_staff_cilindro}")
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

                cursor.execute(
                    f"select count(almoco) from lancamento_cilindro where data between '{data1}' and '{data2}' and id_staff = {id_staff_cilindro} and almoco = 'Sim'")
                quentinhas = (str(cursor.fetchall()).translate(str.maketrans('', '', chars)))
                if nome_staff_cilindro == 'Juninho':
                    valor_total = (int(diarias) * 50) + int(cilindros_acqua) + int(cilindros_pl) + (
                            int(quentinhas) * 17)
                else:
                    valor_total = int(cilindros_acqua) + int(cilindros_pl) + (int(quentinhas) * 17)
                cursor.execute(
                    f"select horario_inicio from lancamento_cilindro where data between '{data1}' and '{data2}'")
                horario_inicial = (str(cursor.fetchone()).translate(str.maketrans('', '', chars)))
                cursor.execute(
                    f"SELECT horario_final from lancamento_cilindro where data between '{data1}' and '{data2}'")
                horario_final = (str(cursor.fetchone()).translate(str.maketrans('', '', chars)))
                cursor.execute(
                    f"select sum(horas_trabalhadas) from lancamento_cilindro where data between '{data1}' and '{data2}'")
                minutos = float((str(cursor.fetchone()).translate(str.maketrans('', '', chars))))
                mydb.close()
                horario_total = str(timedelta(minutes=minutos) / 60).split(':')
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
        cursor.execute(
            f"SELECT data, curso, quantidade, pratica from lancamentos_barco where data between '{data1}' and '{data2}' and id_staff = {id_instrutor} and funcao = 'CURSO'")
        cursos = cursor.fetchall()
        mydb.close()
        df = pd.DataFrame(cursos, columns=['Data', 'Curso', 'Quantidade', 'Pratica'])
        df['Data'] = pd.to_datetime(df['Data'])

        # Formatando a coluna 'Data' para o formato brasileiro
        df['Data'] = df['Data'].dt.strftime('%d/%m/%Y')
        total_praticas = df['Quantidade'].sum()
        df['Comissao'] = df['Curso'].apply(obter_comissao)
        df['Comissao'] = df['Comissao'].apply(int)
        df['Quantidade'] = df['Quantidade'].apply(int)
        df['Comissao'] *= df['Quantidade']
        df = df.fillna('')
        # Configuração de estilo para ocultar o índice
        html_table = df.to_html(index=False)

        # Exibir HTML no Streamlit
        st.markdown(html_table, unsafe_allow_html=True)
        total_comissao = df['Comissao'].sum()
        comissao_total = format_currency(total_comissao, 'BRL', locale='pt_BR')
        st.subheader(f'{int(total_praticas)} praticas - Total {comissao_total}')


st.write('---')

st.subheader('Pagamento')
cursor.execute("SELECT nome from staffs")
lista_staff = str(cursor.fetchall()).translate(str.maketrans('', '', chars)).split()
filtro = st.radio('Opções de Filtragem', ['Intervalo entre datas', 'Data Especifica'])

if filtro == 'Intervalo entre datas':
    data1_pagamento = st.date_input('Data Inicial1', format='DD/MM/YYYY', value=None)
    data2_pagamento = st.date_input('Data Final2', format='DD/MM/YYYY', value=None)
if filtro == 'Data Especifica':
    data1_pagamento = st.date_input('Data2', format='DD/MM/YYYY')
    data2_pagamento = data1_pagamento
staff = st.selectbox('Nome do Staff', lista_staff)
if st.button('Pesquisar2'):

    cursor.execute(f"SELECT id_staff FROM staffs where nome ='{staff}'")
    id_staff = cursor.fetchone()[0]
    cursor.execute(
        'SELECT data, funcao, quantidade, curso, pratica, quentinha FROM lancamentos_barco WHERE id_staff = %s and data between %s and %s',
        (id_staff, data1_pagamento, data2_pagamento))
    dados = cursor.fetchall()
    dados_str = ''
    st.write('oi')
    # Itera sobre cada tupla em 'dados'
    total_equipagens = 0
    total_bat = 0
    total_curso = 0

    for dado in dados:

        # Converta o objeto datetime para uma string formatada
        data_form = datetime.strftime(dado[0], "%d/%m/%Y")

        if dado[4] is None:
            pratica = ''
        else:
            pratica = dado[4]

        if dado[1] == 'AS':
            tipo = 'equipagens'
            total_equipagens += int(dado[2])

        elif dado[1] == 'CURSO':
            tipo = ''
            total_curso += int(dado[2])
        else:
            tipo = dado[1]
            total_bat += int(dado[2])

        # Certifica-se de que há pelo menos 5 elementos na tupla
        if len(dado) >= 5:
            if dado[5] == 'Sim':
                if dado[1] == 'CURSO':
                    texto = f'{data_form} - {int(dado[2])} {tipo}{dado[3]} {pratica} + quentinha'
                else:
                    texto = f'{data_form} - {int(dado[2])} {tipo} + quentinha'
            else:
                if dado[1] == 'CURSO':
                    texto = f'{data_form} - {int(dado[2])} {tipo}{dado[3]} {pratica} '
                else:
                    texto = f'{data_form} - {int(dado[2])} {tipo}'

            # Adiciona o texto e uma quebra de linha ao final de dados_str
            dados_str += texto + '\n'
        else:
            st.warning(f'A tupla {dado} não possui o comprimento esperado.')

        if total_equipagens != 0:
            texto_equipagem = f'Total Equipagens - {total_equipagens}'
        else:
            texto_equipagem = ''

        if total_curso != 0:
            texto_curso = f'Total Praticas - {total_curso}'
        else:
            texto_curso = ''

        if total_bat != 0:
            texto_bat = f'Total Batismo - {total_bat}'

        else:
            texto_bat = ''

    # Agora, dados_str conterá todos os textos com quebras de linha entre eles
    st.code(dados_str + texto_equipagem + texto_curso + texto_bat)
    st.write(total_equipagens)
    st.write(total_curso)
    st.write(total_bat)
    # df = pd.DataFrame(dados, columns=['Data', 'Função', 'Quantidade', 'Curso', 'Pratica', 'Quentinha'])
    # st.table(df)



    # cursor.execute(f"SELECT staffs.nome, lancamentos_barco.quantidade, lancamentos_barco.curso, lancamentos_barco.pratica, lancamentos_barco.quentinha from "
    #                f"lancamentos_barco JOIN staffs ON lancamentos_barco.id_staff = staffs.id_staff where data between '{data1_pagamento}' and '{data2_pagamento}' and staffs.nome = '{staff}'")
    # resultados = cursor.fetchall()
    #
    # for resultado in resultados:
    #     st.markdown(
    #         f"<span style='font-size:20px;'>{resultado}</span>", unsafe_allow_html=True)












