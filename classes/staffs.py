import streamlit as st
from datetime import date, datetime


class Staffs:
    def __init__(self, repo, casos_insercao):
        self.repo = repo
        self.casos_insercao = casos_insercao

    def logica_inserir(self, lista_staffs_total, select_nome_id_staff, quentinha, data):
        # Converte data para string ISO, caso seja um objeto date
        if isinstance(data, (date, datetime)):
            data_iso = data.isoformat()
        else:
            data_iso = data

        for item in self.casos_insercao:
            staff, quantidade, curso, pratica, funcao, diaria = item

            # Se staff for uma lista
            if isinstance(staff, list):
                for nome_staff in staff:
                    try:
                        index_lista_staffs = lista_staffs_total.index(nome_staff)
                        id_staff = select_nome_id_staff[index_lista_staffs][0]

                        self.repo.insert_lancamento_barco(
                            data_iso, id_staff, funcao, quantidade, curso, pratica, 'PENDENTE', diaria
                        )

                        if quentinha == 'Sim':
                            self.repo.insert_controle_quentinhas(data_iso, id_staff)

                    except ValueError:
                        st.error(
                            f"Nome '{nome_staff}' não encontrado na lista de staffs ativos, o lançamento desse staff não foi feito"
                        )
                    except Exception as e:
                        st.error(f'Erro ao inserir lançamento do staff {nome_staff}: {e}')

            # Se staff for único
            elif staff is not None:
                try:
                    index_lista_staffs = lista_staffs_total.index(staff)
                    id_staff = select_nome_id_staff[index_lista_staffs][0]

                    if quentinha == 'Sim':
                        self.repo.insert_controle_quentinhas(data_iso, id_staff)

                    self.repo.insert_lancamento_barco(
                        data_iso, id_staff, funcao, quantidade, curso, pratica, 'PENDENTE', diaria
                    )

                except ValueError:
                    st.error(
                        f"Nome '{staff}' não encontrado na lista de staffs ativos, o lançamento desse staff não foi feito"
                    )
                except Exception as e:
                    st.error(f'Erro ao inserir lançamento do staff {staff}: {e}')

    def formatar_mensagem(self, data):
        """
        Formata a mensagem dos lançamentos com base nos casos_insercao.
        """

        # Converte data para string legível
        if isinstance(data, (date, datetime)):
            data_str = data.strftime('%d/%m/%Y')
        else:
            data_str = str(data)

        # Desempacotando itens (assumindo que cada tupla tem 6 elementos)
        staff_diferente1, quantidade_diferente1, _, _, _, _ = self.casos_insercao[0]
        staff_diferente2, quantidade_diferente2, _, _, _, _ = self.casos_insercao[1]
        apoio_superficie, equipagens, _, _, _, _ = self.casos_insercao[2]
        mestre, embarques, _, _, _, _ = self.casos_insercao[3]
        instrutor, quantidade, curso, pratica, _, _ = self.casos_insercao[4]
        instrutor2, quantidade2, curso2, pratica2, _, _ = self.casos_insercao[5]
        staffs_selecionados, divisao, _, _, _, _ = self.casos_insercao[6]

        texto_p1 = f"*Divisão:*\n\n*{data_str}*\n\n"
        texto_p2 = ''

        # Adiciona instrutores
        if instrutor:
            texto_p2 += f"{instrutor} - {quantidade} {curso} {pratica}\n\n"

        if instrutor2:
            texto_p2 += f"{instrutor2} - {quantidade2} {curso2} {pratica2}\n\n"

        # Adiciona staffs diferentes
        if staff_diferente1:
            texto_p2 += f"{quantidade_diferente1} - {staff_diferente1}\n\n"

        if staff_diferente2:
            texto_p2 += f"{quantidade_diferente2} - {staff_diferente2}\n\n"

        # Adiciona divisão
        if staffs_selecionados and divisao:
            texto_p2 += f"{divisao} - {', '.join(staffs_selecionados)}\n\n"

        # Adiciona apoio na superfície
        if apoio_superficie:
            texto_p2 += f"{', '.join(apoio_superficie)} - {equipagens} equipagens\n\n"

        # Adiciona mestre
        if mestre:
            texto_p2 += f"{mestre} - {embarques} embarques\n\n"

        # Exibe a mensagem completa
        st.code(texto_p1 + texto_p2)
