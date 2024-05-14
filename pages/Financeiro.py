import streamlit as st
import mysql.connector
import os
import pandas as pd
import datetime
from datetime import date, timedelta
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
        for item in select_total_comissoes:
            st.write(item)
        df = pd.DataFrame(select_total_comissoes,
                          columns=['Nome', 'Bat', 'Comissao_bat', 'Comissao Efr', 'Equipagem', 'Embarque', 'Praticas', 'Review', 'Rescue', 'EFR', 'DM', 'Cilindro', 'Quentinha', 'Diaria'])




        st.write(df)

    elif filtro2 == 'Staff especifico':
        index_lista = lista_staff.index(staff)
        id_staff = info_staff[index_lista][0]
        select_comissao_individual = repository_staffs.select_soma_comissao_individual(data1_pagamento, data2_pagamento,
                                                                                       id_staff)

        select_contagem_cilindros = repository_staffs.select_contagem_cilindros(data1_pagamento, data2_pagamento,
                                                                                id_staff)

        resultado_combinado = select_comissao_individual + select_contagem_cilindros

        # Ordene os resultados pela data
        resultado_final = sorted(resultado_combinado, key=lambda x: x[0])

        total_valor_bat = 0
        contagem_bat = 0
        contagem_equipagem = 0
        contagem_embarque = 0
        contagem_pratica = 0
        contagem_rescue = 0
        contagem_review = 0
        contagem_divemaster = 0
        contagem_quentinha = 0
        contagem_cilindro_acqua = 0
        contagem_cilindro_pl = 0
        contagem_efr = 0
        contagem_diaria = 0
        mensagem = f'Comissão {staff} do dia {data1_pagamento.strftime("%d/%m")} à {data2_pagamento.strftime("%d/%m")} \n'
        lista_datas = []
        valor_bat = 0
        valor_diaria = 0
        valor_pratica = 0
        valor_review = 0
        valor_rescue = 0
        valor_efr = 0
        valor_divemaster = 0
        valor_quentinha = 0

        for select in resultado_final:

            data, _, bat, equipagem, embarque, quantidade_curso, curso, pratica, quentinha, cilindro_acqua, cilindro_pl, _, diaria = select
            valores_diferentes_de_zero = []

            # Verifica se cada variável é diferente de zero e adiciona à lista
            if bat != '0':
                valores_diferentes_de_zero.append(f'{bat} BAT')
                contagem_bat += float(bat)
            if equipagem != '0':
                valores_diferentes_de_zero.append(f'{equipagem} Equipagens')
                contagem_equipagem += int(equipagem)
            if embarque != '0':
                valores_diferentes_de_zero.append(f'{embarque} Embarques')
                contagem_embarque += int(embarque)
            if quantidade_curso != '0':
                if curso == 'REVIEW':
                    contagem_review += int(quantidade_curso)
                elif curso == 'RESCUE':
                    contagem_rescue += int(quantidade_curso)
                elif curso == 'DIVEMASTER':
                    contagem_divemaster += int(quantidade_curso)
                elif curso == 'PRIMEIROS SOCORROS':
                    contagem_efr += int(quantidade_curso)
                else:
                    contagem_pratica += int(quantidade_curso)
                valores_diferentes_de_zero.append(f'{quantidade_curso} {curso} {pratica}')

            if cilindro_acqua is not None and cilindro_acqua != 0:
                contagem_cilindro_acqua += int(cilindro_acqua)
                valores_diferentes_de_zero.append(f'{cilindro_acqua} Cilindros Acqua')
            if cilindro_pl is not None and cilindro_pl != 0:
                contagem_cilindro_pl += int(cilindro_pl)
                valores_diferentes_de_zero.append(f'{cilindro_pl} Cilindros Pl')

            contagem_diaria += int(diaria)

            if data in lista_datas:
                mensagem += ' + ' + ' + '.join(valores_diferentes_de_zero)
            else:
                lista_datas.append(data)
                if quentinha != 0:
                    contagem_quentinha += int(quentinha)
                    valores_diferentes_de_zero.append('quentinha')
                mensagem += '\n' + f'{data} - ' + ' + '.join(valores_diferentes_de_zero)

        mensagem += '\n'

        if contagem_bat != 0:
            comissao_bat = resultado_final[0][1]
            valor_bat = contagem_bat * int(comissao_bat)
            valor_pagar_bat = format_currency(float(valor_bat), 'BRL', locale='pt_BR')
            mensagem += '\n' + f'Total Batismo - {contagem_bat:.2f} * {comissao_bat} = {valor_pagar_bat}'

        if contagem_equipagem != 0:
            valor_pagar_equipagem = format_currency(float(contagem_equipagem), 'BRL', locale='pt_BR')
            mensagem += '\n' + f'Total Equipagens - {contagem_equipagem} * 1 = {valor_pagar_equipagem}'

        if contagem_embarque != 0:
            valor_pagar_embarque = format_currency(float(contagem_embarque), 'BRL', locale='pt_BR')
            mensagem += '\n' + f'Total Embarques - {contagem_embarque} * 1 = {valor_pagar_embarque}'

        if contagem_pratica != 0:
            valor_pratica = contagem_pratica * 75
            valor_pagar_pratica = format_currency(float(valor_pratica), 'BRL', locale='pt_BR')
            mensagem += '\n' + f'Total Pratica OWD e ADV - {contagem_pratica} * 75 = {valor_pagar_pratica}'

        if contagem_review != 0:
            comissao_review = resultado_final[0][11]
            valor_review = contagem_review * comissao_review
            valor_pagar_review = format_currency(float(valor_review), 'BRL', locale='pt_BR')
            mensagem += '\n' + f'Total Review - {contagem_review} * {comissao_review} = {valor_pagar_review}'

        if contagem_rescue != 0:
            valor_rescue = contagem_rescue * 150
            valor_pagar_rescue = format_currency(float(valor_rescue), 'BRL', locale='pt_BR')
            mensagem += '\n' + f'Total Curso Rescue - {contagem_rescue} * 150 = {valor_pagar_rescue}'

        if contagem_efr != 0:
            valor_efr = contagem_efr * 200
            valor_pagar_efr = format_currency(float(valor_efr), 'BRL', locale='pt_BR')
            mensagem += '\n' + f'Total Curso Primeiro Socorros - {contagem_efr} * 200 = {valor_pagar_efr}'

        if contagem_divemaster != 0:
            valor_divemaster = contagem_divemaster * 200
            valor_pagar_divemaster = format_currency(float(valor_divemaster), 'BRL', locale='pt_BR')
            mensagem += '\n' + f'Total Curso DM - {contagem_divemaster}  * 200 = {valor_pagar_divemaster}'

        if contagem_quentinha != 0:
            valor_quentinha = contagem_quentinha * 15
            valor_pagar_quentinha = format_currency(float(valor_quentinha), 'BRL', locale='pt_BR')
            mensagem += '\n' + f'Total Quentinhas - {contagem_quentinha}  * 15 = {valor_pagar_quentinha}'

        if contagem_cilindro_acqua != 0 or contagem_cilindro_pl != 0:
            valor_pagar_cilindro = contagem_cilindro_acqua + contagem_cilindro_pl
            valor_pagar_cilindro = format_currency(float(valor_pagar_cilindro), 'BRL', locale='pt_BR')
            mensagem += '\n' + f'Total Cilindros - {contagem_cilindro_acqua} Acqua + {contagem_cilindro_pl} PL  = {valor_pagar_cilindro}'
            if contagem_diaria != 0:
                valor_diaria = contagem_diaria * 50
                valor_pagar_diaria = format_currency(float(valor_diaria), 'BRL', locale='pt_BR')
                mensagem += '\n' + f'Total Diarias - {contagem_diaria} diarias * 50  = {valor_pagar_diaria}'

        total_pagar = valor_bat + contagem_equipagem + contagem_embarque + valor_pratica + valor_review + valor_rescue + valor_efr + valor_divemaster + valor_quentinha + contagem_cilindro_acqua + contagem_cilindro_pl + valor_diaria

        mensagem += '\n' + '\n' + f"Total a Pagar = {format_currency(float(total_pagar), 'BRL', locale='pt_BR')}"
        st.code(mensagem)

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
