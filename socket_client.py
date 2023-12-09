import socket
import threading

HOST = '127.0.1.1'
PORT = 7672

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

def recv_data(client_socket):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        print("Received: ", repr(data.decode()))

recv_thread = threading.Thread(target=recv_data, args=(client_socket,))
recv_thread.start()
print('>> Connected to the Server')

while True:
    message = input()
    if message == 'quit':
        client_socket.send(message.encode())
        break

    client_socket.send(message.encode())

client_socket.close()
