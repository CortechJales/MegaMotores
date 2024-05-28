from database.database import Database
class OrdemDeServicoController:
    def __init__(self):
        self.db = Database('database/gerenciamento_ordens_servico.db')    
    
    def create_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS ordens_servico (
                      id INTEGER PRIMARY KEY,
                      cliente_id INTEGER,
                      equipamento_id INTEGER,
                      data_inicio DATA,
                      data_final DATA,
                      mao_de_obra NUMERIC(10, 2),
                      fechada BOOLEAN,
                      ativo BOOLEAN,
                      FOREIGN KEY(cliente_id) REFERENCES cliente(id),
                      FOREIGN KEY(equipamento_id) REFERENCES equipamento_cliente(id)
                      )'''
       
        self.db.create_table(sql)
        
    
    def ListarOrdemServico(self):
        query = '''SELECT 
    ordens_servico.id AS id_ordem,
    cliente.nome AS nome_cliente,
    equipamento_cliente.modelo AS modelo_equipamento,
    ordens_servico.data_inicio,
    ordens_servico.data_final,
    ordens_servico.mao_de_obra,
    CASE 
        WHEN COALESCE(SUM(CAST(produto.valor AS NUMERIC(10,2)) * itens_ordem.quantidade), 0) = 0 THEN ordens_servico.mao_de_obra
        ELSE ROUND(
            ordens_servico.mao_de_obra + SUM(CAST(produto.valor AS NUMERIC(10,2)) * itens_ordem.quantidade), 2
        )
    END AS valor_total,
    ordens_servico.ativo
FROM 
    ordens_servico 
JOIN 
    cliente ON ordens_servico.cliente_id = cliente.id 
JOIN 
    equipamento_cliente ON ordens_servico.equipamento_id = equipamento_cliente.id 
LEFT JOIN 
    itens_ordem ON ordens_servico.id = itens_ordem.ordem_id 
LEFT JOIN 
    produto ON itens_ordem.produto_id = produto.id 
GROUP BY 
    ordens_servico.id;
 

                '''
        
        return self.db.execute_query(query)
    
    
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
        WHEN COALESCE(SUM(CAST(produto.valor AS NUMERIC(10,2)) * itens_ordem.quantidade), 0) = 0 THEN printf('%.2f', ordens_servico.mao_de_obra)
        ELSE printf('%.2f', ROUND(ordens_servico.mao_de_obra + SUM(CAST(produto.valor AS NUMERIC(10,2)) * itens_ordem.quantidade), 2))
    END AS valor_total,
    ordens_servico.ativo
FROM 
    ordens_servico 
JOIN 
    cliente ON ordens_servico.cliente_id = cliente.id 
JOIN 
    equipamento_cliente ON ordens_servico.equipamento_id = equipamento_cliente.id 
LEFT JOIN 
    itens_ordem ON ordens_servico.id = itens_ordem.ordem_id 
LEFT JOIN 
    produto ON itens_ordem.produto_id = produto.id 
WHERE 
    ordens_servico.ativo = 1 and ordens_servico.id=? 
GROUP BY 
    ordens_servico.id;
'''
        data = (id,)
        return self.db.execute_query(query,data)
    
    def FiltrarOrdemServico(self, tipo):
        query = '''SELECT 
    ordens_servico.id AS id_ordem,
    cliente.nome AS nome_cliente,
    equipamento_cliente.modelo AS modelo_equipamento,
    ordens_servico.data_inicio,
    ordens_servico.data_final,
    printf('%.2f', ordens_servico.mao_de_obra) AS mao_de_obra,
    CASE 
        WHEN COALESCE(SUM(CAST(produto.valor AS NUMERIC(10,2)) * itens_ordem.quantidade), 0) = 0 THEN printf('%.2f', ordens_servico.mao_de_obra)
        ELSE printf('%.2f', ROUND(ordens_servico.mao_de_obra + SUM(CAST(produto.valor AS NUMERIC(10,2)) * itens_ordem.quantidade), 2))
    END AS valor_total,
    ordens_servico.ativo
FROM 
    ordens_servico 
JOIN 
    cliente ON ordens_servico.cliente_id = cliente.id 
JOIN 
    equipamento_cliente ON ordens_servico.equipamento_id = equipamento_cliente.id 
LEFT JOIN 
    itens_ordem ON ordens_servico.id = itens_ordem.ordem_id 
LEFT JOIN 
    produto ON itens_ordem.produto_id = produto.id 
WHERE 
    ordens_servico.ativo = ? 
GROUP BY 
    ordens_servico.id;





'''
        data = (tipo,)
        return self.db.execute_query(query, data)
    
    def CadastrarOrdemServico(self, cliente, equipamento, data_inicio, mao_de_obra):
        query = '''
            INSERT INTO ordens_servico 
            (cliente_id, equipamento_id, data_inicio, mao_de_obra, fechada, ativo) 
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        data = (cliente, equipamento, data_inicio, mao_de_obra, False, True)
        self.db.execute_query_no_return(query, data)

    def EditarOrdemServico(self, cliente, equipamento, data_inicio, mao_de_obra, id):
        query = '''
        UPDATE ordens_servico 
        SET cliente_id = ?,
            equipamento_id = ?,
            data_inicio = ?,
            mao_de_obra = ?
        WHERE id = ?
    '''
        data = (cliente, equipamento, data_inicio, mao_de_obra, id)
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
    
    def ValidarOrdemServico(self,id):
        query = 'SELECT ativo FROM ordens_servico WHERE id=?'
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
    
        