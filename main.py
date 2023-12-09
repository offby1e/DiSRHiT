import time
import RPi.GPIO as GPIO
import Adafruit_PCA9685
import threading
import socket
import os

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
    
os.system("clear")
class Servo_Controller_Class:
    def __init__(self,Channel,ZeroOffset):
        self.mChannel = Channel
        self.m_ZeroOffset = ZeroOffset

        self.mPwm = Adafruit_PCA9685.PCA9685(address = 0x40)
        self.mPwm.set_pwm_freq(60)
    
    def SetPos(self,pos):
        pulse = (650-150)*pos/180+150+self.m_ZeroOffset
        self.mPwm.set_pwm(self.mChannel,0,int(pulse))

    def Cleanup(self):
        self.SetPos(90)
        time.sleep(1)

Servo_controller = []
Servo_action_thread = []
action_range = [[10] for _ in range(11)]
action_lock=[threading.Lock() for _ in action_range]
command=[]

client_sockets = []
HOST = '0.0.0.0'
PORT = 7672

def append_angle(index,pos):
    global action_range
    action_lock[index].acquire()
    if len(action_range[index]) == 1:
        action_range[index][0] = int(float(pos))
    if len(action_range[index]) > 1:
        action_range[index].append(int(float(pos)))
    action_lock[index].release()
    

def handle_client(client_socket, addr):
    global action_range, command
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
            
            append_action_thread=[]

            command = list(data.decode().split(':'))
            if command[0] == 'action':
                for index in range(11):
                    append_action_thread.append(threading.Thread(target=append_angle, args=(index,command[index+1])))

                for action_thread in append_action_thread:
                    action_thread.start()
                
        except ConnectionResetError as e:
            print(f"{Colors.YELLOW}[Socket] {Colors.END}{Colors.BLUE}Disconnected by: {Colors.END}{Colors.WHITE}{Colors.BLUE}{addr[0]}:{addr[1]}{Colors.END}")
            break

    if client_socket in client_sockets:
        client_sockets.remove(client_socket)
        print(f"{Colors.YELLOW}[Socket] {Colors.END}{Colors.BLUE}remove client list: {Colors.END}{Colors.WHITE}{len(client_sockets)}{Colors.END}")

    client_socket.close()

def socket_main():
    print(f"\n{Colors.YELLOW}=============Socket Start============={Colors.END}")
    print(f"{Colors.YELLOW}[Socket] {Colors.END}{Colors.BLUE}Server Start with IP:{Colors.END} {Colors.MAGENTA}{socket.gethostbyname(socket.gethostname())}{Colors.END} {Colors.BLUE}PORT:{Colors.END}{Colors.MAGENTA}{PORT}{Colors.END}")
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

def servo_action(controller,pos,index):
    global action_range
    while True:
        controller.SetPos(pos[0])
        action_lock[index].acquire()
        if len(action_range[index]) > 1:
            action_range[index].pop(0)
        action_lock[index].release()

if __name__ == '__main__':
    print(f"{Colors.BOLD}{Colors.WHITE}=================Program Start================={Colors.END}{Colors.END}")
    print(f"{Colors.GREEN}=============Servo Controll Start============={Colors.END}")
    try:
        channel=0
        for index in range(11):
            channel=index
            Servo_controller.append(Servo_Controller_Class(Channel = channel, ZeroOffset = -10)) 
            print(f"{Colors.GREEN}[Servo Controller] {Colors.END}{Colors.BLUE}Init Controller No.{channel}{Colors.END}")
        
        index=0
        for controller_thread in Servo_controller:
            Servo_action_thread.append(threading.Thread(target = servo_action, args = (controller_thread,action_range[index],index)))
            index+=1
        print("\n")
        index=0
        for controller_thread in Servo_action_thread:
            controller_thread.start()
            print(f"{Colors.GREEN}[Servo Controller] {Colors.END}{Colors.BLUE}Start of Motor No.{index}{Colors.END}")
            index+=1
    except KeyboardInterrupt:
        print(f"{Colors.GREEN}[Servo Controller] {Colors.END}"+Colors.RED+"Ctrl + C: KeyboardInterrupt"+Colors.END)
    except Exception as e:
        print(f"{Colors.GREEN}[Servo Controller]{Colors.END}{Colors.RED}[Error] Exception error: {str(e)}{Colors.END}")
    finally:
        for controller in Servo_controller:
            controller.Cleanup()
<<<<<<< HEAD
    
=======
   
>>>>>>> 2b09b7d44d16357af471caded8e60bba80a38afb
    socket_main()