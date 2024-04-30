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
            id_staff,
            COALESCE(SUM(cilindros_acqua + cilindros_pl), 0) AS quantidade_cilindro,
            COUNT(DISTINCT data) AS diarias
        FROM lancamento_cilindro
        WHERE data BETWEEN '2024-04-01' AND '2024-04-30'
        GROUP BY id_staff
    ),
    SomaQuentinhas AS (
        SELECT
            id_staff,
            SUM(CASE WHEN quentinha = 'Sim' THEN 1 ELSE 0 END) AS quantidade_quentinha
        FROM controle_quentinhas
        WHERE data BETWEEN '2024-04-01' AND '2024-04-30'
        GROUP BY id_staff
    )
    SELECT
        staffs.nome,
        SUM(CASE WHEN l.funcao = 'BAT' THEN l.quantidade ELSE 0 END) AS quantidade_bat,
        SUM(CASE WHEN l.funcao = 'BAT' THEN l.quantidade * staffs.comissao ELSE 0 END) AS total_bat,
        SUM(CASE WHEN l.funcao = 'AS' THEN l.quantidade ELSE 0 END) AS quantidade_as,
        SUM(CASE WHEN l.funcao = 'CAPITAO' THEN l.quantidade ELSE 0 END) AS quantidade_capitao,
        SUM(CASE WHEN l.funcao = 'CURSO' THEN l.quantidade ELSE 0 END) AS quantidade_curso,
        SUM(CASE WHEN l.funcao = 'CURSO' THEN
            CASE
                WHEN l.curso IN ('OWD', 'ADV') THEN l.quantidade * 75
                WHEN l.curso = 'RESCUE' THEN l.quantidade * 150
                WHEN l.curso = 'REVIEW' THEN l.quantidade * 120
                WHEN l.curso = 'DIVEMASTER' THEN l.quantidade * 200
                ELSE 0
            END
        ELSE 0 END) AS total_curso,
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
                CASE WHEN sc.diarias != 0 AND staffs.tipo != 'FIXO' THEN 50 ELSE 0 END +
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
    WHERE l.data BETWEEN '2024-04-01' AND '2024-04-30'
    GROUP BY staffs.nome;





        """
        params = (data_incial, data_final, data_incial, data_final)
        return self.db.execute_query(query, params)

    def select_soma_comissao_individual(self, data_inicial, data_final, id_staff):
        query = """
        WITH SomaQuentinha as  (
            SELECT 
            data as data,
            id_staff as id_staff,
            quentinha as quentinha
            from controle_quentinhas
            where data between %s and %s and id_staff = %s)
            
        SELECT 
            DATE_FORMAT(lb.data, '%d/%m/%Y') AS data, 
            MAX(CASE WHEN lb.funcao = 'BAT' THEN lb.quantidade * staffs.comissao ELSE 0 END) AS total_bat,
            MAX(CASE WHEN lb.funcao = 'BAT' THEN lb.quantidade ELSE 0 END) AS quantidade_bat,
            MAX(CASE WHEN lb.funcao = 'AS' THEN lb.quantidade ELSE 0 END) AS total_as,
            MAX(CASE WHEN lb.funcao = 'CAPITAO' THEN lb.quantidade ELSE 0 END) AS total_capitao,
            MAX(CASE WHEN lb.funcao = 'CURSO' and lb.curso IN ('OWD', 'ADV') THEN lb.quantidade else 0 end) as quantidade_owd_adv,
            MAX(CASE WHEN lb.curso = 'RESCUE' THEN lb.quantidade else 0 end) as quantidade_rescue,
            MAX(CASE WHEN lb.curso = 'REVIEW' THEN lb.quantidade else 0 end) as quantidade_review,
            MAX(CASE WHEN lb.curso = 'DIVEMASTER' THEN lb.quantidade else 0 end) as quantidade_divemaster,
            CASE WHEN cq.quentinha = 'Sim' Then 1 else 0 end as quantidade_quentinha
        FROM lancamentos_barco AS lb
        LEFT JOIN staffs ON staffs.id_staff = lb.id_staff 
        LEFT JOIN SomaQuentinha as cq ON cq.id_staff = lb.id_staff and cq.data = lb.data
        WHERE lb.data BETWEEN %s AND %s and lb.id_staff = %s
        GROUP BY lb.data
        order by lb.data asc

        """

        params = (data_inicial, data_final, id_staff, data_inicial, data_final, id_staff)

        return self.db.execute_query(query, params)

    def insert_lancamento_barco(self, data, id_staff, funcao, quantidade, curso, pratica, situacao, quentinha):
        query = """
        INSERT INTO lancamentos_barco 
        (data, id_staff, funcao, quantidade, curso, pratica, situacao, quentinha)
         VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (data, id_staff, funcao, quantidade, curso, pratica, situacao, quentinha)

        return self.db.execute_query(query, params)
