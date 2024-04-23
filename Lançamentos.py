import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import os
import mysql.connector
from database import DataBaseMysql
from repository import MainRepository
mysql_db = DataBaseMysql()

repo = MainRepository(mysql_db)


chars = "'),([]"
chars2 = "')([]"


st.write('''<style>

[data-testid="column"] {
    width: calc(33.3333% - 1rem) !important;
    flex: 1 1 calc(33.3333% - 1rem) !important;
    min-width: calc(33% - 1rem) !important;
}
</style>''', unsafe_allow_html=True)

escolha = option_menu(menu_title=None, options=['Lançar', 'Editar', 'Deletar'],
                      icons=['book', 'pencil-square', 'trash'],
                      orientation='horizontal')
if escolha == 'Lançar':

    lista_staffs = []
    lista_staffs_total = []
    select_nome_id_staff = repo.select_staffs()

    for select in select_nome_id_staff:
        if select[2] == 'Divemaster' or select[2] == 'Instrutor':
            lista_staffs.append(select[1])
        lista_staffs_total.append(select[1])

    staffs_selecionados = []

    st.subheader('Divisão Diaria')
    data = st.date_input('Data:', format='DD/MM/YYYY')
    st.text('STAFFS:')

    col1, col2 = st.columns(2)

    for i, item in enumerate(lista_staffs):
        if i < len(lista_staffs) / 2:
            done = col1.checkbox(str(item), key=str(i))
        else:
            done = col2.checkbox(str(item), key=str(i))

        if done:
            if str(item) not in staffs_selecionados:
                staffs_selecionados.append(str(item))

    divisao = st.text_input('Divisão')

    with st.expander('Divisão diferente'):
        col1, col2 = st.columns(2)
        with col1:
            staff_diferente1 = st.selectbox('Nome do staff', options=lista_staffs, index=None)
            staff_diferente2 = st.selectbox('Nome do staff2', options=lista_staffs, index=None)

        with col2:
            quantidade_diferente1 = st.text_input('Divisão1')
            quantidade_diferente2 = st.text_input('Divisão2')

    colu1, colu2 = st.columns(2)

    with colu1:
        apoio_superficie = st.multiselect('Apoio de Superficie', ['Manu', 'Catatau', 'Juninho', 'Glauber', 'Roberta'])
        mestre = st.selectbox('Mestre', ['Risadinha', 'Marquinhos', 'Freelancer'], index=None)
        instrutor = st.selectbox('Instrutor', ['Glauber', 'Martin'], index=None)
        quantidade = st.text_input('Quantidade')

    with colu2:
        equipagens = st.text_input('Equipagens')
        embarques = st.text_input('Embarques')
        curso = st.selectbox('Curso', ['OWD', 'ADV', 'REVIEW', 'RESCUE', 'PRIMEIROS SOCORROS', 'DIVEMASTER'],
                             index=None)
        pratica = st.selectbox('Pratica', ['Pratica 1', 'Pratica 2'], index=None)

    with st.expander('Segundo Curso'):
        colun1, colun2 = st.columns(2)
        with colun1:
            instrutor2 = st.selectbox('Instrutor2', ['Glauber', 'Martin'], index=None)
            quantidade2 = st.text_input('Quantidade2')

        with colun2:
            curso2 = st.selectbox('Curso2', ['OWD', 'ADV', 'REVIEW', 'RESCUE', 'PRIMEIROS SOCORROS', 'DIVEMASTER'],
                                  index=None)
            pratica2 = st.selectbox('Pratica2', ['Pratica 1', 'Pratica 2'], index=None)

    quentinha = st.selectbox('Pagar quentinhas nessa data?', ['Sim', 'Não'], index=None)

    if st.button('Lançar no Sistema'):
        # Lista de tuplas representando cada caso de inserção de lançamento de barco
        casos_insercao = [
            (staff_diferente1, quantidade_diferente1, '', '', 'BAT'),
            (staff_diferente2, quantidade_diferente2, '', '', 'BAT'),
            (apoio_superficie, equipagens, '', '', 'AS'),
            (mestre, embarques, '', '', 'CAPITAO'),
            (curso, quantidade, curso, pratica, 'CURSO'),
            (curso2, quantidade2, curso2, pratica2, 'CURSO'),
            (staffs_selecionados, divisao, '', '', 'BARCO')
        ]

        # Iterar sobre os casos e inserir os lançamentos de barco correspondentes
        for staff, quantidade, curso, pratica, funcao in casos_insercao:
            if staff is not None:
                index_lista_staffs = lista_staffs.index(staff)
                id_staff = select_nome_id_staff[index_lista_staffs][0]
                repo.insert_lancamento_barco(data, id_staff, funcao, quantidade, curso, pratica, 'PENDENTE', quentinha)

        st.success('Divisão Lançada no Sistema')

