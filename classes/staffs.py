import streamlit as st


class Staffs:

    def __init__(self, repo, casos_insercao):
        self.repo = repo
        self.casos_insercao = casos_insercao

    def logica_inserir(self, lista_staffs_total, select_nome_id_staff, quentinha, data):

        for staff, quantidade, curso, pratica, funcao in self.casos_insercao:
            # Verifica se staff é uma lista
            if isinstance(staff, list):
                # Itera sobre cada nome na lista
                for nome_staff in staff:
                    try:
                        index_lista_staffs = lista_staffs_total.index(nome_staff)
                        id_staff = select_nome_id_staff[index_lista_staffs][0]
                        self.repo.insert_lancamento_barco(data, id_staff, funcao, quantidade, curso, pratica,
                                                          'PENDENTE', quentinha)
                    except ValueError:
                        # Lida com o caso em que o nome do staff não está na lista
                        st.error(
                            f"Nome '{nome_staff}' não encontrado na lista de staffs ativos, o lançamento desse staff "
                            f"não foi feito")
            elif staff is not None:
                try:
                    index_lista_staffs = lista_staffs_total.index(staff)
                    id_staff = select_nome_id_staff[index_lista_staffs][0]
                    self.repo.insert_lancamento_barco(data, id_staff, funcao, quantidade, curso, pratica, 'PENDENTE',
                                                      quentinha)
                except ValueError:
                    # Lida com o caso em que o nome do staff não está na lista
                    st.error(
                        f"Nome '{staff}' não encontrado na lista de staffs ativos, o lançamento desse staff não foi "
                        f"feito")

    def formatar_mensagem(self, data):

        staff_diferente1, quantidade_diferente1, _, _, _ = self.casos_insercao[0]
        staff_diferente2, quantidade_diferente2, _, _, _ = self.casos_insercao[1]
        apoio_superficie, equipagens, _, _, _ = self.casos_insercao[2]
        mestre, embarques, _, _, _ = self.casos_insercao[3]
        instrutor, quantidade, curso, pratica, _ = self.casos_insercao[4]
        instrutor2, quantidade2, curso2, pratica2, _ = self.casos_insercao[5]
        staffs_selecionados, divisao, _, _, _ = self.casos_insercao[6]

        texto_p1 = f"*Divisão:*\n\n*{data.strftime('%d/%m/%Y')}*\n\n"
        texto_p2 = ''

        # Verifica se há instrutor e adiciona à mensagem
        if instrutor:
            texto_curso = f"{instrutor} - {quantidade} {curso} {pratica}\n\n"
            texto_p2 += texto_curso

        # Verifica se há instrutor2 e adiciona à mensagem
        if instrutor2:
            texto_curso2 = f"{instrutor2} - {quantidade2} {curso2} {pratica2}\n\n"
            texto_p2 += texto_curso2

        # Verifica se há staff_diferente1 e adiciona à mensagem
        if staff_diferente1:
            texto_staff = f"{quantidade_diferente1} - {staff_diferente1}\n\n"
            texto_p2 += texto_staff

        # Verifica se há staff_diferente2 e adiciona à mensagem
        if staff_diferente2:
            texto_staff2 = f"{quantidade_diferente2} - {staff_diferente2}\n\n"
            texto_p2 += texto_staff2

        # Adiciona a divisão à mensagem
        texto_divisao = f"{divisao} - {', '.join(staffs_selecionados)}\n\n"
        texto_p2 += texto_divisao

        # Verifica se há apoio_superficie e adiciona à mensagem
        if apoio_superficie:
            texto_apoio = f"{', '.join(apoio_superficie)} - {equipagens} equipagens\n\n"
            texto_p2 += texto_apoio

        # Verifica se há mestre e adiciona à mensagem
        if mestre:
            texto_mestre = f"{mestre} - {embarques} embarques\n\n"
            texto_p2 += texto_mestre

        # Exibe a mensagem completa
        st.code(texto_p1 + texto_p2)
