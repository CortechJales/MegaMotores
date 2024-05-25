from database.database import Database
class ItemOrdemController:
    def __init__(self):
        self.db = Database('database/gerenciamento_ordens_servico.db')    
    
    def create_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS itens_ordem (
                      id INTEGER PRIMARY KEY,
                      ordem_id INTEGER,
                      produto_id INTEGER,
                      quantidade INTEGER,
                      FOREIGN KEY(ordem_id) REFERENCES ordens_servico(id),
                      FOREIGN KEY(produto_id) REFERENCES produtos(id)
                      )
        '''
        self.db.create_table(sql)
        
    def ListarItemOrdem(self, ordem_id):
        query = '''SELECT 
    itens_ordem.id AS id_item,
    produto.descricao AS produto_nome,
    itens_ordem.quantidade AS quantidade,
    printf('%.2f', produto.valor) AS valor_unitario,
    printf('%.2f', ROUND(SUM(CAST(produto.valor AS NUMERIC(10,2)) * itens_ordem.quantidade), 2)) AS valor_total
FROM 
    itens_ordem 
LEFT JOIN 
    ordens_servico ON ordens_servico.id = itens_ordem.ordem_id 
LEFT JOIN 
    produto ON itens_ordem.produto_id = produto.id 
WHERE 
    ordens_servico.id = ?
GROUP BY 
    itens_ordem.id;



'''
        data = (ordem_id,)
        result = self.db.execute_query(query, data)
        itensOrdem = [{'id_item': row[0],'produto_nome': row[1],'quantidade': row[2],'valor_unitario': row[3],'valor_total': row[4]} for row in result]
        return itensOrdem
    
    def CarregarItemOrdem(self, id):
        query = 'SELECT * FROM itens_ordem where id=?'
        data = (id,)
        return self.db.execute_query(query,data)
       
    def CadastrarItemOrdem(self, ordem_id, produto_id, quantidade ):
        query = '''
            INSERT INTO itens_ordem 
            ( ordem_id, produto_id, quantidade) 
            VALUES (?, ?, ?)
        '''
        data = (ordem_id, produto_id, quantidade)
        self.db.execute_query_no_return(query, data)

    def EditarItemOrdem(self, produto_id, quantidade, id):
        query = '''
            UPDATE itens_ordem 
            SET ordem_id=?, produto_id=?, quantidade=?
            WHERE id=?
        '''
        data = ( id, produto_id, quantidade, id)
        self.db.execute_query_no_return(query, data)
    
    def DeletarItemOrdem(self, id):    
        query = 'DELETE FROM itens_ordem WHERE id=?'
        data = (id,)
        self.db.execute_query_no_return(query, data)
    
    