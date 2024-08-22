import RPi.GPIO as GPIO
import time

def controlLED(leds, VAR):
    for led in leds:
        GPIO.output(led, VAR)

# GPIO VALUES
TIME_INTERVALS = 0.05
HIGH, LOW = GPIO.HIGH, GPIO.LOW
ON, OFF = True, False
LED1, LED2, LED3, LED4 = 26, 16, 20, 21
SWT1, SWT2, SWT3, SWT4 =  5,  6, 13, 19
BUZZER = 12
#BUZZ_freq = {"C": 65.4064, "C#":  69.2957, "D":  73.4162, "D#":  77.7817, "E":  82.4069, "F": 87.3071, "F#": 92.4986,
#             "G": 97.9989, "G#": 103.8262, "A": 110.0001, "A#": 116.5409, "B": 123.4708}
BUZZ_freq = {"C": 130.8128, "C#": 138.5913, "D": 146.8324, "D#": 155.5635, "E": 164.8138, "F": 174.6141, "F#": 184.9972,
             "G": 195.9977, "G#": 207.6523, "A": 220.0000, "A#": 233.0819, "B": 246.9417}



# GPIO GROUPS
GPIOs = [LED1, LED2, LED3, LED4, SWT1, SWT2, SWT3, SWT4]
LEDs  = [LED1, LED2, LED3, LED4]
SWTs  = [SWT1, SWT2, SWT3, SWT4]

# GPIO SETUPS
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(BUZZER, GPIO.OUT)
for leds in LEDs:
    GPIO.setup(leds, GPIO.OUT)
for switch in SWTs:
    GPIO.setup(switch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

p = GPIO.PWM(BUZZER, BUZZ_freq["E"])

def SWT_PUSHED():
    swt_val = [GPIO.input(SWT1), GPIO.input(SWT2), GPIO.input(SWT3), GPIO.input(SWT4)]
    for i in range(4):
        if swt_val[i] == 1:
            return i+1
    return 0

def LED_CONTROL(led_num, flag):
    if led_num == 0: return
    GPIO.output(LEDs[led_num-1], flag)

def BUZ_CONTROL(freq, octv, flag):
    if flag:
        p.start(1)
        p.ChangeFrequency(BUZZ_freq[freq] * octv)
    else:
        p.stop()

def play_music():
    play_list = [["E", OCT, 1], ["A", OCT, 1], ["A", OCT, 3], ["B", OCT, 1], ["C", OCT2, 1], ["A", OCT, 1], ["A", OCT, 0.5],
                ["A", OCT, 0.2], ["C", OCT2, 1], ["B", OCT, 1], ["G", OCT, 1], ["G", OCT, 3], ["B", OCT, 1], ["C", OCT2, 1], ["A", OCT, 1], ["A", OCT, 4]]
    for freq, octv, cnts in play_list:
        if SWT_PUSHED(): break
        BUZ_CONTROL(freq, octv, ON)
        time.sleep(TIME_INTERVALS * cnts)
        BUZ_CONTROL(freq, octv, OFF)
        time.sleep(0.2)


OCT, OCT2, OCT3 = 1, 2, 4

if __name__ == "__main__":
    play_music()
    
    p.stop()
    #controlLED(LEDs, LOW)
    GPIO.cleanup()
