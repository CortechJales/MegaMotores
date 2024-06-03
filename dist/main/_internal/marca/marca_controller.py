from database.database import Database
class MarcaController:
    def __init__(self):
        self.db = Database()    
    
    def create_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS marca (
        id INTEGER PRIMARY KEY,
        nome TEXT,
        ativo BOOLEAN
         )
        '''
        self.db.create_table(sql)

    def ListarMarca(self):
        query = 'SELECT * FROM marca'
        return self.db.execute_query(query)
       
    def FiltraMarca(self,tipo):
        query = 'SELECT * FROM marca where ativo=?'
        data = (tipo,)
        return self.db.execute_query(query,data)
    
    def CadastrarMarca(self, nome ):
        query = 'INSERT INTO marca (nome,ativo) VALUES (?, ?)'
        data = ( nome, True)
        self.db.execute_query_no_return(query, data)
    
    def EditarMarca(self, nome, id):    
        query = 'UPDATE marca SET nome=? WHERE id=?'
        data = (nome, id)
        self.db.execute_query_no_return(query, data)
    
    def DeletarMarca(self, id):    
        query = 'DELETE FROM marca WHERE id=?'
        data = (id,)
        self.db.execute_query_no_return(query, data)
    
    def InativarMarca(self,id):
        query = 'UPDATE marca SET ativo=? WHERE id=?'
        data = (0, id)
        self.db.execute_query_no_return(query, data)

    def AtivarMarca(self,id):
        query = 'UPDATE marca SET ativo=? WHERE id=?'
        data = (1, id)
        self.db.execute_query_no_return(query, data)
    
    def ValidarMarca(self,id):
        query = 'SELECT ativo FROM marca WHERE id=?'
        data = (id,)
        return self.db.execute_query(query, data)
    def BuscarMarca(self):
        query = "SELECT id, nome FROM marca WHERE ativo=1"
        result = self.db.execute_query(query)
        return result
    
        