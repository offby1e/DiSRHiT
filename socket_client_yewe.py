import socket
import threading

HOST = '10.244.84.28'  # Replace with the server's IP address
PORT = 7672

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((HOST, PORT))
except ConnectionError as e:
    print(f"Error connecting to the server: {e}")
    exit()

def recv_data(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            print("Received: ", repr(data.decode()))
        except ConnectionError as e:
            print(f"Error receiving data: {e}")
            break

recv_thread = threading.Thread(target=recv_data, args=(client_socket,))
recv_thread.start()

print('>> Connected to the Server')

try:
    while True:
        message = input()
        if message == 'quit':
            client_socket.send(message.encode())
            break
        client_socket.send(message.encode())

except KeyboardInterrupt:
    print("\nKeyboardInterrupt: Exiting the program.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    client_socket.close()
