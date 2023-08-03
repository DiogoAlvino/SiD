import pika
import time
import random

services = ["cortar_cabelo", "cortar_barba", "cortar_bigode"]

def request_service(service):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='barbeiro', exchange_type='direct')

    result = channel.queue_declare(queue='', exclusive=True)
    callback_queue = result.method.queue

    channel.basic_publish(exchange='barbeiro',
                          routing_key=service,
                          properties=pika.BasicProperties(
                              reply_to=callback_queue,
                              ),
                          body='')

    while True:
        method_frame, header_frame, body = channel.basic_get(callback_queue)
        if method_frame:
            channel.basic_ack(method_frame.delivery_tag)
            break
        time.sleep(0.1)

    connection.close()

if __name__ == "__main__":
    num_clients = 5
    num_cycles = 20
    client_id = random.randint(1, num_clients)

    for cycle in range(num_cycles):
        print(f"Cliente {client_id} está competindo no ciclo {cycle+1}...")
        random.shuffle(services)
        for service in services:
            request_service(service)

        # Passa o token para o próximo cliente
        client_id = (client_id % num_clients) + 1
