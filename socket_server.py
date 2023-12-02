import socket
import threading

client_sockets = []
HOST = socket.gethostbyname(socket.gethostname())
PORT = 7672

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    END = '\033[0m'

def handle_client(client_socket, addr):
    print(f"{Colors.YELLOW}[Socket] {Colors.END}{Colors.BLUE}Connected by:{Colors.END} {Colors.WHITE}{addr[0]}:{addr[1]}{Colors.END}")

    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                print(f"{Colors.YELLOW}[Socket] {Colors.END}{Colors.BLUE}Disconnected by: {Colors.END}{Colors.WHITE}{addr[0]}:{addr[1]}{Colors.END}")
                break

            print(f"{Colors.YELLOW}[Socket] {Colors.END}{Colors.BLUE}Received from: {addr[0]}:{addr[1]} {Colors.END}{Colors.WHITE}{data.decode()}{Colors.END}")

            for client in client_sockets:
                if client != client_socket:
                    client.send(data)

        except ConnectionResetError as e:
            print(f"{Colors.YELLOW}[Socket] {Colors.END}{Colors.BLUE}Disconnected by: {Colors.END}{Colors.WHITE}{Colors.BLUE}{addr[0]}:{addr[1]}{Colors.END}")
            break

    if client_socket in client_sockets:
        client_sockets.remove(client_socket)
        print(f"{Colors.YELLOW}[Socket] {Colors.END}{Colors.BLUE}remove client list: {Colors.END}{Colors.WHITE}{len(client_sockets)}{Colors.END}")

    client_socket.close()

def main():
    print(f"{Colors.YELLOW}[Socket] {Colors.END}{Colors.BLUE}Server Start with IP:{Colors.END} {Colors.MAGENTA}{HOST}{Colors.END} {Colors.BLUE}PORT:{Colors.END}{Colors.MAGENTA}{PORT}{Colors.END}")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    try:
        while True:
            print(f"{Colors.YELLOW}[Socket] {Colors.END}{Colors.BLUE}Waiting....{Colors.END}")
            client_socket, addr = server_socket.accept()
            client_sockets.append(client_socket)
            client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            client_thread.start()
            print(f"{Colors.YELLOW}[Socket] {Colors.END}{Colors.BLUE}Number of Participants: {Colors.END}{Colors.WHITE}{len(client_sockets)}{Colors.END}")
    except KeyboardInterrupt:
        print(f"{Colors.YELLOW}[Socket] {Colors.END}"+Colors.BLUE+"Ctrl + C: KeyboardInterrupt"+Colors.END)
    except Exception as e:
        print(f"{Colors.YELLOW}[Socket]{Colors.END}{Colors.RED}[Error] {e}{Colors.END}")
    finally:
        server_socket.close()
        print(f"{Colors.YELLOW}[Socket] {Colors.END}{Colors.BLUE}Socket Close{Colors.END}")

if __name__ == "__main__":
    main()