#         apoio_superficie = str(apoio_superficie).translate(str.maketrans('', '', chars2))
#
#         data_formatada = str(data).translate(str.maketrans('', '', chars)).split('-')
#         st.write('---')
#         lista_final = str(staffs_selecionados).translate(str.maketrans('', '', chars2))
#
#         texto_p1 = f"""
#                 *Divisão:*
#
#                 *{data_formatada[2]}/{data_formatada[1]}/{data_formatada[0]}*
#                 """
#         texto_p2 = f"""
#                 {divisao} - {lista_final}
#
#                 {apoio_superficie} - {equipagens} equipagens
#
#                 {mestre} - {embarques} embarques
#                 """
#         texto_curso = f"{instrutor} - {quantidade} {curso} {pratica}"
#         texto_curso2 = f"{instrutor2} - {quantidade2} {curso2} {pratica2}"
#
#         if instrutor is None and staff_diferente1 is None:  # Somente batismo sem staff extra
#
#             st.code(texto_p1 + texto_p2)
#
#         if instrutor is not None and staff_diferente1 is None and instrutor2 is None and staff_diferente2 is None:  # 1  curso
#             texto_curso = f"""
#                 {instrutor} - {quantidade} {curso} {pratica}
#
#                 {divisao} - {lista_final}
#
#                 {apoio_superficie} - {equipagens} equipagens
#
#                 {mestre} - {embarques} embarques"""
#             st.code(texto_p1 + texto_curso)
#
#         if instrutor2 is not None and staff_diferente1 is None and staff_diferente2 is None:  # 2 cursos
#             texto_curso_total = f"""
#                 {instrutor} - {quantidade} {curso} {pratica}
#                 {instrutor2} - {quantidade2} {curso2} {pratica2}
#
#                 """
#             st.code(texto_p1 + texto_curso_total + texto_p2)
#
#         if staff_diferente1 is not None and staff_diferente2 is None and instrutor is None and instrutor2 is None:  # 1 staff extra
#             texto_staff = f"""
#                 {quantidade_diferente1} - {staff_diferente1}
#
#                 {divisao} - {lista_final}
#
#                 {apoio_superficie} - {equipagens} equipagens
#
#                 {mestre} - {embarques} embarques"""
#             st.code(texto_p1 + texto_staff)
#
#         if staff_diferente1 is not None and staff_diferente2 is not None and instrutor is None and instrutor2 is None:  # 2 staffs extras e 1 curso
#             texto_staff2 = f"""
#                 {quantidade_diferente1} - {staff_diferente1}
#
#                 {quantidade_diferente2} - {staff_diferente2}
#
#                 {divisao} - {lista_final}
#
#                 {apoio_superficie} - {equipagens} equipagens
#
#                 {mestre} - {embarques} embarques"""
#             st.code(texto_p1 + texto_staff2)
#
#         if staff_diferente1 is not None and instrutor is not None and staff_diferente2 is None and instrutor2 is None:  # 1 staff extra e 1 curso
#             texto_staff = f"""
#                 {instrutor} - {quantidade} {curso} {pratica}
#
#                 {quantidade_diferente1} - {staff_diferente1}
#                 """
#             st.code(texto_p1 + texto_staff + texto_p2)
#
#         if staff_diferente1 is not None and instrutor is not None and instrutor2 is not None and staff_diferente2 is None:  # 1 staff extra e 2 cursos
#             texto_staff = f"""
#                 {instrutor} - {quantidade} {curso} {pratica}
#                 {instrutor2} - {quantidade2} {curso2} {pratica2}
#
#                 {quantidade_diferente2} - {staff_diferente1}
#                 """
#             st.code(texto_p1 + texto_staff + texto_p2)
#
#         if staff_diferente1 is not None and staff_diferente2 is not None and instrutor is not None and instrutor2 is not None:  # 2 staffs extra e 2 cursos
#             texto_staff_curso2 = f"""
#                 {instrutor} - {quantidade} {curso} {pratica}
#                 {instrutor2} - {quantidade2} {curso2} {pratica2}
#
#                 {quantidade_diferente1} - {staff_diferente1}
#                 {quantidade_diferente2} - {staff_diferente2}
#                 """
#             st.code(texto_p1 + texto_staff_curso2 + texto_p2)
#
#         if staff_diferente1 is not None and staff_diferente2 is not None and instrutor is not None and instrutor2 is None:  # 1 curso e 2 staffs extras
#             texto_staff_curso = f"""
#                 {instrutor} - {quantidade} {curso} {pratica}
#
#                 {quantidade_diferente1} - {staff_diferente1}
#                 {quantidade_diferente2} - {staff_diferente2}
#                 """
#             st.code(texto_p1 + texto_staff_curso + texto_p2)
#
# if escolha == 'Deletar':
#     st.title('Deletar Lançamentos')
#     st.subheader('Selecione o lançamento para deletar')
#     data1 = st.date_input('Selecione a Data', format='DD/MM/YYYY')
#     if st.button('Apagar do Sistema'):
#         cursor.execute(f"Delete from lancamentos_barco where data = '{data1}'")
#         mydb.commit()
#         st.success('Lançamento Deletado com Sucesso')
#
# if escolha == 'Editar':
#     st.title('Editar Lançamentos')
#     data2 = st.date_input('Selecione a data para editar', format='DD/MM/YYYY')
#
#     cursor.execute(f"SELECT staffs.nome, lancamentos_barco.quantidade, lancamentos_barco.quentinha from "
#                    f"lancamentos_barco JOIN staffs ON lancamentos_barco.id_staff = staffs.id_staff where data = "
#                    f"'{data2}' and lancamentos_barco.funcao != 'CURSO'")
#     resultado = cursor.fetchall()
#
#     df = pd.DataFrame(resultado, columns=['Nome', 'Quantidade', 'Almoço'])
#
#     cursor.execute(
#         f"SELECT staffs.nome, lancamentos_barco.curso, lancamentos_barco.quantidade, lancamentos_barco.pratica, lancamentos_barco.quentinha from lancamentos_barco JOIN staffs ON lancamentos_barco.id_staff = staffs.id_staff where data = '{data2}' and lancamentos_barco.funcao = 'CURSO'")
#     resultado = cursor.fetchall()
#
#     df2 = pd.DataFrame(resultado, columns=['Nome', 'Curso', 'Quantidade', 'Pratica', 'Almoço'])
#
#     df_final2 = st.data_editor(df2, key="editable_df2", hide_index=True)
#
#     df_final = st.data_editor(df, key="editable_df", hide_index=True)
#
#     if st.button('Editar Lançamento'):
#         if df_final is not None and not df_final.equals(df):
#             for index, row in df_final.iterrows():
#                 nome = row['Nome']
#                 quantidade = row['Quantidade']
#                 quentinha = row['Almoço']
#                 cursor.execute(f"SELECT id_staff FROM staffs WHERE nome = '{nome}'")
#                 id_staff_ed = cursor.fetchone()[0]
#                 # Gerar a instrução SQL UPDATE correspondente
#                 update_query = f"UPDATE lancamentos_barco SET quantidade = {quantidade}, quentinha = '{quentinha}' " \
#                                f"WHERE data = '{data2}' AND id_staff = {id_staff_ed} AND funcao != 'CURSO'"
#
#                 # Executar a instrução SQL UPDATE
#                 cursor.execute(update_query)
#
#                 # Commit para aplicar as alterações no banco de dados
#             mydb.commit()
#
#         if df_final2 is not None and not df_final2.equals(df2):
#             for index, row in df_final2.iterrows():
#                 nome = row['Nome']
#                 curso = row['Curso']
#                 pratica = row['Pratica']
#                 quantidade = row['Quantidade']
#                 quentinha = row['Almoço']
#                 cursor.execute(f"SELECT id_staff FROM staffs WHERE nome = '{nome}'")
#                 id_staff_ed = cursor.fetchone()[0]
#                 # Gerar a instrução SQL UPDATE correspondente
#                 update_query = f"UPDATE lancamentos_barco SET quantidade = {quantidade}, curso = '{curso}', pratica = '{pratica}', quentinha = '{quentinha}' " \
#                                f"WHERE data = '{data2}' AND id_staff = {id_staff_ed} AND funcao = 'CURSO'"
#
#                 # Executar a instrução SQL UPDATE
#                 cursor.execute(update_query)
#
#                 # Commit para aplicar as alterações no banco de dados
#             mydb.commit()
#         st.success('Lançamentos editados com sucesso!')
