from socket import *

serverCredentials = ('localhost', 5000)

questoes = [
    {'numero': 1, 'opcoes': 5, 'respostas': 'VFFFV'},
    {'numero': 2, 'opcoes': 4, 'respostas': 'VVVV'},
    {'numero': 3, 'opcoes': 3, 'respostas': 'VVV'}
]

client_socket = socket(AF_INET, SOCK_DGRAM)

for questao in questoes:
    responseMessage = f'{questao["numero"]};{questao["opcoes"]};{questao["respostas"]}'
    client_socket.sendto(responseMessage.encode(), serverCredentials)

    response, _ = client_socket.recvfrom(1024)
    print('Resposta do servidor:', response.decode())

client_socket.close()
