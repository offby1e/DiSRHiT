import socket
import threading

client_sockets = []
HOST = socket.gethostbyname(socket.gethostname())
PORT = 7672

def handle_client(client_socket, addr):
    print('>> Connected by:', addr[0], ':', addr[1])

    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                print('>> Disconnected by', addr[0], ':', addr[1])
                break

            print('>> Received from', addr[0], ':', addr[1], data.decode())

            for client in client_sockets:
                if client != client_socket:
                    client.send(data)

        except ConnectionResetError as e:
            print('>> Disconnected by', addr[0], ':', addr[1])
            break

    if client_socket in client_sockets:
        client_sockets.remove(client_socket)
        print('remove client list:', len(client_sockets))

    client_socket.close()

def main():
    print('>> Server Start with ip:', HOST)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    try:
        while True:
            print('>> Wait')
            client_socket, addr = server_socket.accept()
            client_sockets.append(client_socket)
            client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            client_thread.start()
            print("참가자 수:", len(client_sockets))
    except Exception as e:
        print('에러:', e)
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()