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
    WITH SomaCilindros AS (
        SELECT
            lc.id_staff,
            COALESCE(SUM(cilindros_acqua + cilindros_pl), 0) AS quantidade_cilindro
        FROM lancamento_cilindro as lc
        LEFT JOIN staffs s ON lc.id_staff = s.id_staff
        WHERE data BETWEEN %s AND %s
        GROUP BY lc.id_staff
    ),
    SomaQuentinhas AS (
        SELECT
            id_staff,
            SUM(CASE WHEN quentinha = 'Sim' THEN 1 ELSE 0 END) AS quantidade_quentinha
        FROM controle_quentinhas
        WHERE data BETWEEN %s AND %s
        GROUP BY id_staff
    )
    SELECT
        staffs.nome,
        SUM(CASE WHEN l.funcao = 'BAT' THEN l.quantidade ELSE 0 END) AS quantidade_bat,
        SUM(CASE WHEN l.funcao = 'AS' THEN l.quantidade ELSE 0 END) AS quantidade_as,
        SUM(CASE WHEN l.funcao = 'CAPITAO' THEN l.quantidade ELSE 0 END) AS quantidade_capitao,
        SUM(CASE WHEN l.funcao = 'CURSO' THEN l.quantidade ELSE 0 END) AS quantidade_curso,
        COALESCE(sc.quantidade_cilindro, 0) AS quantidade_cilindro,
        COALESCE(cq.quantidade_quentinha, 0) as quantidade_quentinha,
        COALESCE(sc.diarias, 0) AS diarias,
        FORMAT(
            SUM(
                CASE WHEN l.funcao = 'BAT' THEN l.quantidade * staffs.comissao
                     WHEN l.funcao = 'AS' THEN l.quantidade * 1
                     WHEN l.funcao = 'CAPITAO' THEN l.quantidade * 1
                     ELSE 0
                END +
                CASE WHEN cq.quantidade_quentinha != 0 THEN 15 ELSE 0 END +
                CASE WHEN sc.diarias != 0  THEN 50 ELSE 0 END +
                CASE 
                    WHEN l.funcao = 'CURSO' THEN
                        CASE
                            WHEN l.curso IN ('OWD', 'ADV') THEN l.quantidade * 75
                            WHEN l.curso = 'RESCUE' THEN l.quantidade * 150
                            WHEN l.curso = 'REVIEW' THEN l.quantidade * 120
                            WHEN l.curso = 'DIVEMASTER' THEN l.quantidade * 200
                            ELSE 0
                        END
                    ELSE 0
                END
            ), 2, 'de_DE'
        ) AS total_formatado
    FROM lancamentos_barco AS l
    LEFT JOIN staffs ON staffs.id_staff = l.id_staff
    LEFT JOIN SomaCilindros AS sc ON sc.id_staff = l.id_staff
    LEFT JOIN SomaQuentinhas as cq ON cq.id_staff = staffs.id_staff
    WHERE l.data BETWEEN %s AND %s
    GROUP BY staffs.nome;





        """
        params = (data_incial, data_final, data_incial, data_final, data_incial, data_final)
        return self.db.execute_query(query, params)

    def select_soma_comissao_individual(self, data_inicial, data_final, id_staff):
        query = """
        WITH SomaQuentinha AS (
            SELECT 
                data AS data,
                id_staff AS id_staff,
                quentinha AS quentinha
            FROM controle_quentinhas
            WHERE data BETWEEN %s AND %s AND id_staff = %s
        )
        
        SELECT 
            DATE_FORMAT(lb.data, '%d/%m/%Y') AS data, 
            staffs.comissao,
            CASE WHEN lb.funcao = 'BAT' THEN 
                CASE WHEN ROUND(lb.quantidade, 0) = lb.quantidade THEN FORMAT(lb.quantidade, 0) 
                     ELSE FORMAT(lb.quantidade, 2) END
            ELSE 0 END AS quantidade_bat,
            CASE WHEN lb.funcao = 'AS' THEN 
                CASE WHEN ROUND(lb.quantidade, 0) = lb.quantidade THEN FORMAT(lb.quantidade, 0) 
                     ELSE FORMAT(lb.quantidade, 2) END
            ELSE 0 END AS total_as,
            CASE WHEN lb.funcao = 'CAPITAO' THEN 
                CASE WHEN ROUND(lb.quantidade, 0) = lb.quantidade THEN FORMAT(lb.quantidade, 0) 
                     ELSE FORMAT(lb.quantidade, 2) END
            ELSE 0 END AS total_capitao,
            CASE WHEN lb.funcao = 'CURSO' THEN 
                CASE WHEN ROUND(lb.quantidade, 0) = lb.quantidade THEN FORMAT(lb.quantidade, 0) 
                     ELSE FORMAT(lb.quantidade, 2) END
            ELSE 0 END AS quantidade_curso,
            lb.curso,
            CASE WHEN lb.pratica IS NOT NULL THEN lb.pratica ELSE '' END AS pratica,
            CASE WHEN cq.quentinha = 'Sim' THEN 1 ELSE 0 END AS quantidade_quentinha,
            0 AS cilindros_acqua,
            0 AS cilindros_pl,
            staffs.comissao_review,
            0 AS diaria
        FROM 
            lancamentos_barco AS lb
        LEFT JOIN 
            staffs ON staffs.id_staff = lb.id_staff 
        LEFT JOIN 
            SomaQuentinha AS cq ON cq.id_staff = lb.id_staff AND cq.data = lb.data
        WHERE 
            lb.data BETWEEN %s AND %s AND lb.id_staff = %s

        """
        params = (data_inicial, data_final, id_staff, data_inicial, data_final, id_staff)

        return self.db.execute_query(query, params)

    def select_contagem_cilindros(self, data_inicial, data_final, id_staff):
        query = """
        WITH SomaQuentinha AS (
            SELECT 
                data AS data,
                id_staff AS id_staff,
                quentinha AS quentinha
            FROM controle_quentinhas
            WHERE data BETWEEN %s AND %s AND id_staff = %s
        )
        SELECT 
            DATE_FORMAT(lb.data, '%d/%m/%Y') AS data, 
            '0' AS comissao,
            '0' AS quantidade_bat,
            '0' AS total_as,
            '0' AS total_capitao,
            '0' AS quantidade_curso,
            '0' AS curso,
            '0' AS pratica,
            CASE WHEN cq.quentinha = 'Sim' THEN 1 ELSE 0 END AS quantidade_quentinha,
            lb.cilindros_acqua AS cilindros_acqua,
            lb.cilindros_pl AS cilindros_pl,
            0 AS comissao_review,
            CASE WHEN staffs.tipo = 'FREELANCER' THEN 1 ELSE 0 END AS diaria
        FROM 
            lancamento_cilindro as lb
        LEFT JOIN 
            SomaQuentinha AS cq ON cq.id_staff = lb.id_staff AND cq.data = lb.data
        LEFT JOIN
            staffs ON staffs.id_staff = lb.id_staff
        
        WHERE 
            lb.data BETWEEN %s AND %s AND lb.id_staff = %s
        ORDER BY lb.data
        """

        params = (data_inicial, data_final, id_staff, data_inicial, data_final, id_staff)

        return self.db.execute_query(query, params)

    def insert_lancamento_barco(self, data, id_staff, funcao, quantidade, curso, pratica, situacao):
        query = """
        INSERT INTO lancamentos_barco 
        (data, id_staff, funcao, quantidade, curso, pratica, situacao)
         VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (data, id_staff, funcao, quantidade, curso, pratica, situacao)

        return self.db.execute_query(query, params)

    def insert_controle_quentinhas(self, data, id_staff):

        query = """
        INSERT INTO controle_quentinhas ( data, id_staff, quentinha) VALUES (%s, %s, %s)
        """
        params = (data, id_staff, 'Sim')

        return self.db.execute_query(query, params)

    def delete_lancamentos_barco(self, data):

        query = "DELETE FROM lancamentos_barco WHERE data = %s"
        params = (data, )
        return self.db.execute_query(query, params)
