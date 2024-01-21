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
        staff_diferente1 = st.text_input('Staff1 - Lance o staff , quantidade').capitalize()
        staff_diferente2 = st.text_input('Staff2 - Lance o staff , quantidade').capitalize()

    colu1, colu2 = st.columns(2)

    with colu1:
        apoio_superficie = st.selectbox('Apoio de Superficie', ['Manu', 'Catatau', 'Juninho', 'Glauber', 'Roberta'], index=None)
        mestre = st.selectbox('Mestre', ['', 'Risadinha', 'Marquinhos', 'Freelancer'])
        instrutor = st.selectbox('Instrutor', ['', 'Glauber', 'Martin'])
        quantidade = st.text_input('Quantidade')

    with colu2:
        equipagens = st.text_input('Equipagens')
        embarques = st.text_input('Embarques')
        curso = st.selectbox('Curso', ['', 'OWD', 'ADV', 'REVIEW', 'RESCUE', 'PRIMEIROS SOCORROS', 'DIVEMASTER'])
        pratica = st.selectbox('Pratica', ['', 'Pratica 1', 'Pratica 2'])

    with st.expander('Segundo Curso'):
        colun1, colun2 = st.columns(2)
        with colun1:
            instrutor2 = st.selectbox('Instrutor2', ['', 'Glauber', 'Martin'])
            quantidade2 = st.text_input('Quantidade2')

        with colun2:
            curso2 = st.selectbox('Curso2', ['', 'OWD', 'ADV', 'REVIEW', 'RESCUE', 'PRIMEIROS SOCORROS', 'DIVEMASTER'])
            pratica2 = st.selectbox('Pratica2', ['', 'Pratica 1', 'Pratica 2'])

    cursor.execute(f"SELECT id_staff FROM staffs WHERE nome = '{apoio_superficie}'")
    id_as = (str(cursor.fetchone()).translate(str.maketrans('', '', chars)))

    almoco = st.selectbox('Pagar quentinhas nessa data?', ['Sim', 'Não'], index=None)

    botao = st.button('Lançar no Sistema')
    if botao:

        if staff_diferente1 != '':
            info_staff_diferente1 = staff_diferente1.split(',')
            cursor.execute(f"SELECT id_staff FROM staffs WHERE nome = '{info_staff_diferente1[0]}'")
            id_staff_1 = (str(cursor.fetchone()).translate(str.maketrans('', '', chars)))
            funcao = 'BAT'
            situacao = 'PENDENTE'
            divisao_1 = info_staff_diferente1[1]
            cursor.execute(
                'INSERT INTO lancamentos_barco (data, id_staff, funcao, quantidade,situacao, quentinha) VALUES (%s, %s, %s, %s, %s, %s)',
                (data, id_staff_1, funcao, divisao_1, situacao, almoco))

        if staff_diferente2 != '':
            info_staff_diferente2 = staff_diferente2.split(',')
            cursor.execute(f"SELECT id_staff FROM staffs WHERE nome = '{info_staff_diferente2[0]}'")
            id_staff_2 = (str(cursor.fetchone()).translate(str.maketrans('', '', chars)))
            situacao = 'PENDENTE'
            divisao_2 = info_staff_diferente2[1]
            funcao = 'BAT'
            cursor.execute(
                'INSERT INTO lancamentos_barco (data, id_staff, funcao, quantidade,situacao, quentinha) VALUES (%s, %s, %s, %s, %s, %s)',
                (data, id_staff_2, funcao, divisao_2, situacao, almoco))

        if apoio_superficie != '':
            situacao = 'PENDENTE'
            funcao = 'AS'
            cursor.execute("INSERT INTO lancamentos_barco(data, id_staff, funcao, quantidade, situacao, quentinha) VALUES (%s, %s, %s, %s, %s, %s)",
                           (data, id_as, funcao, equipagens, situacao, almoco))
            mydb.commit()
        if mestre != '':
            cursor.execute(f"SELECT id_staff FROM staffs WHERE nome = '{mestre}'")
            id_staff_mestre = (str(cursor.fetchone()).translate(str.maketrans('', '', chars)))
            situacao = 'PENDENTE'
            funcao = 'CAPITAO'
            cursor.execute("INSERT INTO lancamentos_barco(data, id_staff, funcao, quantidade, situacao, quentinha) VALUES (%s, %s, %s, %s, %s, %s)",
                           (data, id_staff_mestre, funcao, embarques, situacao, almoco))
            mydb.commit()

        if curso != '':
            cursor.execute(f"SELECT id_staff FROM staffs WHERE nome = '{instrutor}'")
            id_staff = (str(cursor.fetchone()).translate(str.maketrans('', '', chars)))
            situacao = 'PENDENTE'
            funcao = 'CURSO'
            cursor.execute("INSERT INTO lancamentos_barco(data, id_staff, funcao, curso, quantidade, pratica, situacao, quentinha) VALUES ("
                           "%s, %s, %s, %s, %s, %s, %s, %s)",
                           (data, id_staff, funcao, curso, quantidade, pratica, situacao, almoco))
            mydb.commit()

        if curso2 != '':
            cursor.execute(f"SELECT id_staff FROM staffs WHERE nome = '{instrutor2}'")
            id_staff = (str(cursor.fetchone()).translate(str.maketrans('', '', chars)))
            situacao = 'PENDENTE'
            funcao = 'CURSO'
            cursor.execute("INSERT INTO lancamentos_barco(data, id_staff, funcao, curso, quantidade, pratica, situacao, quentinha) VALUES ("
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

        if instrutor == '' and staff_diferente1 == '':  # Somente batismo sem staff extra

            st.code(texto_p1 + texto_p2)

        if instrutor != '' and staff_diferente1 == '' and instrutor2 == '' and staff_diferente2 == '':  # 1  curso
            texto_curso = f"""
                {instrutor} - {quantidade} {curso} {pratica}
                
                {divisao} - {lista_final}
                {apoio_superficie} - {equipagens} equipagens
                {mestre} - {embarques} embarques"""
            st.code(texto_p1 + texto_curso)

        if instrutor2 != '' and staff_diferente1 == '' and staff_diferente2 == '':  # 2 cursos
            texto_curso_total = f"""
                {instrutor} - {quantidade} {curso} {pratica}
                {instrutor2} - {quantidade2} {curso2} {pratica2}
                
                """
            st.code(texto_p1 + texto_curso_total + texto_p2)

        if staff_diferente1 != '' and staff_diferente2 == '' and instrutor == '' and instrutor2 == '':  # 1 staff extra
            staffd1_formatado = staff_diferente1.split(',')
            texto_staff = f"""
                {staffd1_formatado[1]} - {staffd1_formatado[0]}
                {divisao} - {lista_final}
                {apoio_superficie} - {equipagens} equipagens
                {mestre} - {embarques} embarques"""
            st.code(texto_p1 + texto_staff)

        if staff_diferente1 != '' and staff_diferente2 != '' and instrutor == '' and instrutor2 == '':  # 2 staffs extras e 1 curso
            staffd1_formatado = staff_diferente1.split(',')
            staffd2_formatado = staff_diferente2.split(',')
            texto_staff2 = f"""
                {staffd1_formatado[1]} - {staffd1_formatado[0]}
                {staffd2_formatado[1]} - {staffd2_formatado[0]}
                {divisao} - {lista_final}
                {apoio_superficie} - {equipagens} equipagens
                {mestre} - {embarques} embarques"""
            st.code(texto_p1 + texto_staff2)

        if staff_diferente1 != '' and instrutor != '' and staff_diferente2 == '' and instrutor2 == '':  # 1 staff extra e 1 curso
            staffd1_formatado = staff_diferente1.split(',')
            texto_staff = f"""
                {instrutor} - {quantidade} {curso} {pratica}
                
                {staffd1_formatado[1]} - {staffd1_formatado[0]}
                """
            st.code(texto_p1 + texto_staff + texto_p2)

        if staff_diferente1 != '' and instrutor != '' and instrutor2 != '' and staff_diferente2 == '':  # 1 staff extra e 2 cursos
            staffd1_formatado = staff_diferente1.split(',')
            texto_staff = f"""
                {instrutor} - {quantidade} {curso} {pratica}
                {instrutor2} - {quantidade2} {curso2} {pratica2}
                
                {staffd1_formatado[1]} - {staffd1_formatado[0]}
                """
            st.code(texto_p1 + texto_staff + texto_p2)

        if staff_diferente1 != '' and staff_diferente2 != '' and instrutor != '' and instrutor2 != '':  # 2 staffs extra e 2 cursos
            staffd1_formatado = staff_diferente1.split(',')
            staffd2_formatado = staff_diferente2.split(',')
            texto_staff_curso2 = f"""
                {instrutor} - {quantidade} {curso} {pratica}
                {instrutor2} - {quantidade2} {curso2} {pratica2}
                
                {staffd1_formatado[1]} - {staffd1_formatado[0]}
                {staffd2_formatado[1]} - {staffd2_formatado[0]}
                """
            st.code(texto_p1 + texto_staff_curso2 + texto_p2)

        if staff_diferente1 != '' and staff_diferente2 != '' and instrutor != '' and instrutor2 == '':  # 1 curso e 2 staffs extras
            staffd1_formatado = staff_diferente1.split(',')
            staffd2_formatado = staff_diferente2.split(',')
            texto_staff_curso = f"""
                {instrutor} - {quantidade} {curso} {pratica}
    
                {staffd1_formatado[1]} - {staffd1_formatado[0]}
                {staffd2_formatado[1]} - {staffd2_formatado[0]}
                """
            st.code(texto_p1 + texto_staff_curso + texto_p2)

if escolha == 'Deletar':
    st.title('Deletar Lançamentos')
    st.subheader('Selecione o lançamento para deletar')
    data1 = st.date_input('Selecione a Data', format='DD/MM/YYYY')
    l_bat = st.checkbox('Lançamento Bat')
    l_as = st.checkbox('Lançamento AS')
    l_mestre = st.checkbox('Lançamento Mestre')
    l_curso = st.checkbox('Lançamento Curso')
    if st.button('Apagar do Sistema'):
        mydb.connect()
        if l_bat:
            cursor.execute(f"delete from lancamento_bat where data = '{data1}'")
            mydb.commit()
        elif l_as:
            cursor.execute(f"delete from lancamento_as where data = '{data1}'")
            mydb.commit()
        elif l_mestre:
            cursor.execute(f"delete from lancamento_mestre where data = '{data1}'")
            mydb.commit()
        elif l_curso:
            cursor.execute(f"delete from lancamento_curso where data = '{data1}'")
            mydb.commit()
        st.success('Lançamento Deletado com Sucesso')

# if escolha == 'Editar':
#     st.title('Editar Lançamentos')
#     staffs = []
#     mydb.connect()
#     data1 = st.date_input('Selecione a data do lançamento')
#     cursor.execute(f"SELECT id_staff FROM lancamento_bat where data = '{data1}'")
#     id_staff = str(cursor.fetchall()).translate(str.maketrans('', '', chars)).split()
#     st.subheader(id_staff)
#     for item in id_staff:
#         cursor.execute(f"SELECT nome from staffs where id_staff = '{item}'")
#         staff = str(cursor.fetchone()).translate(str.maketrans('', '', chars))
#         st.checkbox(str(staff))
