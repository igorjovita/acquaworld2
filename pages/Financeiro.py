import streamlit as st
import mysql.connector
import os
import pandas as pd
import datetime
from datetime import date, timedelta
from functions import obter_comissao
from babel.numbers import format_currency
from datetime import datetime
from collections import defaultdict
from database import DataBaseMysql
from repository import MainRepository

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

escolha_data = st.radio('Selecione o intervalo da pesquisa', ['Data Especifica', 'Intervalo entre Datas'])

if escolha_data == 'Intervalo entre Datas':
    data1 = st.date_input('Data Inicial', format='DD/MM/YYYY', value=None)
    data2 = st.date_input('Data Final', format='DD/MM/YYYY', value=None)
if escolha_data == 'Data Especifica':
    data1 = st.date_input('Data', format='DD/MM/YYYY')
    data2 = data1

filtro_staffs = st.radio('Selecione o filtro da pesquisa', ['Todos', 'Staff especifico'])

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

lista_staff = []
repo = DataBaseMysql()
repository_staffs = MainRepository(repo)

info_staff = repository_staffs.select_staffs()

for resultado in info_staff:
    lista_staff.append(resultado[1])

filtro1 = st.radio('Opções de filtragem da data', ['Intervalo entre datas', 'Data Especifica'])

if filtro1 == 'Intervalo entre datas':
    data1_pagamento = st.date_input('Data Inicial1', format='DD/MM/YYYY', value=None)
    data2_pagamento = st.date_input('Data Final2', format='DD/MM/YYYY', value=None)
if filtro1 == 'Data Especifica':
    data1_pagamento = st.date_input('Data2', format='DD/MM/YYYY')
    data2_pagamento = data1_pagamento

filtro2 = st.radio('Opções de filtragem dos dados', ['Todos', 'Staff especifico'], index=None)

if filtro2 == 'Staff especifico':
    staff = st.selectbox('Nome do Staff', lista_staff)

