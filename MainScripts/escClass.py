import pigpio
import os
import time


class ESC:
    def __init__(self):
        self.yatay1 = 4
        self.yatay2 = 17
        self.dikey1 = 18
        self.dikey2 = 19

        self.maxv = 2450
        self.minv = 1000

        self.pi = pigpio.pi()

        self.pi.set_servo_pulsewidth(self.yatay1,0)
        self.pi.set_servo_pulsewidth(self.yatay2,0)
        self.pi.set_servo_pulsewidth(self.dikey1,0)
        self.pi.set_servo_pulsewidth(self.dikey2,0)

    def calibrate(self):
        motors = [self.yatay1,self.yatay2,self.dikey1,self.dikey2]
        for motor in motors:
            self.pi.set_servo_pulsewidth(motor, 0)
            time.sleep(0.2)
            self.pi.set_servo_pulsewidth(motor, self.maxv)
            time.sleep(0.2)
            self.pi.set_servo_pulsewidth(motor, self.minv)
            time.sleep(7)
            time.sleep(5)
            self.pi.set_servo_pulsewidth(motor, 0)
            time.sleep(2)
            self.pi.set_servo_pulsewidth(motor, self.minv)
            time.sleep(1)

    def forward(self,speed):
        self.pi.set_servo_pulsewidth(self.yatay1, speed)
        self.pi.set_servo_pulsewidth(self.yatay2, speed)

    def leftfor(self,speed):
        self.pi.set_servo_pulsewidth(self.yatay1, 0)
        self.pi.set_servo_pulsewidth(self.yatay2, speed)

    def rightfor(self,speed):
        self.pi.set_servo_pulsewidth(self.yatay1, speed)
        self.pi.set_servo_pulsewidth(self.yatay2, 0)

    def stop(self):
        self.pi.set_servo_pulsewidth(self.yatay1, 0)
        self.pi.set_servo_pulsewidth(self.yatay2, 0)

    def up(self,speed):
        self.pi.set_servo_pulsewidth(self.dikey1, speed)
        self.pi.set_servo_pulsewidth(self.dikey2, speed)

    def down(self, speed):
        self.pi.set_servo_pulsewidth(self.dikey1, speed)
        self.pi.set_servo_pulsewidth(self.dikey2, speed)



