import RPi.GPIO as GPIO

import sys

from . import motors

# GPIO VALUES
HIGH, LOW = GPIO.HIGH, GPIO.LOW
LED1, LED2, LED3, LED4 = 26, 16, 20, 21
SWT1, SWT2, SWT3, SWT4 =  5,  6, 13, 19
FRONT, BACK = 0, 1

# GPIO GROUPS
LEDs    = [LED1, LED2, LED3, LED4]
SWITCHs = [SWT1, SWT2, SWT3, SWT4]

# GPIO SETUPS
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

for led in LEDs:                GPIO.setup(led, GPIO.OUT)
for switch in SWITCHs:          GPIO.setup(switch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


MOTOR = motors.MOTORS()

def SWT_PUSHED():
    swt_val = [GPIO.input(SWT1), GPIO.input(SWT2), GPIO.input(SWT3), GPIO.input(SWT4)]
    for i in range(4):
        if swt_val[i] == 1:
            return i+1
    return 0

def LED_CONTROL(led_on=[], led_off=[]):
    for led_idx in led_on:
        GPIO.output(LEDs[led_idx], HIGH)
    for led_idx in led_off:
        GPIO.output(LEDs[led_idx], LOW)

def cleanup_GPIOs():
        MOTOR.cleanup()
        GPIO.cleanup()

if __name__ == "__main__":
    # test code
    
        
    import time
    motor.move_front(30)
    time.sleep(1)
    motor.move_left(30)
    time.sleep(1)
    motor.move_back(30)
    time.sleep(1)
    motor.move_stop()
    
    pass