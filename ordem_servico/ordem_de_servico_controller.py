from database.database import Database
class OrdemDeServicoController:
    def __init__(self):
        self.db = Database()    
    
    def create_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS ordens_servico (
                      id INTEGER PRIMARY KEY,
                      cliente_id INTEGER,
                      equipamento_id INTEGER,
                      data_inicio DATA,
                      data_final DATA,
                      mao_de_obra NUMERIC(10, 2),
                      observacao TEXT,
                      fechada BOOLEAN,
                      ativo BOOLEAN,
                      orcamento BOOLEAN,
                      orcamento_passado	DATA,
                      orcamento_aprovado DATA,
                      FOREIGN KEY(cliente_id) REFERENCES cliente(id),
                      FOREIGN KEY(equipamento_id) REFERENCES equipamento_cliente(id)
                      )'''
       
        self.db.create_table(sql)
        
    
    def ListarTodasOrdemServico(self, tipo,orcamento):
        query = '''SELECT 
                    ordens_servico.id AS id_ordem,
                    cliente.nome AS nome_cliente,
                    equipamento_cliente.modelo AS modelo_equipamento,
                    ordens_servico.data_inicio,
                    ordens_servico.data_final,
                    ordens_servico.mao_de_obra,
                    CASE 
                        WHEN COALESCE(SUM(CAST(itens_ordem.valor_unitario AS NUMERIC(10,2)) * itens_ordem.quantidade), 0) = 0 THEN ordens_servico.mao_de_obra
                        ELSE ROUND(
                            ordens_servico.mao_de_obra + SUM(CAST(itens_ordem.valor_unitario AS NUMERIC(10,2)) * itens_ordem.quantidade), 2
                        )
                    END AS valor_total,
                    ordens_servico.observacao,
                    ordens_servico.ativo
                    FROM 
                        ordens_servico 
                    JOIN 
                        cliente ON ordens_servico.cliente_id = cliente.id 
                    JOIN 
                        equipamento_cliente ON ordens_servico.equipamento_id = equipamento_cliente.id 
                    LEFT JOIN 
                        itens_ordem ON ordens_servico.id = itens_ordem.ordem_id 
                        
                    WHERE
                        ordens_servico.orcamento=? AND ordens_servico.orcamento=?
                    GROUP BY 
                        ordens_servico.id;

                '''
        
        data = (tipo,orcamento)
        return self.db.execute_query(query,data)
    
    def CarregarOrdemServico(self, id):
        query = 'SELECT * FROM ordens_servico where id=?'
        data = (id,)
        return self.db.execute_query(query,data)
    def ListarOrdemServico(self, id):
        query = ''' SELECT 
                    ordens_servico.id AS id_ordem,
                    cliente.nome AS nome_cliente,
                    equipamento_cliente.modelo AS modelo_equipamento,
                    ordens_servico.data_inicio,
                    ordens_servico.data_final,
                    printf('%.2f', ordens_servico.mao_de_obra) AS mao_de_obra,
                    CASE 
                        WHEN COALESCE(SUM(CAST(itens_ordem.valor_unitario AS NUMERIC(10,2)) * itens_ordem.quantidade), 0) = 0 THEN printf('%.2f', ordens_servico.mao_de_obra)
                        ELSE printf('%.2f', ROUND(ordens_servico.mao_de_obra + SUM(CAST(itens_ordem.valor_unitario AS NUMERIC(10,2)) * itens_ordem.quantidade), 2))
                    END AS valor_total,
                    ordens_servico.observacao,
                    ordens_servico.orcamento_passado,
                    ordens_servico.orcamento_aprovado,
                    ordens_servico.ativo
                    FROM 
                        ordens_servico 
                    JOIN 
                        cliente ON ordens_servico.cliente_id = cliente.id 
                    JOIN 
                        equipamento_cliente ON ordens_servico.equipamento_id = equipamento_cliente.id 
                    LEFT JOIN 
                        itens_ordem ON ordens_servico.id = itens_ordem.ordem_id 
                    WHERE 
                        ordens_servico.ativo = 1 and ordens_servico.id=? 
                    GROUP BY 
                        ordens_servico.id;
                '''
        data = (id,)
        return self.db.execute_query(query,data)
    
    def FiltrarOrdemServico(self, tipo,orcamento,aberto):
        query = ''' SELECT 
                    ordens_servico.id AS id_ordem,
                    cliente.nome AS nome_cliente,
                    equipamento_cliente.modelo AS modelo_equipamento,
                    ordens_servico.data_inicio,
                    ordens_servico.data_final,
                    printf('%.2f', ordens_servico.mao_de_obra) AS mao_de_obra,
                    CASE 
                        WHEN COALESCE(SUM(CAST(itens_ordem.valor_unitario AS NUMERIC(10,2)) * itens_ordem.quantidade), 0) = 0 THEN printf('%.2f', ordens_servico.mao_de_obra)
                        ELSE printf('%.2f', ROUND(ordens_servico.mao_de_obra + SUM(CAST(itens_ordem.valor_unitario AS NUMERIC(10,2)) * itens_ordem.quantidade), 2))
                    END AS valor_total,
                    ordens_servico.observacao,
                    ordens_servico.orcamento_passado,
                    ordens_servico.orcamento_aprovado,
                    ordens_servico.ativo
                    FROM 
                        ordens_servico 
                    JOIN 
                        cliente ON ordens_servico.cliente_id = cliente.id 
                    JOIN 
                        equipamento_cliente ON ordens_servico.equipamento_id = equipamento_cliente.id 
                    LEFT JOIN 
                        itens_ordem ON ordens_servico.id = itens_ordem.ordem_id 
                    WHERE 
                        ordens_servico.ativo = ?  AND  ordens_servico.orcamento= ? AND ordens_servico.fechada=?
                    GROUP BY 
                        ordens_servico.id;
