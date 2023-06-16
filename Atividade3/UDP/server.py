import threading
from socket import *

class Servidor:
    def __init__(self, port):
        self.port = port
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind(('', self.port))
        self.stats = {}

    def start(self):
        print(f'Servidor está rodando na porta {self.port}')

        while True:
            message, client_address = self.socket.recvfrom(1024)
            client_thread = threading.Thread(target=self.handleClient, args=(message, client_address))
            client_thread.start()

    def handleClient(self, message, client_address):
        decoded_message = message.decode()
        question_num, num_options, answers = decoded_message.split(';')

        num_correct = self.questoesCorretas(answers)
        num_errors = len(answers) - num_correct

        response = f'{question_num};{num_correct};{num_errors}'

        self.atualizaEstatisticas(question_num, num_correct, num_errors)

        self.socket.sendto(response.encode(), client_address)

    def questoesCorretas(self, answers):
        return answers.count('V')

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

port = 5000

server = Servidor(port)
server.start()
