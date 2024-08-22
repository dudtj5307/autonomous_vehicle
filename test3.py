import RPi.GPIO as GPIO
import time
import booting_music

# GPIO VALUES
TIME_INTERVALS = 0.05
HIGH, LOW = GPIO.HIGH, GPIO.LOW
LED1, LED2, LED3, LED4 = 26, 16, 20, 21
SWT1, SWT2, SWT3, SWT4 =  5,  6, 13, 19
PWMA, PWMB = 18, 23
AIN1, AIN2, BIN1, BIN2 = 22, 27, 25, 24
FRONT, BACK = 0, 1

BUZZER = 12

# GPIO GROUPS
GPIOs = [LED1, LED2, LED3, LED4, SWT1, SWT2, SWT3, SWT4]
LEDs  = [LED1, LED2, LED3, LED4]
SWITCHs  = [SWT1, SWT2, SWT3, SWT4]
LMOTORs = [PWMA, AIN1, AIN2]
RMOTORs = [PWMB, BIN1, BIN2]

# GPIO SETUPS
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
'''
GPIO.setup(BUZZER, GPIO.OUT)
for leds in LEDs + LMOTORs + RMOTORs:
    GPIO.setup(leds, GPIO.OUT)
p = GPIO.PWM(BUZZER, 164.8138)
'''
for motors in LMOTORs + RMOTORs:
    GPIO.setup(motors, GPIO.OUT)
    
for switch in SWITCHs:
    GPIO.setup(switch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
L_Motor, R_Motor = GPIO.PWM(PWMA, 500), GPIO.PWM(PWMB, 500)    # freq : ~ 10,000(Hz)
L_Motor.start(0)
R_Motor.start(0)
LMOTORs.append(L_Motor)
RMOTORs.append(R_Motor)

def SWT_PUSHED():
    swt_val = [GPIO.input(SWT1), GPIO.input(SWT2), GPIO.input(SWT3), GPIO.input(SWT4)]
    for i in range(4):
        if swt_val[i] == 1:
            return i+1
    return 0

def moveMotor(MOTORS, direction, ncycle):
    GPIO.output(MOTORS[1], direction)
    GPIO.output(MOTORS[2], 1-direction)
    MOTORS[3].ChangeDutyCycle(ncycle)

last_num = 0

try:
    while True:
        swt_num = SWT_PUSHED()
        if swt_num == last_num:
            moveMotor(LMOTORs, FRONT, 0)
            moveMotor(RMOTORs, FRONT, 0)
            last_num = 0
        elif swt_num == 1:
            moveMotor(LMOTORs, FRONT, 20)
            moveMotor(RMOTORs, FRONT, 20)
            last_num = swt_num
        elif swt_num == 2:
            moveMotor(LMOTORs, FRONT, 30)
            moveMotor(RMOTORs, FRONT, 10)
            last_num = swt_num
        elif swt_num == 3:
            moveMotor(LMOTORs, FRONT, 10)
            moveMotor(RMOTORs, FRONT, 30)
            last_num = swt_num
        elif swt_num == 4:
            moveMotor(LMOTORs, BACK, 20)
            moveMotor(RMOTORs, BACK, 20)
            last_num = swt_num
        time.sleep(0.2)

except KeyboardInterrupt:
    L_Motor.stop()
    R_Motor.stop()
    
GPIO.cleanup()