'''
        data = (tipo,orcamento,aberto)
        return self.db.execute_query(query, data)
    
    
    def CadastrarOrdemServico(self, cliente, equipamento, data_inicio, mao_de_obra,observacao,orcamento):
        query = '''
            INSERT INTO ordens_servico 
            (cliente_id, equipamento_id, data_inicio, mao_de_obra,observacao,orcamento, fechada, ativo) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        '''
        data = (cliente, equipamento, data_inicio, mao_de_obra,observacao,orcamento, False, True)
        self.db.execute_query_no_return(query, data)

    def EditarOrdemServico(self, cliente, equipamento, data_inicio, mao_de_obra,observacao, id):
        query = '''
        UPDATE ordens_servico 
        SET cliente_id = ?,
            equipamento_id = ?,
            data_inicio = ?,
            mao_de_obra = ?,
            observacao = ?
        WHERE id = ?
    '''
        data = (cliente, equipamento, data_inicio, mao_de_obra,observacao, id)
        self.db.execute_query_no_return(query, data)
    
    def DeletarOrdemServico(self, id):    
        query = 'DELETE FROM ordens_servico WHERE id=?'
        data = (id,)
        self.db.execute_query_no_return(query, data)
    
    def InativarOrdemServico(self,id):
        query = 'UPDATE ordens_servico SET ativo=? WHERE id=?'
        data = (0, id)
        self.db.execute_query_no_return(query, data)

    def AtivarOrdemServico(self,id):
        query = 'UPDATE ordens_servico SET ativo=? WHERE id=?'
        data = (1, id)
        self.db.execute_query_no_return(query, data)
    
    def FecharOrdemServico(self,data_final,id):
        query = 'UPDATE ordens_servico SET fechada=?, data_final=? WHERE id=?'
        data = (1,data_final, id)
        self.db.execute_query_no_return(query, data)

    def OrcamentoOrdemServico(self,id):
        query = 'UPDATE ordens_servico SET orcamento=? WHERE id=?'
        data = (1, id)
        self.db.execute_query_no_return(query, data)
    
    def AbrirOrdemServico(self,id):
        query = 'UPDATE ordens_servico SET fechada=?, data_final=? WHERE id=?'
        data = (0,None, id)
        self.db.execute_query_no_return(query, data)
    
    def AprovarOrcamento(self, data_orcamento, id):
        query = 'UPDATE ordens_servico SET orcamento=?, orcamento_aprovado=? WHERE id=?'
        data = (0, data_orcamento, id)
        try:
            self.db.execute_query_no_return(query, data)
            return True
        except Exception as e:
            print(f"Erro ao aprovar orçamento: {str(e)}")
            return False
    
    def NegarOrcamento(self,data_final,id):
        query = 'UPDATE ordens_servico SET fechada=?, data_final=? WHERE id=?'
        data = (1,data_final, id)
        try:
            self.db.execute_query_no_return(query, data)
            return True
        except Exception as e:
            print(f"Erro ao aprovar orçamento: {str(e)}")
            return False
    
    def PassarOrcamento(self,data_orcamento,id):
        query = 'UPDATE ordens_servico SET  orcamento_passado=? WHERE id=?'
        data = (data_orcamento, id)
        try:
            self.db.execute_query_no_return(query, data)
            return True
        except Exception as e:
            print(f"Erro ao aprovar orçamento: {str(e)}")
            return False
    def ValidarOrdemServico(self,id):
        query = 'SELECT ativo FROM ordens_servico WHERE id=?'
        data = (id,)
        return self.db.execute_query(query, data)
    
    def ValidarOrdemPassadaAoCliente(self, id):
        query = 'SELECT orcamento_passado FROM ordens_servico WHERE id = ?'
        data = (id,)
        result = self.db.execute_query(query, data)

        if result and result[0][0] is not None:
            return True
        else:
            return False
    def ValidarOrdemServicoFechada(self,id):
        query = 'SELECT fechada FROM ordens_servico WHERE id=?'
        data = (id,)
        return self.db.execute_query(query, data)
   
    def CalcularTotal(self,id):
        query = '''
            SELECT   
        ROUND(os.mao_de_obra + CAST(SUM(CAST(p.valor AS REAL) * io.quantidade) AS REAL), 2) AS valor_total_ordem
        FROM 
        ordens_servico AS os
        LEFT JOIN 
        itens_ordem AS io ON os.id = io.ordem_id
        LEFT JOIN 
        produto AS p ON io.produto_id = p.id
        WHERE 
        os.id = ?
        GROUP BY 
        os.id;
        '''
        data = (id,)
        return self.db.execute_query(query, data)
    def CarregarImpressaoOrdem(self,id):
        query = '''SELECT 
                    ordens_servico.id AS id_ordem,
                    ordens_servico.cliente_id AS cliente_id,
                    ordens_servico.equipamento_id AS equipamento_id,
                    ordens_servico.data_inicio,
                    ordens_servico.data_final,
                    printf('%.2f', ordens_servico.mao_de_obra) AS mao_de_obra,
                    CASE 
                        WHEN COALESCE(SUM(CAST(itens_ordem.valor_unitario AS NUMERIC(10,2)) * itens_ordem.quantidade), 0) = 0 THEN printf('%.2f', ordens_servico.mao_de_obra)
                        ELSE printf('%.2f', ROUND(ordens_servico.mao_de_obra + SUM(CAST(itens_ordem.valor_unitario AS NUMERIC(10,2)) * itens_ordem.quantidade), 2))
                    END AS valor_total,
                    printf('%.2f', COALESCE(SUM(CAST(itens_ordem.valor_unitario AS NUMERIC(10,2)) * itens_ordem.quantidade), 0)) AS total_itens_ordem,
                    ordens_servico.observacao,
                    ordens_servico.orcamento_passado,
                    ordens_servico.orcamento_aprovado
                FROM 
                    ordens_servico 
                LEFT JOIN 
                    itens_ordem ON ordens_servico.id = itens_ordem.ordem_id 
                WHERE 
                    ordens_servico.ativo = 1 AND ordens_servico.id = ? 
                GROUP BY 
                    ordens_servico.id;'''
        data = (id,)
        return self.db.execute_query(query, data)
    
    def LimparCamposOrcamento(self, id_ordem):
        query = 'UPDATE ordens_servico SET orcamento_passado = NULL, orcamento_aprovado = NULL WHERE id = ?'
        data = (id_ordem,)
        self.db.execute_query_no_return(query, data)