from database.database import Database
class EquipamentoClienteController:
    def __init__(self):
        self.db = Database('database/gerenciamento_ordens_servico.db')    
    
    def create_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS equipamento_cliente (
        id INTEGER PRIMARY KEY,
        descricao TEXT,
        cliente_id INTEGER,
        ativo BOOLEAN,
        FOREIGN KEY(cliente_id) REFERENCES cliente(id)
        )
        '''
        self.db.create_table(sql)
    def ListarEquipamentoCliente(self, cliente_id):
        query = "SELECT id, descricao FROM equipamento_cliente WHERE cliente_id = ? and ativo=1"
        data = (cliente_id,)
        result = self.db.execute_query(query, data)
        equipamentos = [{'id': row[0], 'descricao': row[1]} for row in result]
        return equipamentos
    
    def CarregarEquipamentoCliente(self, id):
        query = 'SELECT * FROM equipamento_cliente where id=?'
        data = (id,)
        return self.db.execute_query(query,data)
    
    def FiltrarEquipamentoCliente(self,tipo):
        query = 'SELECT * FROM equipamento_cliente where ativo=?'
        data = (tipo,)
        return self.db.execute_query(query,data)
    
    def CadastrarEquipamentoCliente(self, descricao, cliente_id):
        query = 'INSERT INTO equipamento_cliente (descricao, cliente_id, ativo) VALUES (?, ?, ?)'
        data = (descricao, cliente_id, True)
        self.db.execute_query_no_return(query, data)
    
    def EditarequipamentoCliente(self, descricao,id):    
        query = 'UPDATE equipamento_cliente SET descricao=? WHERE id=?'
        data = (descricao, id)
        self.db.execute_query_no_return(query, data)
    
    def DeletarEquipamentoCliente(self, id):    
        query = 'DELETE FROM equipamento_cliente WHERE id=?'
        data = (id,)
        self.db.execute_query_no_return(query, data)
    
    def InativarEquipamentoCliente(self,id):
        query = 'UPDATE equipamento_cliente SET ativo=? WHERE id=?'
        data = (0, id)
        self.db.execute_query_no_return(query, data)

    def AtivarEquipamentoCliente(self,id):
        query = 'UPDATE equipamento_cliente SET ativo=? WHERE id=?'
        data = (1, id)
        self.db.execute_query_no_return(query, data)
    
    def ValidarEquipamentoCliente(self,id):
        query = 'SELECT ativo FROM equipamento_cliente WHERE id=?'
        data = (id,)
        return self.db.execute_query(query, data)
    
        