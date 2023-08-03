import pika
import time

contador = 0

def cortar_cabelo():
    global contador
    time.sleep(3)
    print(f"Ciclo {contador}: Cabelo cortado!")
    contador += 1
    return "Cabelo cortado!"

def cortar_barba():
    global contador
    time.sleep(4)
    print(f"Ciclo {contador}: Barba cortada!")
    contador += 1
    return "Barba cortada!"

def cortar_bigode():
    global contador
    time.sleep(5)
    print(f"Ciclo {contador}: Bigode cortado!")
    contador += 1
    return "Bigode cortado!"

def on_request(ch, method, props, body):
    response = None
    client_id = int(props.correlation_id)

    if method.routing_key == "cortar_cabelo":
        response = cortar_cabelo()
    elif method.routing_key == "cortar_barba":
        response = cortar_barba()
    elif method.routing_key == "cortar_bigode":
        response = cortar_bigode()
    else:
        print("Serviço desconhecido:", method.routing_key)

    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(
            correlation_id=props.correlation_id
        ),
        body=response.encode()
    )

    ch.basic_ack(delivery_tag=method.delivery_tag)

def queue_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='barbeiro', exchange_type='direct')

    channel.queue_declare(queue='cortes')

    channel.queue_bind(exchange='barbeiro', queue='cortes', routing_key='cortar_cabelo')
    channel.queue_bind(exchange='barbeiro', queue='cortes', routing_key='cortar_barba')
    channel.queue_bind(exchange='barbeiro', queue='cortes', routing_key='cortar_bigode')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='cortes', on_message_callback=on_request)

    print("Aguardando clientes...")
    channel.start_consuming()

def main():
    queue_consumer()

if __name__ == "__main__":
    main()
