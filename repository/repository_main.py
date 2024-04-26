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
                 SUM(CASE WHEN l.funcao = 'BAT' THEN l.quantidade ELSE 0 END), ' BAT', ' + ',
                'Equipagens: ', SUM(CASE WHEN l.funcao = 'AS' THEN l.quantidade ELSE 0 END), ' + ',
                'Embarques: ', SUM(CASE WHEN l.funcao = 'CAPITAO' THEN l.quantidade ELSE 0 END), ' + ',
                'Curso: ', SUM(CASE WHEN l.funcao = 'CURSO' THEN l.quantidade ELSE 0 END), ' + ',
                'Cilindros: ', COALESCE(SUM(lc.cilindros_acqua + lc.cilindros_pl), 0), ' + ',
                'Quentinhas: ', SUM(CASE WHEN MAX(l.quentinha = 'Sim' OR lc.almoco = 'Sim') THEN 1 ELSE 0 END), ' = ',
                'R$ : ', SUM(
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
                )
            ) AS summary
        FROM 
            staffs
        LEFT JOIN 
            lancamentos_barco AS l ON staffs.id_staff = l.id_staff AND l.data BETWEEN %s AND %s
        LEFT JOIN 
            lancamento_cilindro AS lc ON staffs.id_staff = lc.id_staff AND l.data = lc.data
        WHERE l.id_staff IS NOT NULL
        GROUP BY 
            staffs.nome;


        """
        params = (data_incial, data_final)
        return self.db.execute_query(query, params)

    def select_soma_comissao_individual(self, data_inicial, data_final, id_staff):
        query = """
        SELECT 
            CONCAT(
                DATE_FORMAT(lb.data, '%d/%m/%Y'),
                ' - ',
                GROUP_CONCAT(
                    CONCAT( 
                        IF(ROUND(lb.quantidade) = lb.quantidade, FORMAT(lb.quantidade, 0), FORMAT(lb.quantidade, 2)),
                        ' ',
                        CASE 
                            WHEN lb.funcao = 'CURSO' THEN CONCAT(lb.curso, ' ', IFNULL(lb.pratica, 'Pratica 1'))
                            ELSE lb.funcao
                        END
                    ) ORDER BY lb.data SEPARATOR ' + '
                ),
                CASE 
                    WHEN SUM(CASE WHEN lb.quentinha = 'Sim' THEN 1 ELSE 0 END) > 0 AND SUM(CASE WHEN lc.almoco = 'Sim' THEN 1 ELSE 0 END) > 0 THEN ' + quentinha'
                    WHEN SUM(CASE WHEN lb.quentinha = 'Sim' THEN 1 ELSE 0 END) > 0 THEN ' + quentinha'
                    WHEN SUM(CASE WHEN lc.almoco = 'Sim' THEN 1 ELSE 0 END) > 0 THEN ' + quentinha'
                    ELSE ''
                END,
                 CASE 
                    WHEN COUNT(lc.data) > 0 THEN
                        CASE
                            WHEN lc.cilindros_acqua <> 0 AND lc.cilindros_pl <> 0 THEN 
                                CONCAT(' + ', lc.cilindros_acqua, ' Cilindros Acqua + ', lc.cilindros_pl, ' Cilindros Pl')
                            WHEN lc.cilindros_acqua <> 0 THEN
                                CONCAT(' + ', lc.cilindros_acqua, ' Cilindros Acqua')
                            WHEN lc.cilindros_pl <> 0 THEN
                                CONCAT(' + ', lc.cilindros_pl, ' Cilindros Pl')
                            ELSE ''
                        END
                    ELSE ''
                END
            ) AS formatted_output,
            SUM(CASE WHEN lb.funcao = 'BAT' THEN lb.quantidade * staffs.comissao ELSE 0 END) AS total_bat,
            SUM(CASE WHEN lb.funcao = 'BAT' THEN lb.quantidade ELSE 0 END) AS quantidade_bat,
            SUM(CASE WHEN lb.funcao = 'AS' THEN lb.quantidade ELSE 0 END) AS total_as,
            SUM(CASE WHEN lb.funcao = 'CAPITAO' THEN lb.quantidade ELSE 0 END) AS total_capitao,
            SUM(CASE WHEN lb.funcao = 'CURSO' and lb.curso IN ('OWD', 'ADV') THEN lb.quantidade else 0 end) as quantidade_owd_adv,
            SUM(CASE WHEN lb.curso = 'RESCUE' THEN lb.quantidade else 0 end) as quantidade_rescue,
            SUM(CASE WHEN lb.curso = 'REVIEW' THEN lb.quantidade else 0 end) as quantidade_review,
            SUM(CASE WHEN lb.curso = 'DIVEMASTER' THEN lb.quantidade else 0 end) as quantidade_divemaster,
            CASE WHEN MAX(lb.quentinha = 'Sim' OR lc.almoco = 'Sim') THEN 15 ELSE 0 END AS total_quentinha_almoco
        FROM 
            lancamentos_barco lb
        LEFT JOIN
            lancamento_cilindro lc ON lb.id_staff = lc.id_staff AND lb.data = lc.data
        INNER JOIN staffs ON staffs.id_staff = lb.id_staff
        WHERE 
            lb.data BETWEEN %s AND %s AND lb.id_staff = %s
        GROUP BY
            lb.data
        ORDER BY
            lb.data;

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
