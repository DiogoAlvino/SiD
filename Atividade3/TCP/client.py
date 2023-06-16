import socket

serverCredentials = ('localhost', 9000)
filePath = 'respostas.txt'

with open(filePath, 'r') as file:
    respostas = file.read()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(serverCredentials)
client_socket.sendall(respostas.encode())


response = client_socket.recv(1024).decode()
print('Resposta do servidor:', response)

client_socket.close()