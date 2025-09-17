from database import SupabaseDB

class MainRepository:
    def __init__(self, db: SupabaseDB):
        self.db = db

    # -----------------------
    # SELECTS SIMPLES
    # -----------------------
    def select_id_staff_por_nome(self, nome):
        rows = self.db.execute_select("staffs", "id_staff", {"nome": nome})
        return rows

    def select_staffs(self):
        rows = self.db.execute_select("staffs", "id_staff, nome, ocupacao, comissao", {"status": "Ativo"})
        return rows

    def select_cilindros_cadastrados(self):
        rows = self.db.execute_select("cadastro_cilindro", "marca, num_serie, data_teste, situacao")
        return rows

    # -----------------------
    # RPC / FUNÇÕES COMPLEXAS
    # -----------------------
    def select_soma_total_comissoes(self, data_inicial, data_final):
        rows = self.db.rpc("fn_soma_total_comissoes", {"data_inicial": data_inicial, "data_final": data_final})
        return [tuple(row.values()) for row in rows] if rows else []

    def select_soma_comissao_individual(self, data_inicial, data_final, id_staff):
        rows = self.db.rpc("fn_soma_comissao_individual", {
            "data_inicial": data_inicial,
            "data_final": data_final,
            "p_id_staff": id_staff
        })
        return [tuple(row.values()) for row in rows] if rows else []

    def select_contagem_cilindros(self, data_inicial, data_final, id_staff):
        rows = self.db.rpc("fn_contagem_cilindros", {
            "data_inicial": data_inicial,
            "data_final": data_final,
            "p_id_staff": id_staff
        })
        return [tuple(row.values()) for row in rows] if rows else []

    # -----------------------
    # INSERTS
    # -----------------------
    def insert_lancamento_barco(self, data, id_staff, funcao, quantidade, curso, pratica, situacao, diaria):
        data_dict = {
            "data": data,
            "id_staff": id_staff,
            "funcao": funcao,
            "quantidade": quantidade,
            "curso": curso,
            "pratica": pratica,
            "situacao": situacao,
            "diaria": diaria
        }
        return self.db.insert("lancamentos_barco", data_dict)

    def insert_controle_quentinhas(self, data, id_staff):
        data_dict = {"data": data, "id_staff": id_staff, "quentinha": "Sim"}
        return self.db.insert("controle_quentinhas", data_dict)

    def insert_lancamento_cilindro(self, data, id_staff, inicio, final, quantidade_acqua, quantidade_pl, situacao, h3, m1):
        data_dict = {
            "data": data,
            "id_staff": id_staff,
            "horario_inicio": inicio,
            "horario_final": final,
            "cilindros_acqua": quantidade_acqua,
            "cilindros_pl": quantidade_pl,
            "situacao": situacao,
            "horas_trabalhadas": h3,
            "media_tempo": m1
        }
        return self.db.insert("lancamento_cilindro", data_dict)

    def insert_staff(self, nome, telefone, ocupacao, tipo, salario, comissao, status):
        data_dict = {
            "nome": nome,
            "telefone": telefone,
            "ocupacao": ocupacao,
            "tipo": tipo,
            "salario": salario,
            "comissao": comissao,
            "status": status
        }
        return self.db.insert("staffs", data_dict)

    # -----------------------
    # DELETE
    # -----------------------
    def delete_lancamentos_barco(self, data):
        return self.db.delete("lancamentos_barco", {"data": data})
