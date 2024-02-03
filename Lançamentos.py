import streamlit as st
import pandas as pd
import os
import mysql.connector
from streamlit_option_menu import option_menu

mydb = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USERNAME"),
    passwd=os.getenv("DB_PASSWORD"),
    db=os.getenv("DB_NAME"),
    autocommit=True)

cursor = mydb.cursor(buffered=True)

chars = "'),([]"
chars2 = "')([]"
cursor.execute(
    "SELECT nome FROM staffs where status ='Ativo' and  ocupacao ='Divemaster' or status ='Ativo' and ocupacao ='Instrutor'")
lista_staffs = str(cursor.fetchall()).translate(str.maketrans('', '', chars)).split()
staffs_selecionados = []
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
    st.subheader('Divisão Diaria')
    data = st.date_input('Data:', format='DD/MM/YYYY')
    st.text('STAFFS:')

    for i, item in enumerate(lista_staffs):
        done = st.checkbox(str(item), key=str(i))

        if done:
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

    colun1, colun2, colun3 = st.columns(3)

    with colun1:
        st.number_input('Quantidade de AS')

    with colun2:
        apoio_superficie = st.multiselect('Apoio de Superficie', ['Manu', 'Catatau', 'Juninho', 'Glauber', 'Roberta'])

    with colun3:
        equipagens = st.text_input('Equipagens')

    colu1, colu2 = st.columns(2)

    with colu1:
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



    almoco = st.selectbox('Pagar quentinhas nessa data?', ['Sim', 'Não'], index=None)

    botao = st.button('Lançar no Sistema')
    if botao:
        if staff_diferente1 is not None:
            cursor.execute(f"SELECT id_staff FROM staffs WHERE nome = '{staff_diferente1}'")
            id_staff_1 = (str(cursor.fetchone()).translate(str.maketrans('', '', chars)))
            funcao = 'BAT'
            situacao = 'PENDENTE'
            cursor.execute(
                'INSERT INTO lancamentos_barco (data, id_staff, funcao, quantidade,situacao, quentinha) VALUES (%s, %s, %s, %s, %s, %s)',
                (data, id_staff_1, funcao, quantidade_diferente1, situacao, almoco))

        if staff_diferente2 is not None:
            cursor.execute(f"SELECT id_staff FROM staffs WHERE nome = '{staff_diferente2}'")
            id_staff_2 = (str(cursor.fetchone()).translate(str.maketrans('', '', chars)))
            situacao = 'PENDENTE'
            funcao = 'BAT'
            cursor.execute(
                'INSERT INTO lancamentos_barco (data, id_staff, funcao, quantidade,situacao, quentinha) VALUES (%s, %s, %s, %s, %s, %s)',
                (data, id_staff_2, funcao, quantidade_diferente2, situacao, almoco))

        if apoio_superficie is not None:
            situacao = 'PENDENTE'
            funcao = 'AS'
            for staff in apoio_superficie:
                cursor.execute(f"SELECT id_staff FROM staffs WHERE nome = '{staff}'")
                id_as = (str(cursor.fetchone()).translate(str.maketrans('', '', chars)))

                cursor.execute(
                    "INSERT INTO lancamentos_barco(data, id_staff, funcao, quantidade, situacao, quentinha) VALUES (%s, %s, %s, %s, %s, %s)",
                    (data, id_as, funcao, equipagens, situacao, almoco))
                mydb.commit()
        if mestre is not None:
            cursor.execute(f"SELECT id_staff FROM staffs WHERE nome = '{mestre}'")
            id_staff_mestre = (str(cursor.fetchone()).translate(str.maketrans('', '', chars)))
            situacao = 'PENDENTE'
            funcao = 'CAPITAO'
            cursor.execute(
                "INSERT INTO lancamentos_barco(data, id_staff, funcao, quantidade, situacao, quentinha) VALUES (%s, %s, %s, %s, %s, %s)",
                (data, id_staff_mestre, funcao, embarques, situacao, almoco))
            mydb.commit()

        if curso is not None:
            cursor.execute(f"SELECT id_staff FROM staffs WHERE nome = '{instrutor}'")
            id_staff = (str(cursor.fetchone()).translate(str.maketrans('', '', chars)))
            situacao = 'PENDENTE'
            funcao = 'CURSO'
            cursor.execute(
                "INSERT INTO lancamentos_barco(data, id_staff, funcao, curso, quantidade, pratica, situacao, quentinha) VALUES ("
                "%s, %s, %s, %s, %s, %s, %s, %s)",
                (data, id_staff, funcao, curso, quantidade, pratica, situacao, almoco))
            mydb.commit()

        if curso2 is not None:
            cursor.execute(f"SELECT id_staff FROM staffs WHERE nome = '{instrutor2}'")
            id_staff = (str(cursor.fetchone()).translate(str.maketrans('', '', chars)))
            situacao = 'PENDENTE'
            funcao = 'CURSO'
            cursor.execute(
                "INSERT INTO lancamentos_barco(data, id_staff, funcao, curso, quantidade, pratica, situacao, quentinha) VALUES ("
                "%s, %s, %s, %s, %s, %s, %s, %s)",
                (data, id_staff, funcao, curso2, quantidade2, pratica2, situacao, almoco))
            mydb.commit()

        for i, nome_staff in enumerate(staffs_selecionados):
            nome = str(nome_staff)
            cursor.execute(f"SELECT id_staff FROM staffs WHERE nome = '{nome}'")
            id_staff = (str(cursor.fetchone()).translate(str.maketrans('', '', chars)))
            situacao = 'PENDENTE'
            funcao = 'BAT'
            cursor.execute(
                'INSERT INTO lancamentos_barco (data, id_staff, funcao, quantidade, situacao, quentinha) VALUES (%s, %s, %s, %s, %s, %s)',
                (data, id_staff, funcao, divisao, situacao, almoco))
            mydb.commit()


        st.success('Divisão Lançada no Sistema')

        data_formatada = str(data).translate(str.maketrans('', '', chars)).split('-')
        st.write('---')
        lista_final = str(staffs_selecionados).translate(str.maketrans('', '', chars2))

        texto_p1 = f"""
                *Divisão:*
    
                *{data_formatada[2]}/{data_formatada[1]}/{data_formatada[0]}*
                """
        texto_p2 = f"""
                {divisao} - {lista_final}
                
                {apoio_superficie} - {equipagens} equipagens
                
                {mestre} - {embarques} embarques
                """
        texto_curso = f"{instrutor} - {quantidade} {curso} {pratica}"
        texto_curso2 = f"{instrutor2} - {quantidade2} {curso2} {pratica2}"

        if instrutor is None and staff_diferente1 is None:  # Somente batismo sem staff extra

            st.code(texto_p1 + texto_p2)

        if instrutor is not None and staff_diferente1 is None and instrutor2 is None and staff_diferente2 is None:  # 1  curso
            texto_curso = f"""
                {instrutor} - {quantidade} {curso} {pratica}
                
                {divisao} - {lista_final}
                
                {apoio_superficie} - {equipagens} equipagens
                
                {mestre} - {embarques} embarques"""
            st.code(texto_p1 + texto_curso)

        if instrutor2 is not None and staff_diferente1 is None and staff_diferente2 is None:  # 2 cursos
            texto_curso_total = f"""
                {instrutor} - {quantidade} {curso} {pratica}
                {instrutor2} - {quantidade2} {curso2} {pratica2}
                
                """
            st.code(texto_p1 + texto_curso_total + texto_p2)

        if staff_diferente1 is not None and staff_diferente2 is None and instrutor is None and instrutor2 is None:  # 1 staff extra
            texto_staff = f"""
                {quantidade_diferente1} - {staff_diferente1}
                
                {divisao} - {lista_final}
                
                {apoio_superficie} - {equipagens} equipagens
                
                {mestre} - {embarques} embarques"""
            st.code(texto_p1 + texto_staff)

        if staff_diferente1 is not None and staff_diferente2 is not None and instrutor is None and instrutor2 is None:  # 2 staffs extras e 1 curso
            texto_staff2 = f"""
                {quantidade_diferente1} - {staff_diferente1} 
                
                {quantidade_diferente2} - {staff_diferente2} 
                
                {divisao} - {lista_final}
                
                {apoio_superficie} - {equipagens} equipagens
                
                {mestre} - {embarques} embarques"""
            st.code(texto_p1 + texto_staff2)

        if staff_diferente1 is not None and instrutor is not None and staff_diferente2 is None and instrutor2 is None:  # 1 staff extra e 1 curso
            texto_staff = f"""
                {instrutor} - {quantidade} {curso} {pratica}
                
                {quantidade_diferente1} - {staff_diferente1}
                """
            st.code(texto_p1 + texto_staff + texto_p2)

        if staff_diferente1 is not None and instrutor is not None and instrutor2 is not None and staff_diferente2 is None:  # 1 staff extra e 2 cursos
            texto_staff = f"""
                {instrutor} - {quantidade} {curso} {pratica}
                {instrutor2} - {quantidade2} {curso2} {pratica2}
                
                {quantidade_diferente2} - {staff_diferente1} 
                """
            st.code(texto_p1 + texto_staff + texto_p2)

        if staff_diferente1 is not None and staff_diferente2 is not None and instrutor is not None and instrutor2 is not None:  # 2 staffs extra e 2 cursos
            texto_staff_curso2 = f"""
                {instrutor} - {quantidade} {curso} {pratica}
                {instrutor2} - {quantidade2} {curso2} {pratica2}
                
                {quantidade_diferente1} - {staff_diferente1}
                {quantidade_diferente2} - {staff_diferente2}  
                """
            st.code(texto_p1 + texto_staff_curso2 + texto_p2)

        if staff_diferente1 is not None and staff_diferente2 is not None and instrutor is not None and instrutor2 is None:  # 1 curso e 2 staffs extras
            texto_staff_curso = f"""
                {instrutor} - {quantidade} {curso} {pratica}
    
                {quantidade_diferente1} - {staff_diferente1}
                {quantidade_diferente2} - {staff_diferente2}
                """
            st.code(texto_p1 + texto_staff_curso + texto_p2)

