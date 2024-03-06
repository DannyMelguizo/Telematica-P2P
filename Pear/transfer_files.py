import config_file, client
import pika

def get_file():
    connection = pika.BlockingConnection(pika.ConnectionParameters(config_file.get_ip(), 5672))
    channel = connection.channel()

    channel.queue_declare(queue=config_file.get_ip())

    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")
        client.files_founds(body)
        
    channel.basic_consume(queue=config_file.get_ip(), on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

def upload_file(ip, file):
    connection = pika.BlockingConnection(pika.ConnectionParameters(ip, 5672))
    channel = connection.channel()

    channel.queue_declare(queue=ip)
    channel.basic_publish(exchange='', routing_key=ip, body=file)
    print(f" [x] Sent file {file}")
    connection.close()