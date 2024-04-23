class MainRepository:

    def __init__(self, db):
        self.db = db

    def select_staffs(self):
        query = """
        SELECT id_staff, nome, ocupacao 
        FROM staffs 
        where status ='Ativo' """

        return self.db.execute_query(query)

    def insert_lancamento_barco(self, data, id_staff, funcao, quantidade, curso, pratica, situacao, quentinha):
        query = """
        INSERT INTO lancamentos_barco 
        (data, id_staff, funcao, quantidade, curso, pratica, situacao, quentinha)
         VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (data, id_staff, funcao, quantidade, curso, pratica, situacao, quentinha)

        return self.db.execute_query(query, params)




