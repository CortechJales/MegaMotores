from database.database import Database

class ItemOrdemController:
    def __init__(self):
        self.db = Database()    
    
    def create_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS itens_ordem (
            id INTEGER PRIMARY KEY,
            ordem_id INTEGER,
            produto_id INTEGER,
            quantidade INTEGER,
            valor_unitario REAL,
            FOREIGN KEY(ordem_id) REFERENCES ordens_servico(id),
            FOREIGN KEY(produto_id) REFERENCES produtos(id)
        )
        '''
        self.db.create_table(sql)
        
    def ListarItemOrdem(self, ordem_id):
        # Força substituição de vírgula por ponto antes do CAST para REAL,
        # e calcula valor total por item multiplicando valor_unitario * quantidade
        query = '''
            SELECT 
                itens_ordem.id AS id_item,
                produto.descricao AS produto_nome,
                itens_ordem.quantidade AS quantidade,
                printf('%.2f', CAST(REPLACE(itens_ordem.valor_unitario, ',', '.') AS REAL)) AS valor_unitario,
                printf('%.2f', CAST(REPLACE(itens_ordem.valor_unitario, ',', '.') AS REAL) * itens_ordem.quantidade) AS valor_total
            FROM 
                itens_ordem 
            LEFT JOIN 
                produto ON itens_ordem.produto_id = produto.id 
            WHERE 
                itens_ordem.ordem_id = ?
            ORDER BY 
                itens_ordem.id;
        '''
        data = (ordem_id,)
        result = self.db.execute_query(query, data)
        itensOrdem = [
            {
                'id_item': row[0],
                'produto_nome': row[1],
                'quantidade': row[2],
                'valor_unitario': row[3],
                'valor_total': row[4]
            }
            for row in result
        ]
        return itensOrdem
    
    def CarregarItemOrdem(self, id):
        # Carrega bruto (mantém formato salvo)
        query = 'SELECT * FROM itens_ordem WHERE id = ?'
        data = (id,)
        return self.db.execute_query(query, data)
       
    def CadastrarItemOrdem(self, ordem_id, produto_id, quantidade, valor_unitario):
        query = '''
            INSERT INTO itens_ordem 
            (ordem_id, produto_id, quantidade, valor_unitario) 
            VALUES (?, ?, ?, ?)
        '''
        # garante que salvamos com ponto decimal
        valor_unitario_float = float(str(valor_unitario).replace(',', '.'))
        data = (ordem_id, produto_id, quantidade, valor_unitario_float)
        self.db.execute_query_no_return(query, data)

    def EditarItemOrdem(self, produto_id, quantidade, valor_unitario, id):
        query = '''
            UPDATE itens_ordem 
            SET produto_id = ?, quantidade = ?, valor_unitario = ?
            WHERE id = ?
        '''
        valor_unitario_float = float(str(valor_unitario).replace(',', '.'))
        data = (produto_id, quantidade, valor_unitario_float, id)
        self.db.execute_query_no_return(query, data)
    
    def DeletarItemOrdem(self, id):    
        query = 'DELETE FROM itens_ordem WHERE id = ?'
        data = (id,)
        self.db.execute_query_no_return(query, data)

    def CalcularTotalItens(self, ordem_id):
        """Retorna o total geral da ordem, somando todos os itens (com duas casas)."""
        query = '''
            SELECT 
                printf('%.2f', SUM(CAST(REPLACE(valor_unitario, ',', '.') AS REAL) * quantidade))
            FROM 
                itens_ordem
            WHERE 
                ordem_id = ?;
        '''
        data = (ordem_id,)
        result = self.db.execute_query(query, data)
        return result[0][0] if result and result[0][0] is not None else "0.00"
