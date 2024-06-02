def print_order(self):
    # Criar uma instância da impressora
        printer = QPrinter(QPrinter.HighResolution)
        printer.setPageSize(QPrinter.A4)
        dialog = QPrintDialog(printer, self)
        id_ordem = self.ordem_info['Código']

        ords = self.controller_ordem.CarregarOrdemServico(id_ordem)
        if ords:
            ord = ords[0] 
            cliente_id = ord[1]  
            equipamentod_id = ord[2]  
            data_inicio = ord[3]  
            data_final = ord[4]
            mao_de_obra = ord[5]
            valor_total = ord[6]

        clientes = self.controller_cliente.CarregarCliente(cliente_id)

        if clientes:
            cliente = clientes[0] 
            nome = cliente[1]  
            cep = cliente[2]  
            endereco = cliente[3]  
            numero = cliente[4]
            cidade = cliente[5]
            estado = cliente[6]
            cpf_cnjp = cliente[7]
            telefone = cliente[8]

            cliente_info = {
                'Nome': nome,
                'Cep': cep,
                'Endereco': endereco,
                'Número': numero,
                'Cidade': cidade,
                'Estado': estado,
                'Cpf_cnpj': cpf_cnjp,
                'Telefone': telefone
            }

        if dialog.exec_() == QPrintDialog.Accepted:
        # Renderizar a tela de detalhes na impressora
            self.renderContents(printer, cliente_info)

    def renderContents(self, printer, cliente_info):
        self.cliente_info = cliente_info

    # Criar um QPainter para desenhar na impressora
        painter = QPainter()

    # Iniciar a pintura com a impressora como dispositivo de pintura
        painter.begin(printer)

    ## Configurar a escala de impressão para preencher a página inteira
        screen_size = self.size()
        printer_size = printer.pageRect(QPrinter.DevicePixel)

# Calcular a escala horizontal e vertical
        scale_factor_x = printer_size.width() / screen_size.width()
        scale_factor_y = printer_size.height() / screen_size.height()

# Usar a menor escala entre largura e altura para garantir que o conteúdo caiba completamente na página
        scale_factor = min(scale_factor_x, scale_factor_y)

