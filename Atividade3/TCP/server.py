import threading
import socket

class Servidor:
    def __init__(self, port):
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', self.port))
        self.stats = {}

    def start(self):
        print(f'Servidor está rodando na porta {self.port}')
        self.server_socket.listen(5)

        while True:
            client_socket, client_address = self.server_socket.accept()
            client_thread = threading.Thread(target=self.handleClient, args=(client_socket, client_address))
            client_thread.start()

    def handleClient(self, client_socket, client_address):
        print(f'Cliente conectado: {client_address}')

        answers = client_socket.recv(1024).decode()
        answers_list = answers.splitlines()

        for answer in answers_list:
            question_num, num_options, response = answer.split(';')

            num_correct = self.questoesCorretas(response)
            num_errors = len(response) - num_correct

            response_msg = f'{question_num};{num_correct};{num_errors}'

            self.atualizaEstatisticas(question_num, num_correct, num_errors)

            client_socket.send(response_msg.encode())

        client_socket.close()
        print(f'Cliente Desconectado: {client_address}')

    def questoesCorretas(self, response):
        return response.count('V')

    def atualizaEstatisticas(self, question_num, num_correct, num_errors):
        if question_num in self.stats:
            self.stats[question_num]['acertos'] += num_correct
            self.stats[question_num]['erros'] += num_errors
        else:
            self.stats[question_num] = {'acertos': num_correct, 'erros': num_errors}

        self.print_statistics()

    def print_statistics(self):
        print('Estatísticas:')
        for question_num, data in self.stats.items():
            print(f'Questão {question_num}: acertos={data["acertos"]} erros={data["erros"]}')

port = 9000

server = Servidor(port)
server.start()