import RPi.GPIO as GPIO
from . import leds

# GPIO VALUES
PWMA, AIN1, AIN2 = 18, 22, 27
PWMB, BIN1, BIN2 = 23, 25, 24

# GPIO GROUPS
LMOTORs = [PWMA, AIN1, AIN2]
RMOTORs = [PWMB, BIN1, BIN2]

# GPIO SETUPS
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
for motor in LMOTORs + RMOTORs:
    GPIO.setup(motor, GPIO.OUT)

L_Motor = GPIO.PWM(PWMA, 500)     # freq : 0 ~ 10,000(Hz)
R_Motor = GPIO.PWM(PWMB, 500)
L_Motor.start(0); LMOTORs.append(L_Motor)
R_Motor.start(0); RMOTORs.append(R_Motor)

FRONT, BACK  = 0, 1

class MOTORS():
    def __init__(self):
        self.direction = FRONT
        
    def move_motor(self, MOTORS, direction, ncycle):
        GPIO.output(MOTORS[1], direction)
        GPIO.output(MOTORS[2], 1-direction)
        MOTORS[3].ChangeDutyCycle(ncycle)
        
    def move_stop(self):
        self.move_motor(LMOTORs, FRONT, 0)
        self.move_motor(RMOTORs, FRONT, 0)
        leds.LED_CONTROL(led_off=[0,1,2,3])

    def move_front(self, motorSpeed):
        self.move_motor(LMOTORs, FRONT, motorSpeed)
        self.move_motor(RMOTORs, FRONT, motorSpeed)
        self.direction = FRONT
        leds.LED_CONTROL(led_on=[0,1], led_off=[2,3])
        
    def move_back(self, motorSpeed):
        self.move_motor(LMOTORs, BACK, motorSpeed)
        self.move_motor(RMOTORs, BACK, motorSpeed)
        self.direction = BACK
        leds.LED_CONTROL(led_on=[2,3], led_off=[0,1])
        
    def move_left(self, motorSpeed):
        self.move_motor(LMOTORs, self.direction, motorSpeed * 0.477)
        self.move_motor(RMOTORs, self.direction, motorSpeed * 1.523)
        leds.LED_CONTROL(led_on=[0,2], led_off=[1,3])

    def move_right(self, motorSpeed):
        self.move_motor(LMOTORs, self.direction, motorSpeed * 1.523)
        self.move_motor(RMOTORs, self.direction, motorSpeed * 0.477)
        leds.LED_CONTROL(led_on=[1,3], led_off=[0,2])
        
    def cleanup(self):
        L_Motor.stop()
        R_Motor.stop()
        leds.LED_CONTROL(led_off=[0,1,2,3])

if __name__ == "__main__":
    # test code
    import time
    moveMotor_front(30)
    time.sleep(1)
    moveMotor_stop()
    
    pass

