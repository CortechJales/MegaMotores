from database.database import Database
class EquipamentoClienteController:
    def __init__(self):
        self.db = Database()    
    
    def create_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS equipamento_cliente (
        id INTEGER PRIMARY KEY,
        modelo TEXT,
        rpm TEXT,
        polos TEXT,
        fases TEXT,
        tensao TEXT,
        marca_id TEXT,
        defeito TEXT,
        potencia TEXT,
        cliente_id INTEGER,
        ativo BOOLEAN,
        FOREIGN KEY(cliente_id) REFERENCES cliente(id)
        
        FOREIGN KEY(cliente_id) REFERENCES cliente(id)
        )
        '''
        self.db.create_table(sql)
    def ListarEquipamentoCliente(self, cliente_id):
        query = "SELECT id, modelo, rpm, polos, fases, tensao, marca_id, potencia, defeito FROM equipamento_cliente WHERE cliente_id = ? and ativo=1"
        data = (cliente_id,)
        result = self.db.execute_query(query, data)
        equipamentos = [{'id': row[0], 'modelo': row[1],'rpm': row[2],'polos': row[3],'fases': row[4],'tensao': row[5],'marca_id': row[6],'potencia': row[7],'defeito': row[8]} for row in result]
        return equipamentos
    
    def CarregarEquipamentoCliente(self, id):
        query = 'SELECT * FROM equipamento_cliente where id=?'
        data = (id,)
        return self.db.execute_query(query,data)
    
    def FiltrarEquipamentoCliente(self,tipo):
        query = 'SELECT * FROM equipamento_cliente where ativo=?'
        data = (tipo,)
        return self.db.execute_query(query,data)
    
    def CadastrarEquipamentoCliente(self, modelo, rpm, polos, fases, tensao, marca_id, potencia, defeito, cliente_id):
        query = '''
            INSERT INTO equipamento_cliente 
            (modelo, rpm, polos, fases, tensao, marca_id, potencia, defeito, cliente_id, ativo) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        data = (modelo, rpm, polos, fases, tensao, marca_id,potencia, defeito, cliente_id, True)
        self.db.execute_query_no_return(query, data)

    def EditarequipamentoCliente(self, modelo, rpm, polos, fases, tensao, marca_id, potencia, defeito, id):
        query = '''
            UPDATE equipamento_cliente 
            SET modelo=?, rpm=?, polos=?, fases=?, tensao=?, marca_id=?,potencia=?, defeito=? 
            WHERE id=?
        '''
        data = (modelo, rpm, polos, fases, tensao, marca_id,potencia, defeito, id)
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
    def BuscarEquipamento(self,id):
        query = "SELECT id, modelo FROM equipamento_cliente WHERE cliente_id = ? AND ativo = 1"
        data = (id,)
        result = self.db.execute_query(query,data)
        return result
    def BuscarEquipamentos(self):
        query = "SELECT id, modelo FROM equipamento_cliente WHERE ativo = 1"
        result = self.db.execute_query(query)
        return result
    def CarregarImpressaoEquipamento(self,id):
        query = '''SELECT equipamento_cliente.id, equipamento_cliente.modelo, equipamento_cliente.rpm, equipamento_cliente.polos, equipamento_cliente.fases, equipamento_cliente.tensao, m.nome AS nome_marca,equipamento_cliente.potencia, equipamento_cliente.defeito 
FROM equipamento_cliente  
INNER JOIN marca AS m ON equipamento_cliente.marca_id = m.id 
WHERE equipamento_cliente.id=?'''
        data = (id,)
        return self.db.execute_query(query, data)
    
    def BuscarEquipamento(self, cliente_id):
        query = "SELECT id, modelo FROM equipamento_cliente WHERE cliente_id = ?"
        data = (cliente_id,)
        return self.db.execute_query(query, data)
    