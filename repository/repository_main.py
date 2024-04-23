class MainRepository:

    def __init__(self, db):
        self.db = db

    def select_dm_instrutor(self):
        query = """
        SELECT id_staff, nome, ocupacao 
        FROM staffs 
        where status ='Ativo' and  ocupacao IN ('Divemaster', 'Instrutor')"""

        return self.db.execute_query(query)

    def insert_lancamento_barco(self, data, id_staff, funcao, quantidade, situacao, quentinha):
        query = """
        INSERT INTO lancamentos_barco 
        (data, id_staff, funcao, quantidade,situacao, quentinha)
         VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (data, id_staff, funcao, quantidade, situacao, quentinha)

        return self.db.execute_query(query, params)




