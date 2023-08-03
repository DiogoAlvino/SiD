import pika
import time
import random

def request_service(cliente, service):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='barbeiro', exchange_type='direct')

    result = channel.queue_declare(queue='', exclusive=True)
    callback_queue = result.method.queue

    channel.basic_publish(exchange='barbeiro',
                          routing_key=service,
                          properties=pika.BasicProperties(
                              reply_to=callback_queue,
                              correlation_id=str(cliente['clienteid'])
                          ),
                          body='')

    response = None
    while response is None:
        method_frame, header_frame, body = channel.basic_get(callback_queue)
        if method_frame and str(cliente['clienteid']) == header_frame.correlation_id:
            channel.basic_ack(method_frame.delivery_tag)
            response = body
        time.sleep(0.1)

    connection.close()
    return response

if __name__ == "__main__":
    num_clients = 5
    num_cycles = 20
    clientes = []
    clienteAtual = ''

    for i in range(num_clients):
        clientes.append({
            "clienteid": i,
            "service": ""
        })

    for i in range(num_cycles):
        print(f"\n--- Ciclo {i} ---")
        
        clienteAtual = random.choice(clientes)

        if clienteAtual['service'] == '':
            clienteAtual['service'] = 'cortar_cabelo'
        elif clienteAtual['service'] == 'cortar_cabelo':
            clienteAtual['service'] = 'cortar_barba'
        elif clienteAtual['service'] == 'cortar_barba':
            clienteAtual['service'] = 'cortar_bigode'
        else:
            clienteAtual['service'] = 'cortar_cabelo'

        print(f"Cliente {clienteAtual['clienteid']} será atendido com: {clienteAtual['service']}!")
        response = request_service(clienteAtual, clienteAtual['service'])
        print(f"Resposta do servidor para o Cliente {clienteAtual['clienteid']}: {response.decode()}")