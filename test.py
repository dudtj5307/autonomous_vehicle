import RPi.GPIO as GPIO
import time

def controlLED(leds, VAR):
    for led in leds:
        GPIO.output(led, VAR)

HIGH, LOW = GPIO.HIGH, GPIO.LOW
LED1, LED2, LED3, LED4 = 26, 16, 20, 21
SWT1, SWT2, SWT3, SWT4 =  5,  6, 13, 19

GPIOs = [LED1, LED2, LED3, LED4, SWT1, SWT2, SWT3, SWT4]
LEDs  = [LED1, LED2, LED3, LED4]
SWTs  = [SWT1, SWT2, SWT3, SWT4]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

for leds in LEDs:
    GPIO.setup(leds, GPIO.OUT)

for switch in SWTs:
    GPIO.setup(switch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

swt_flag = 0
try:
    while True:
        swt1_val = GPIO.input(SWT1)
        if swt1_val==1 and swt_flag==0:
            swt_flag = 1
            controlLED(LEDs, HIGH)
            print("ON")
        elif swt1_val==0 and swt_flag==1:
            swt_flag = 0
            controlLED(LEDs, LOW)
            print("OFF")
            
        time.sleep(0.1)
    
except KeyboardInterrupt:
    controlLED(LEDs, LOW)

GPIO.cleanup()