if escolha == 'Deletar':
    st.title('Deletar Lançamentos')
    st.subheader('Selecione o lançamento para deletar')
    data1 = st.date_input('Selecione a Data', format='DD/MM/YYYY')
    if st.button('Apagar do Sistema'):
        cursor.execute(f"Delete from lancamentos_barco where data = '{data1}'")
        mydb.commit()
        st.success('Lançamento Deletado com Sucesso')

if escolha == 'Editar':
    st.title('Editar Lançamentos')
    data2 = st.date_input('Selecione a data para editar', format='DD/MM/YYYY')

    cursor.execute(f"SELECT staffs.nome, lancamentos_barco.quantidade, lancamentos_barco.quentinha from "
                   f"lancamentos_barco JOIN staffs ON lancamentos_barco.id_staff = staffs.id_staff where data = "
                   f"'{data2}' and lancamentos_barco.funcao != 'CURSO'")
    resultado = cursor.fetchall()

    df = pd.DataFrame(resultado, columns=['Nome', 'Quantidade', 'Almoço'])

    cursor.execute(
        f"SELECT staffs.nome, lancamentos_barco.curso, lancamentos_barco.quantidade, lancamentos_barco.pratica, lancamentos_barco.quentinha from lancamentos_barco JOIN staffs ON lancamentos_barco.id_staff = staffs.id_staff where data = '{data2}' and lancamentos_barco.funcao = 'CURSO'")
    resultado = cursor.fetchall()

    df2 = pd.DataFrame(resultado, columns=['Nome', 'Curso', 'Quantidade', 'Pratica', 'Almoço'])

    df_final2 = st.data_editor(df2, key="editable_df2", hide_index=True)

    df_final = st.data_editor(df, key="editable_df", hide_index=True)

    if st.button('Editar Lançamento'):
        if df_final is not None and not df_final.equals(df):
            for index, row in df_final.iterrows():
                nome = row['Nome']
                quantidade = row['Quantidade']
                quentinha = row['Almoço']
                cursor.execute(f"SELECT id_staff FROM staffs WHERE nome = '{nome}'")
                id_staff_ed = cursor.fetchone()[0]
                # Gerar a instrução SQL UPDATE correspondente
                update_query = f"UPDATE lancamentos_barco SET quantidade = {quantidade}, quentinha = '{quentinha}' " \
                               f"WHERE data = '{data2}' AND id_staff = {id_staff_ed} AND funcao != 'CURSO'"

                # Executar a instrução SQL UPDATE
                cursor.execute(update_query)

                # Commit para aplicar as alterações no banco de dados
            mydb.commit()

        if df_final2 is not None and not df_final2.equals(df2):
            for index, row in df_final2.iterrows():
                nome = row['Nome']
                curso = row['Curso']
                pratica = row['Pratica']
                quantidade = row['Quantidade']
                quentinha = row['Almoço']
                cursor.execute(f"SELECT id_staff FROM staffs WHERE nome = '{nome}'")
                id_staff_ed = cursor.fetchone()[0]
                # Gerar a instrução SQL UPDATE correspondente
                update_query = f"UPDATE lancamentos_barco SET quantidade = {quantidade}, curso = '{curso}', pratica = '{pratica}', quentinha = '{quentinha}' " \
                               f"WHERE data = '{data2}' AND id_staff = {id_staff_ed} AND funcao = 'CURSO'"

                # Executar a instrução SQL UPDATE
                cursor.execute(update_query)

                # Commit para aplicar as alterações no banco de dados
            mydb.commit()
        st.success('Lançamentos editados com sucesso!')
