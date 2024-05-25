from database.database import Database
class ClienteController:
    def __init__(self):
        self.db = Database('database/gerenciamento_ordens_servico.db')    
    
    def create_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS cliente (
        id INTEGER PRIMARY KEY,
        nome TEXT,
        cep TEXT,
        endereco TEXT,
        numero TEXT,
        cidade TEXT,
        estado TEXT,
        cpf_cnpj TEXT,
        telefone TEXT,
        ativo BOOLEAN
        )
        '''
        self.db.create_table(sql)
    def ListarCliente(self):
        query = 'SELECT * FROM cliente'
        return self.db.execute_query(query)
    
    def CarregarCliente(self, id):
        query = 'SELECT * FROM cliente where id=?'
        data = (id,)
        return self.db.execute_query(query,data)
    
    def FiltrarCliente(self,tipo):
        query = 'SELECT * FROM cliente where ativo=?'
        data = (tipo,)
        return self.db.execute_query(query,data)
    
    def CadastrarCliente(self, nome, cep, endereco, numero, cidade, estado, cpf_cnpj, telefone):
        query = 'INSERT INTO cliente (nome, cep, endereco,numero, cidade, estado, cpf_cnpj,telefone,ativo) VALUES (?, ?, ?, ?, ?,?, ?, ?, ?)'
        data = (nome, cep, endereco,numero, cidade, estado, cpf_cnpj, telefone, True)
        self.db.execute_query_no_return(query, data)
    
    def EditarCliente(self, nome, cep, endereco, numero, cidade, estado, cpf_cnpj, telefone,id):    
        query = 'UPDATE cliente SET nome=?, cep=?, endereco=?, numero=?, cidade=?, estado=?, cpf_cnpj=?, telefone=? WHERE id=?'
        data = (nome, cep, endereco, numero, cidade, estado, cpf_cnpj, telefone, id)
        self.db.execute_query_no_return(query, data)
    
    def DeletarCliente(self, id):    
        query = 'DELETE FROM cliente WHERE id=?'
        data = (id,)
        self.db.execute_query_no_return(query, data)
    
    def InativarCliente(self,id):
        query = 'UPDATE cliente SET ativo=? WHERE id=?'
        data = (0, id)
        self.db.execute_query_no_return(query, data)

    def AtivarCliente(self,id):
        query = 'UPDATE cliente SET ativo=? WHERE id=?'
        data = (1, id)
        self.db.execute_query_no_return(query, data)
    
    def ValidarCliente(self,id):
        query = 'SELECT ativo FROM cliente WHERE id=?'
        data = (id,)
        return self.db.execute_query(query, data)
    def BuscarCliente(self):
        query = "SELECT id, nome FROM cliente WHERE ativo=1"
        result = self.db.execute_query(query)
        return result
    
        