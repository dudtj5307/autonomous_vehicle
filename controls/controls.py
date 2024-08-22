import RPi.GPIO as GPIO


# GPIO VALUES
HIGH, LOW = GPIO.HIGH, GPIO.LOW
FRONT, BACK = 0, 1

LED1, LED2, LED3, LED4 = 26, 16, 20, 21
SWT1, SWT2, SWT3, SWT4 =  5,  6, 13, 19
PWMA, PWMB, AIN1, AIN2, BIN1, BIN2 = 18, 23, 22, 27, 25, 24

# GPIO GROUPS
LEDs     = [LED1, LED2, LED3, LED4]
SWITCHs  = [SWT1, SWT2, SWT3, SWT4]
LMOTORs = [PWMA, AIN1, AIN2]
RMOTORs = [PWMB, BIN1, BIN2]

# GPIO SETUPS
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

for led in LEDs:                GPIO.setup(led, GPIO.OUT)
for switch in SWITCHs:          GPIO.setup(switch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
for motor in LMOTORs + RMOTORs: GPIO.setup(motor, GPIO.OUT)

L_Motor, R_Motor = GPIO.PWM(PWMA, 500), GPIO.PWM(PWMB, 500)    # freq : ~ 10,000(Hz)
L_Motor.start(0); LMOTORs.append(L_Motor)
R_Motor.start(0); RMOTORs.append(R_Motor)


def LED_CONTROL(led_idx, flag):
    if isinstance(led_idx, int):
        GPIO.output(LEDs[led_idx], flag)
    else:
        for led_i in led_idx:
            GPIO.output(LEDs[led_i], flag)

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
    
def moveMotor_stop():
    moveMotor(LMOTORs, FRONT, 0)
    moveMotor(RMOTORs, FRONT, 0)

def moveMotor_front(motorSpeed):
    moveMotor(LMOTORs, FRONT, motorSpeed)
    moveMotor(RMOTORs, FRONT, motorSpeed)

def moveMotor_back(motorSpeed):
    moveMotor(LMOTORs, BACK, motorSpeed)
    moveMotor(RMOTORs, BACK, motorSpeed)
    
def moveMotor_left(motorSpeed, directionFlag):
    moveMotor(LMOTORs, directionFlag, motorSpeed * 0.5)
    moveMotor(RMOTORs, directionFlag, motorSpeed * 1.5)

def moveMotor_right(motorSpeed, directionFlag):
    moveMotor(LMOTORs, directionFlag, motorSpeed * 1.5)
    moveMotor(RMOTORs, directionFlag, motorSpeed * 0.5)

def cleanup_GPIOs():
        L_Motor.stop()
        R_Motor.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    # test code

    pass