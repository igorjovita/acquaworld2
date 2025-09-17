import streamlit as st
import mysql.connector
import os
import pandas as pd
import datetime
from datetime import date, timedelta
from babel.numbers import format_currency
from datetime import datetime
from collections import defaultdict
from database import SupabaseDB
from repository import MainRepository


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

st.subheader('Pagamentos')

lista_staff = []
repo = SupabaseDB()
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
        total_pagamento = []
        soma_valores = 0
        for item in select_total_comissoes:
            nome, comissao_bat, comissao_review, qntd_bat, qntd_equipagem, qntd_embarque, qntd_pratica, qntd_review, qntd_rescue, qntd_efr, qntd_dm, cilindros, quentinhas, diarias, diarias_as = item

            valores = {
                'bat': float(qntd_bat),
                'valor_bat': float(qntd_bat) * int(comissao_bat),
                'equipagens': int(qntd_equipagem),
                'valor_equipagem': int(qntd_equipagem),
                'embarques': int(qntd_embarque),
                'valor_embarque': int(qntd_embarque),
                'praticas': int(qntd_pratica),
                'valor_pratica': int(qntd_pratica) * 75,
                'review': int(qntd_review),
                'valor_review': int(qntd_review) * int(comissao_review),
                'rescue': int(qntd_rescue),
                'valor_rescue': int(qntd_rescue) * 150,
                'efr': int(qntd_efr),
                'valor_efr': int(qntd_efr) * 200,
                'dm': int(qntd_dm),
                'valor_dm': int(qntd_dm) * 75,
                'cilindros': int(cilindros),
                'valor_cilindros': int(cilindros),
                'diarias': int(diarias),
                'valor_diaria': int(diarias) * 50,
                'quentinhas': int(quentinhas),
                'valor_quentinha': int(quentinhas) * 15,
                'diaria_as': int(diarias_as) * 50

            }

            mensagem = []
            valor_total = 0

            for chave, valor in valores.items():
                if valor != 0:

                    if str(chave).startswith('valor'):
                        valor_total += valor
                    else:

                        mensagem.append(f'{valor} {chave}')

            soma_valores += valor_total

            mensagem = ' + '.join(mensagem)
            valor_total = format_currency(float(valor_total), 'BRL', locale='pt_BR')
            total_pagamento.append((nome, mensagem, valor_total))

        df = pd.DataFrame(total_pagamento, columns=['Nome', 'Descrição', 'Total'])

        st.table(df)
        st.write(soma_valores)

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

            data, _, bat, equipagem, embarque, quantidade_curso, curso, pratica, quentinha, cilindro_acqua, cilindro_pl, _, diaria, diarias_as = select
            
            valores_diferentes_de_zero = []

            # Verifica se cada variável é diferente de zero e adiciona à lista
            if bat != '0':
                valores_diferentes_de_zero.append(f'{bat} BAT')
                contagem_bat += float(bat)
            if equipagem != '0':
                if diarias_as != '0':
                    valores_diferentes_de_zero.append(f'{diarias_as} Diarias AS + {equipagem} Equipagens')
                else:
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
            valor_divemaster = contagem_divemaster * 75
            valor_pagar_divemaster = format_currency(float(valor_divemaster), 'BRL', locale='pt_BR')
            mensagem += '\n' + f'Total Curso DM - {contagem_divemaster}  * 75 = {valor_pagar_divemaster}'

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

