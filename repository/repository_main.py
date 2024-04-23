
class MainRepository:

    def __init__(self, db):
        self.db = db

    def select_dm_instrutor(self):

        query = """
        SELECT id_staff, nome 
        FROM staffs 
        where status ='Ativo' and  ocupacao IN ('Divemaster', 'Instrutor')"""

        return self.db.execute_query(query)
