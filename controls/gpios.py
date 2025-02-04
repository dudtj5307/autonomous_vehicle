import RPi.GPIO as GPIO

import sys

from . import motors

# GPIO VALUES
SWT1, SWT2, SWT3, SWT4 =  5, 6, 13, 19

# GPIO GROUPS
SWITCHs = [SWT1, SWT2, SWT3, SWT4]

# GPIO SETUPS
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

for switch in SWITCHs: GPIO.setup(switch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

MOTOR = motors.MOTORS()

def SWT_PUSHED():
    swt_val = [GPIO.input(SWT1), GPIO.input(SWT2), GPIO.input(SWT3), GPIO.input(SWT4)]
    for i in range(4):
        if swt_val[i] == 1:
            return i+1
    return 0

NOT_CLEANUP = True

def cleanup_GPIOs():
    global NOT_CLEANUP
    if NOT_CLEANUP:
        MOTOR.cleanup()
        GPIO.cleanup()
        NOT_CLEANUP = False

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