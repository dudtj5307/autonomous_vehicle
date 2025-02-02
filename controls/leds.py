import RPi.GPIO as GPIO

# GPIO VALUES
HIGH, LOW = GPIO.HIGH, GPIO.LOW
LED1, LED2, LED3, LED4 = 26, 16, 20, 21

# GPIO GROUPS
LEDs = [LED1, LED2, LED3, LED4]

# GPIO SETUPS
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

for led in LEDs: GPIO.setup(led, GPIO.OUT)

def LED_CONTROL(led_on=[], led_off=[]):
    for led_idx in led_on:
        GPIO.output(LEDs[led_idx], HIGH)
    for led_idx in led_off:
        GPIO.output(LEDs[led_idx], LOW)