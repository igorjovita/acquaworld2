class MainRepository:

    def __init__(self, db):
        self.db = db

    def select_staffs(self):
        query = """
        SELECT id_staff, nome, ocupacao , comissao
        FROM staffs 
        where status ='Ativo' """

        return self.db.execute_query(query)

    def select_soma_total_comissoes(self, data_incial, data_final):
        query = """
        SELECT 
            CONCAT(
                 staffs.nome, ' - ',
                 CASE WHEN SUM(CASE WHEN l.funcao = 'BAT' THEN l.quantidade ELSE 0 END) > 0 THEN CONCAT(FORMAT(SUM(CASE WHEN l.funcao = 'BAT' THEN l.quantidade ELSE 0 END), 2), ' BAT + ') ELSE '' END,
                 CASE WHEN SUM(CASE WHEN l.funcao = 'AS' THEN l.quantidade ELSE 0 END) > 0 THEN CONCAT(FORMAT(SUM(CASE WHEN l.funcao = 'AS' THEN l.quantidade ELSE 0 END), 2), ' Equipagens + ') ELSE '' END,
                 CASE WHEN SUM(CASE WHEN l.funcao = 'CAPITAO' THEN l.quantidade ELSE 0 END) > 0 THEN CONCAT(FORMAT(SUM(CASE WHEN l.funcao = 'CAPITAO' THEN l.quantidade ELSE 0 END), 2), ' Embarques + ') ELSE '' END,
                 CASE WHEN SUM(CASE WHEN l.funcao = 'CURSO' THEN l.quantidade ELSE 0 END) > 0 THEN CONCAT(FORMAT(SUM(CASE WHEN l.funcao = 'CURSO' THEN l.quantidade ELSE 0 END), 2), ' Curso + ') ELSE '' END,
                 CASE WHEN COALESCE(SUM(lc.cilindros_acqua + lc.cilindros_pl), 0) > 0 THEN CONCAT(FORMAT(COALESCE(SUM(lc.cilindros_acqua + lc.cilindros_pl), 0), 2), ' Cilindros + ') ELSE '' END,
                 CASE WHEN SUM(CASE WHEN l.quentinha = 'Sim' OR lc.almoco = 'Sim' THEN 1 ELSE 0 END) > 0 THEN CONCAT(FORMAT(SUM(CASE WHEN l.quentinha = 'Sim' OR lc.almoco = 'Sim' THEN 1 ELSE 0 END), 2), ' Quentinhas = ') ELSE '' END,
                CONCAT('R$ : ', FORMAT(
                    SUM(
                        CASE 
                            WHEN l.id_staff IS NOT NULL THEN
                                CASE 
                                    WHEN l.funcao = 'BAT' THEN l.quantidade * staffs.comissao
                                    WHEN l.funcao = 'AS' THEN l.quantidade * 1
                                    WHEN l.funcao = 'CAPITAO' THEN l.quantidade * 1
                                    WHEN l.funcao = 'CURSO' THEN 
                                        CASE 
                                            WHEN l.curso IN ('OWD', 'ADV') THEN l.quantidade * 75
                                            WHEN l.curso = 'RESCUE' THEN l.quantidade * 150
                                            WHEN l.curso = 'REVIEW' THEN l.quantidade * 120
                                            WHEN l.curso = 'DIVEMASTER' THEN l.quantidade * 200
                                            ELSE 0
                                        END
                                    ELSE 0
                                END +
                                CASE 
                                    WHEN l.quentinha = 'Sim' THEN 15
                                    ELSE 0
                                END
                            ELSE
                                0
                        END
                    ), 2)
                )
            ) AS summary
        FROM 
            staffs
        LEFT JOIN 
            lancamentos_barco AS l ON staffs.id_staff = l.id_staff AND l.data BETWEEN %s AND %s
        LEFT JOIN 
            lancamento_cilindro AS lc ON staffs.id_staff = lc.id_staff AND l.data = lc.data
        WHERE 
            l.id_staff IS NOT NULL
        GROUP BY 
            staffs.nome;



        """
        params = (data_incial, data_final)
        return self.db.execute_query(query, params)

    def select_soma_comissao_individual(self, data_inicial, data_final, id_staff):
        query = """
        SELECT 
            CONCAT(
                 staffs.nome, ' - ',
                 CASE WHEN SUM(CASE WHEN l.funcao = 'BAT' THEN l.quantidade ELSE 0 END) > 0 THEN CONCAT(FORMAT(SUM(CASE WHEN l.funcao = 'BAT' THEN l.quantidade ELSE 0 END), 2), ' BAT + ') ELSE '' END,
                 CASE WHEN SUM(CASE WHEN l.funcao = 'AS' THEN l.quantidade ELSE 0 END) > 0 THEN CONCAT(FORMAT(SUM(CASE WHEN l.funcao = 'AS' THEN l.quantidade ELSE 0 END), 2), ' Equipagens + ') ELSE '' END,
                 CASE WHEN SUM(CASE WHEN l.funcao = 'CAPITAO' THEN l.quantidade ELSE 0 END) > 0 THEN CONCAT(FORMAT(SUM(CASE WHEN l.funcao = 'CAPITAO' THEN l.quantidade ELSE 0 END), 2), ' Embarques + ') ELSE '' END,
                 CASE WHEN SUM(CASE WHEN l.funcao = 'CURSO' THEN l.quantidade ELSE 0 END) > 0 THEN CONCAT(FORMAT(SUM(CASE WHEN l.funcao = 'CURSO' THEN l.quantidade ELSE 0 END), 2), ' Curso + ') ELSE '' END,
                 CASE WHEN COALESCE(SUM(lc.cilindros_acqua + lc.cilindros_pl), 0) > 0 THEN CONCAT(FORMAT(COALESCE(SUM(lc.cilindros_acqua + lc.cilindros_pl), 0), 2), ' Cilindros + ') ELSE '' END,
                 CASE WHEN SUM(CASE WHEN l.quentinha = 'Sim' OR lc.almoco = 'Sim' THEN 1 ELSE 0 END) > 0 THEN CONCAT(FORMAT(SUM(CASE WHEN l.quentinha = 'Sim' OR lc.almoco = 'Sim' THEN 1 ELSE 0 END), 2), ' Quentinhas = ') ELSE '' END,
                CONCAT('R$ : ', FORMAT(
                    SUM(
                        CASE 
                            WHEN l.id_staff IS NOT NULL THEN
                                CASE 
                                    WHEN l.funcao = 'BAT' THEN l.quantidade * staffs.comissao
                                    WHEN l.funcao = 'AS' THEN l.quantidade * 1
                                    WHEN l.funcao = 'CAPITAO' THEN l.quantidade * 1
                                    WHEN l.funcao = 'CURSO' THEN 
                                        CASE 
                                            WHEN l.curso IN ('OWD', 'ADV') THEN l.quantidade * 75
                                            WHEN l.curso = 'RESCUE' THEN l.quantidade * 150
                                            WHEN l.curso = 'REVIEW' THEN l.quantidade * 120
                                            WHEN l.curso = 'DIVEMASTER' THEN l.quantidade * 200
                                            ELSE 0
                                        END
                                    ELSE 0
                                END +
                                CASE 
                                    WHEN l.quentinha = 'Sim' THEN 15
                                    ELSE 0
                                END
                            ELSE
                                0
                        END
                    ), 2)
                )
            ) AS summary
        FROM 
            staffs
        LEFT JOIN 
            lancamentos_barco AS l ON staffs.id_staff = l.id_staff AND l.data BETWEEN %s AND %s
        LEFT JOIN 
            lancamento_cilindro AS lc ON staffs.id_staff = lc.id_staff AND l.data = lc.data
        WHERE 
            l.id_staff IS NOT NULL
        GROUP BY 
            staffs.nome;


        """

        params = (data_inicial, data_final, id_staff)

        return self.db.execute_query(query, params)

    def insert_lancamento_barco(self, data, id_staff, funcao, quantidade, curso, pratica, situacao, quentinha):
        query = """
        INSERT INTO lancamentos_barco 
        (data, id_staff, funcao, quantidade, curso, pratica, situacao, quentinha)
         VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (data, id_staff, funcao, quantidade, curso, pratica, situacao, quentinha)

        return self.db.execute_query(query, params)