if st.button('Pesquisar2'):

    if filtro2 == 'Todos':
        select_total_comissoes = repository_staffs.select_soma_total_comissoes(data1_pagamento, data2_pagamento)
        st.write(select_total_comissoes)


    elif filtro2 == 'Staff especifico':
        index_lista = lista_staff.index(staff)
        id_staff = info_staff[index_lista][0]
        select_comissao_individual = repository_staffs.select_soma_comissao_individual(data1_pagamento, data2_pagamento, id_staff)
        st.write(select_comissao_individual)


    # mydb.connect()
    # cursor.execute(f"SELECT id_staff, comissao FROM staffs where nome ='{staff}'")
    # result = cursor.fetchone()
    # id_staff = result[0]
    # comissao = result[1]
    # cursor.execute(
    #     'SELECT data, funcao, quantidade, curso, pratica, quentinha FROM lancamentos_barco WHERE id_staff = %s and data between %s and %s',
    #     (id_staff, data1_pagamento, data2_pagamento))
    # dados = cursor.fetchall()
    #
    # cursor.execute(
    #     "SELECT data, cilindros_acqua, cilindros_pl, almoco FROM lancamento_cilindro where id_staff = %s and data between %s and %s",
    #     (id_staff, data1_pagamento, data2_pagamento))
    # dados2 = cursor.fetchall()
    #
    # dados_str = ''
    # # Itera sobre cada tupla em 'dados'
    # total_equipagens = 0
    # total_bat = 0
    # total_curso = 0
    # valor_curso = 0
    # total_quentinha = 0
    # total_comissao = 0
    # agrupado_por_data = {}
    # total_cilindro = 0
    # total_diaria = 0
    # calculo_bat = 0
    # total_embarque = 0
    # calculo_quentinha = 0
    #
    # # Itera sobre cada tupla em 'dados'
    # for dado in dados:
    #     # Converta o objeto datetime para uma string formatada
    #     data_form = datetime.strftime(dado[0], "%d/%m/%Y")
    #
    #     if dado[4] is None:
    #         pratica = ''
    #     else:
    #         pratica = dado[4]
    #
    #     if dado[1] == 'AS':
    #         tipo = 'Equipagens'
    #         total_equipagens += int(dado[2])
    #
    #     if dado[1] == 'CAPITAO':
    #         tipo = 'Embarques'
    #         total_embarque += int(dado[2])
    #
    #     if dado[1] == 'CURSO':
    #         tipo = ''
    #         if dado[3] == 'RESCUE':
    #             total_comissao += int(dado[2]) * 150
    #             total_curso += int(dado[2])
    #         elif dado[3] == 'REVIEW':
    #             total_comissao += int(dado[2]) * 120
    #             total_curso += int(dado[2])
    #         elif dado[3] == 'DIVEMASTER':
    #             total_comissao += int(dado[2]) * 200
    #             total_curso += int(dado[2])
    #         else:
    #             total_comissao += int(dado[2]) * 75
    #             total_curso += int(dado[2])
    #     if dado[1] == 'BAT':
    #         tipo = dado[1]
    #         total_bat += float(dado[2])
    #
    #     # Certifica-se de que há pelo menos 5 elementos na tupla
    #     if len(dado) >= 5:
    #         # Inicializa a lista para a data se ainda não existir
    #         if data_form not in agrupado_por_data:
    #             agrupado_por_data[data_form] = []
    #
    #         if dado[5] == 'Sim':
    #             if dado[1] == 'CURSO':
    #                 texto = f'{int(dado[2])}{tipo} {dado[3]} {pratica} + quentinha'
    #                 total_quentinha += 1
    #             else:
    #                 texto = f'{float(dado[2])} {tipo} + quentinha'
    #                 total_quentinha += 1
    #         else:
    #             if dado[1] == 'CURSO':
    #                 texto = f'{int(dado[2])}{tipo} {dado[3]} {pratica}'
    #             else:
    #                 texto = f'{float(dado[2])} {tipo}'
    #
    #         # Adiciona à lista correspondente à data
    #         agrupado_por_data[data_form].append(texto)
    #
    # # Adiciona os dados da tabela lancamento_cilindro ao dicionário agrupado_por_data
    # for dado in dados2:
    #     # Converta o objeto datetime para uma string formatada
    #     data_form = datetime.strftime(dado[0], "%d/%m/%Y")
    #
    #     # Certifica-se de que há pelo menos 4 elementos na tupla
    #     if len(dado) >= 4:
    #
    #         if staff == 'Juninho':
    #             total_diaria += 1
    #         # Inicializa a lista para a data se ainda não existir
    #         if data_form not in agrupado_por_data:
    #             agrupado_por_data[data_form] = []
    #
    #         if dado[2] == 0:
    #             texto = f'{int(dado[1])} Cilindros Acqua'
    #             agrupado_por_data[data_form].append(texto)
    #         else:
    #             texto = f'{int(dado[1])} Cilindros Acqua + {int(dado[2])} Cilindro Pl'
    #             agrupado_por_data[data_form].append(texto)
    #
    # # Agora você pode iterar sobre o dicionário para criar a string final
    # dados_str = ''
    # for data, textos in agrupado_por_data.items():
    #     dados_str += f"{data} - {' + '.join(textos)}\n"
    #
    # # Adiciona uma linha em branco
    # dados_str += '\n'
    #
    # # Calcula os totais e adiciona ao resultado final
    # total_equipagens = sum(int(dado[2]) for dado in dados if dado[1] == 'AS')
    # total_curso = sum(int(dado[2]) for dado in dados if dado[1] == 'CURSO')
    # total_bat = sum(float(dado[2]) for dado in dados if dado[1] not in ['AS', 'CURSO', 'CAPITAO'])
    #
    # total_cilindro_acqua = sum(int(dado[1]) for dado in dados2)
    # total_cilindro_pl = sum(int(dado[2]) for dado in dados2)
    #
    # if total_equipagens != 0:
    #     equipagens_formatado = format_currency(total_equipagens, 'BRL', locale='pt_BR')
    #     dados_str += f"Total Equipagens - {total_equipagens} = {equipagens_formatado}\n"
    #
    # if total_curso != 0:
    #     curso_formatado = format_currency(total_comissao, 'BRL', locale='pt_BR')
    #     dados_str += f"Total Praticas - {total_curso} = {curso_formatado}\n"
    #
    # if total_bat != 0:
    #     calculo_bat = total_bat * comissao
    #     bat_formatado = format_currency(calculo_bat, 'BRL', locale='pt_BR')
    #     dados_str += f"Total Batismos - {total_bat:.2f} = {bat_formatado}\n"
    #
    # if total_quentinha != 0:
    #     calculo_quentinha = total_quentinha * 15
    #     quentinha_formatado = format_currency(calculo_quentinha, 'BRL', locale='pt_BR')
    #     dados_str += f"Total Quentinhas - {total_quentinha} = {quentinha_formatado}\n"
    #
    # if total_embarque != 0:
    #     embarque_formatado = format_currency(total_embarque, 'BRL', locale='pt_BR')
    #     dados_str += f"Total Embarques - {total_embarque} = {embarque_formatado}\n"
    #
    # if total_diaria != 0:
    #     diaria_formatada = format_currency(total_diaria * 50, 'BRL', locale='pt_BR')
    #     dados_str += f"Total Diarias - {total_diaria} = {diaria_formatada}\n"
    #
    # if total_cilindro_acqua != 0 or total_cilindro_pl != 0:
    #     total_cilindro = total_cilindro_acqua + total_cilindro_pl
    #     cilindro_formatado = format_currency(total_cilindro, 'BRL', locale='pt_BR')
    #     dados_str += f"Total Cilindros - {total_cilindro_acqua} Acqua + {total_cilindro_pl} Pl = {cilindro_formatado}\n"
    #
    # total_pagar = total_equipagens + total_comissao + calculo_bat + calculo_quentinha + total_cilindro + (
    #             total_diaria * 50) + total_embarque
    # total_formatado = format_currency(total_pagar, 'BRL', locale='pt_BR')
    # dados_str += f"Total a pagar - {total_formatado}"
    #
    # # Agora, dados_str conterá todos os textos com quebras de linha entre eles
    # st.code(dados_str)
    # mydb.close()

