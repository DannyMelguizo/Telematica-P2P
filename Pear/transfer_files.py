import config_file, client
import socket
import threading
import pika


# class Server():
#     def __init__(self):
#         self.ip = "0.0.0.0"
#         self.port = config_file.get_port_mom()

#         self.recv_files = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.recv_files.bind((self.ip, self.port))
#         self.recv_files.listen()

#         while True:
#             client_file, address = self.recv_files.accept()
#             thread_client_file = threading.Thread(target=self.handle_client, args=(client_file, address))
#             thread_client_file.start()

#     def handle_client(self, client_socket, address):
#         while True:
#             data = client_socket.recv(self.buffer)

#             if data:
#                 data = data.decode()
#                 client.files_founds(data)

#                 client_socket.close()
#                 break


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

# def main():
#     Server()