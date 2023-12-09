import time
import RPi.GPIO as GPIO
import Adafruit_PCA9685

class SG90_92R_Class:

    def __init__(self, Channel, ZeroOffset):
        self.mChannel = Channel
        self.m_ZeroOffset = ZeroOffset

        self.mPwm = Adafruit_PCA9685.PCA9685(address = 0x40)
        self.mPwm.set_pwm_freq(60)

    def SetPos(self, pos):
        pulse = (650 - 150) * pos / 180 + 150 + self.m_ZeroOffset
        self.mPwm.set_pwm(self.mChannel, 0, int(pulse))

    def Cleanup(self):
        self.SetPos(90)
        time.sleep(1)

if __name__ == '__main__':

    angle_max = 90
    angle_delay_t = 0.01
    angle=0
    continue_sign=True

    try:
        while True:
            continue_sign=True
            channel = input("Channel num: ")
            Servo = SG90_92R_Class(Channel = int(channel), ZeroOffset = -10)
            while continue_sign==True:
                angle=input("Action angle: ")
                Servo.SetPos(int(angle))
                message=input("continue?: ")
                if message=="n":
                    continue_sign=False
                elif message=="y":
                    continue_sign=True

    except KeyboardInterrupt:
        print("Ctrl + C")

    except Exception as e:
        print(str(e))

    # finally:
    #     Servo.Cleanup()