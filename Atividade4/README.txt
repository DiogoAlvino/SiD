>>README<<
Este é um código para um sistema cliente-servidor de arquivos implementado usando a biblioteca Pyro5 e a GUI Tkinter em Python.

>>DESCRIÇÃO<<
O sistema consiste em um servidor de arquivos e um cliente que interagem entre si para permitir o upload, download, registro e cancelamento de interesse em arquivos.
O servidor mantém uma lista de arquivos e uma lista de clientes registrados. Os clientes podem se registrar no servidor e expressar interesse em arquivos específicos. Quando um arquivo é enviado ao servidor, ele notifica os clientes interessados ​​nesse arquivo. Os clientes podem fazer o download de arquivos disponíveis no servidor.
A interação entre o cliente e o servidor é realizada por meio de chamadas de método remotas usando a biblioteca Pyro5, que fornece uma maneira fácil de expor objetos Python para acesso remoto.
A interface do usuário do cliente é implementada usando a biblioteca Tkinter, fornecendo uma GUI simples para o usuário interagir com o sistema.

>>REQUISITOS<<
-Python 3.x
-Pyro5
-Tkinter
-Certifique-se de ter o Pyro5 e o Tkinter instalados antes de executar o código.

>>COMO EXECUTAR O SISTEMA<<
1- Inicie o servidor:
    -Execute o arquivo servidor.py em um terminal Python.

2- Inicie o cliente:
    -Execute o arquivo cliente.py em um terminal Python.
    -Insira o URI do servidor de arquivos quando solicitado.

3- Interface do cliente:
    -A interface do usuário do cliente será exibida.
    -Use os botões e campos de entrada para realizar as seguintes ações:
        -Fazer upload: Enviar um arquivo para o servidor.
        -Registrar interesse: Expressar interesse em um arquivo.
        -Cancelar interesse: Cancelar o interesse em um arquivo.
        -Baixar arquivo: Fazer o download de um arquivo do servidor.
        -Visualizar Lista de Arquivos: Exibir uma lista dos arquivos disponíveis no servidor.

>>OBSERVAÇÕES<<
-Certifique-se de que o servidor esteja em execução antes de iniciar o cliente.
-Certifique-se de fornecer o URI correto do servidor ao iniciar o cliente.
-Os arquivos enviados para o servidor são armazenados em memória e não são persistentes.
-O sistema suporta o envio de notificações para clientes interessados ​​em um arquivo específico quando esse arquivo é enviado ao servidor.