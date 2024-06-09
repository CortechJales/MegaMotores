from database.database import Database
class ProdutoController:
    def __init__(self):
        self.db = Database()    
    
    def create_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS produto (
        id INTEGER PRIMARY KEY,
        descricao TEXT,
        valor REAL,
        ativo BOOLEAN
         )
        '''
        self.db.create_table(sql)

    def ListarProduto(self):
        query = 'SELECT * FROM produto'
        return self.db.execute_query(query)
    
    
    def ValidarProdutoCadastrado(self, id):
        query = 'SELECT descricao FROM produto WHERE id=?'
        data = (id,)
        result = self.db.execute_query(query, data)

    # Se houver algum resultado, significa que o produto já está cadastrado
        if result:
            return True
        else:
            return False
    
    def FiltrarProduto(self,tipo):
        query = '''SELECT id,descricao,printf('%.2f', valor) AS valor, ativo FROM  produto WHERE     ativo = ?;'''
        data = (tipo,)
        return self.db.execute_query(query,data)
    
    def CadastrarProduto(self, descricao, valor, id):
        query = 'INSERT INTO produto (id,descricao, valor,ativo) VALUES (?, ?, ?, ?)'
        data = (id, descricao, valor, True)
        self.db.execute_query_no_return(query, data)
    
    def EditarProduto(self, descricao, valor, id):    
        query = 'UPDATE produto SET descricao=?, valor=? WHERE id=?'
        data = (descricao, valor, id)
        self.db.execute_query_no_return(query, data)
    
    def DeletarProduto(self, id):    
        query = 'DELETE FROM produto WHERE id=?'
        data = (id,)
        self.db.execute_query_no_return(query, data)
    
    def InativarProduto(self,id):
        query = 'UPDATE produto SET ativo=? WHERE id=?'
        data = (0, id)
        self.db.execute_query_no_return(query, data)

    def AtivarProduto(self,id):
        query = 'UPDATE produto SET ativo=? WHERE id=?'
        data = (1, id)
        self.db.execute_query_no_return(query, data)
    
    def ValidarProduto(self,id):
        query = 'SELECT ativo FROM produto WHERE id=?'
        data = (id,)
        return self.db.execute_query(query, data)
    
    def obter_valor_produto(self, id):
        query = '''SELECT valor FROM produto WHERE id = ?;'''
        data = (id,)
        result = self.db.execute_query(query, data)
        if result:
            return float(result[0][0])  # Retorna o valor do primeiro resultado, convertido para float
        else:
            return None
        