#     for dado in dados:
#
#         # Converta o objeto datetime para uma string formatada
#         data_form = datetime.strftime(dado[0], "%d/%m/%Y")
#
#         if dado[4] is None:
#             pratica = ''
#         else:
#             pratica = dado[4]
#
#         if dado[1] == 'AS':
#             tipo = 'equipagens'
#             total_equipagens += int(dado[2])
#
#         elif dado[1] == 'CURSO':
#             tipo = ''
#             total_curso += int(dado[2])
#         else:
#             tipo = dado[1]
#             total_bat += int(dado[2])
#
#         # Certifica-se de que há pelo menos 5 elementos na tupla
#         if len(dado) >= 5:
#             if dado[5] == 'Sim':
#                 if dado[1] == 'CURSO':
#                     texto = f'{data_form} - {int(dado[2])} {tipo}{dado[3]} {pratica} + quentinha'
#                 else:
#                     texto = f'{data_form} - {int(dado[2])} {tipo} + quentinha'
#             else:
#                 if dado[1] == 'CURSO':
#                     texto = f'{data_form} - {int(dado[2])} {tipo}{dado[3]} {pratica} '
#                 else:
#                     texto = f'{data_form} - {float(dado[2])} {tipo}'
#
#             # Adiciona o texto e uma quebra de linha ao final de dados_str
#             dados_str += texto + '\n'
#         else:
#             st.warning(f'A tupla {dado} não possui o comprimento esperado.')
#
#     dados_str += '\n'
#
#     if total_equipagens != 0:
#         texto_equipagem = (f"""Total Equipagens - {total_equipagens}
# """)
#     else:
#         texto_equipagem = ''
#
#     if total_curso != 0:
#         texto_curso = (f"""Total Praticas - {total_curso}
# """)
#     else:
#         texto_curso = ''
#
#     if total_bat != 0:
#         texto_bat = f"""Total Batismo - {total_bat}
# """
#
#     else:
#         texto_bat = ''
#
#     # Agora, dados_str conterá todos os textos com quebras de linha entre eles
#     st.code(dados_str + texto_equipagem + texto_curso + texto_bat)

# agrupado_por_data = defaultdict(list)
#
# # Agrupando informações do lancamento_bat
# for data, funcao, quantidade, curso, pratica, quentinha in dados:
#     agrupado_por_data[data].append((funcao, quantidade))
#
# # Agrupando informações do lancamento_cilindro
# for data, cilindros_acqua, cilindros_pl, almoco in dados2:
#     agrupado_por_data[data].append(('Cilindro', cilindros_acqua + cilindros_pl))
#
# # Exibindo os resultados
# for data, informacoes in agrupado_por_data.items():
#     st.write(f'Data: {data}')
#     for funcao, quantidade in informacoes:
#         st.write(f'{funcao}: {quantidade}')
#     st.write('-' * 20)
#
#
