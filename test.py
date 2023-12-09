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
    Servo = SG90_92R_Class(Channel = 0, ZeroOffset = -10)

    angle_max = 90
    angle_delay_t = 0.01
    a=0
    try:
        while True:
    #         for i in range(angle_max):
    #             time.sleep(angle_delay_t)
    #             Servo.SetPos(i)
    #         for i in reversed(range(angle_max)):
    #             time.sleep(angle_delay_t)
    #             Servo.SetPos(i)
            a = input()
            Servo.SetPos(int(a))

    except KeyboardInterrupt:
        print("Ctrl + C")

    except Exception as e:
        print(str(e))

    # finally:
    #     Servo.Cleanup()