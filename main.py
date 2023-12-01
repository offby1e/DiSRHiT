import time
import RPi.GPIO as GPIO
import Adafruit_PCA9685
import threading

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

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
action_range = [[0]]
action_lock=[threading.Lock() for _ in action_range]

def servo_action(controller,pos,index):
    global action_range
    while True:
        controller.SetPos(pos[0])
        action_lock[index].acquire
        if len(action_range[index]) > 1:
            action_range[index].pop(0)

if __name__ == '__main__':
    channel=0
    for index in range(11):
        channel=index
        if index>4:
            channel+=1
        Servo_controller.append(Servo_Controller_Class(Channel = channel, ZeroOffset = -10)) 
        print(f"Init Controller No.{channel}")
    
    index=0
    for controller_thread in Servo_controller:
        Servo_action_thread.append(threading.Thread(target = servo_action, args = (controller_thread,action_range[index],index)))
        index+=1

    index=0
    for controller_thread in Servo_action_thread:
        controller_thread.start()
        print(f"Start of Motor No.{index}")
        index+=1

    try:
        pass
    except KeyboardInterrupt:
        print("Ctrl + C: "+Colors.BLUE+"KeyboardInterrupt"+Colors.END)
    except Exception as e:
        print(Colors.RED+"Exception error: "+Colors.END+str(e))
    finally:
        for controller in Servo_controller:
            controller.Cleanup()