# Ajustar a escala para preencher toda a largura ou altura da página, o que for menor
        painter.scale(scale_factor, scale_factor)
        # Adicionar código HTML com os valores das variáveis
        html_content = f""" 
           <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Detalhes da Ordem de Serviço</title>
    <style>
      @page {{
                size: A4;
                margin: 0;
            }}
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
        }}

        #header {{
            text-align: center;
            margin-bottom: 20px;
        }}

        fieldset {{
            border: 1px solid #ccc;
            border-radius: 5px;
            padding: 10px;
            margin-bottom: 20px;
            position: relative;
        }}

        legend {{
            font-weight: bold;
        }}

        table {{
            border-collapse: collapse;
            width: 100%;
        }}

        th, td {{
            border: 1px solid #ccc;
            padding: 8px;
            text-align: left;
        }}

        th {{
            background-color: #f2f2f2;
        }}

        .info-item {{
            margin-bottom: 10px;
            position: relative;
        }}

        .info-item p {{
            margin: 0;
            position: relative;
        }}

        .info-item p:not(:last-child) {{
            margin-bottom: 5px;
        }}

        .info-item p span {{
            margin-right: 5px;
        }}

        .info-item p::after {{
            content: "";
            position: absolute;
            width: 100%;
            height: 1px;
            background-color: #ccc;
            bottom: -5px;
            left: 0;
        }}

        #total {{
            font-weight: bold;
        }}

        .info-table {{
            float: left;
            width:25%;
            margin-top: 10px;            
            margin-bottom: 40px;
            border: 1px solid #ccc; /* Adiciona uma borda na parte inferior da tabela */
        }}

        .info-table td {{
            border: 1px solid #ccc;
            padding: 5px;
        }}

        .info-table td:first-child {{
            text-align: right;
            font-weight: bold;
        }}
        .info-table td:first-child tr:last-child {{
            border: none;
        }}
        
        
    </style>
</head>
<body>
    <div id="header">
        <img src="logo.png" alt="Logo">
        <h1>Nome da Empresa</h1>
        <p>Telefone: <span>(00) 1234-5678</span></p>
        <p>Endereço: <span>Rua Exemplo, 1234</span></p>
        <p class="info-item">Cidade: <span>Cidade Exemplo</span> | Estado: <span>Estado</span> | CEP: <span>12345-678</span></p>
    </div>

    <fieldset id="cliente-info">
        <legend>Informações do Cliente</legend>
        <div class="info-item">
            <p><strong>Cliente:</strong> {self.cliente_info['Nome']}</p>
        </div>
        <div class="info-item">
            <p><strong>Endereço:</strong> {self.cliente_info['Endereco']}</p>
        </div>
        <div class="info-item">
            <p><strong>Cidade:</strong> {self.cliente_info['Cidade']}</p>
            <p><strong>Estado:</strong> {self.cliente_info['Estado']}</p>
            <p><strong>CEP:</strong> {self.cliente_info['Cep']}</p>
        </div>
        <div class="info-item">
            <p><strong>CPF/CNPJ:</strong> {self.cliente_info['Cpf_cnpj']}</p>
        </div>
        <div class="info-item">
            <p><strong>Telefone:</strong> {self.cliente_info['Telefone']}</p>
        </div>
    </fieldset>

    <fieldset id="produto-info">
        <legend>Informações do Produto</legend>
        <div class="info-item">
            <p><strong>Produto:</strong> <span>Modelo do Produto - Marca</span></p>
        </div>
        <div class="info-item">
            <p><strong>RPM:</strong> <span>3000</span></p>
        </div>
        <div class="info-item">
            <p><strong>Polos:</strong> <span>4</span></p>
        </div>
        <div class="info-item">
            <p><strong>Fases:</strong> <span>3</span></p>
        </div>
        <div class="info-item">
            <p><strong>Tensão:</strong> <span>220V</span></p>
        </div>
        <div class="info-item">
            <p><strong>Defeito:</strong> <span>Descrição do Defeito</span></p>
        </div>
    </fieldset>

    <fieldset id="item-info">
        <legend>Materiais Utilizados</legend>
        <table>
            <thead>
                <tr>
                    <th>Quantidade</th>
                    <th>Descrição do Material</th>
                    <th>Valor Unitário</th>
                    <th>Total</th>
                </tr>
            </thead>
            <tbody>
                <!-- Linhas da tabela preenchidas dinamicamente -->
                <tr>
                    <td>2</td>
                    <td>Material A</td>
                    <td>R$ 50,00</td>
                    <td>R$ 100,00</td>
                </tr>
                <tr>
                    <td>1</td>
                    <td>Material B</td>
                    <td>R$ 75,00</td>
                    <td>R$ 75,00</td>
                </tr>
            </tbody>
        </table>
    </fieldset>
    <table class="info-table">
        <tbody>
            <tr>
                <th>Data Inicial:</th>
                <td>01/01/2023</td>
                
            </tr>
            <tr>
                <th>Data Final:</th>
                <td>05/01/2023</td>
                
            </tr>
            
        </tbody>
    </table>
    <table class="info-table">
        <tbody>
            <tr>
                
                <th>Total dos Materiais Utilizados:</th>
                <td>R$ 175,00</td>
            </tr>
            <tr>
                
                <th>Mão de Obra:</th>
                <td>R$ 150,00</td>
            </tr>
            <tr>
                <th>Total da Ordem de Serviço:</th>
                <td>R$ 325,00</td>
            </tr>
        </tbody>
    </table>
    

    
   
</body>
</html>

        """
        
        # Criar um documento QTextDocument para renderizar o HTML
        document = QTextDocument()
        document.setHtml(html_content)
        
        # Renderizar o conteúdo HTML na impressora
        document.drawContents(painter)

        # Finalizar a pintura
        painter.end()
        