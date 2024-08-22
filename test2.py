import RPi.GPIO as GPIO
import time

# GPIO VALUES
TIME_INTERVALS = 0.05
HIGH, LOW = GPIO.HIGH, GPIO.LOW
LED1, LED2, LED3, LED4 = 26, 16, 20, 21
SWT1, SWT2, SWT3, SWT4 =  5,  6, 13, 19
BUZZER = 12
BUZZ_freq = [130.8128, 146.8324, 164.8138, 174.6141]

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

p = GPIO.PWM(BUZZER, 164.8138)

def SWT_PUSHED():
    swt_val = [GPIO.input(SWT1), GPIO.input(SWT2), GPIO.input(SWT3), GPIO.input(SWT4)]
    for i in range(4):
        if swt_val[i] == 1:
            return i+1
    return 0

def LED_CONTROL(led_num, flag):
    if led_num == 0: return
    GPIO.output(LEDs[led_num-1], flag)

def BUZ_CONTROL(buzz_num, flag):
    if buzz_num ==0: return
    if flag:
        p.ChangeFrequency(BUZZ_freq[buzz_num-1])
        p.start(0.01)
    else:
        p.stop()

def record(swt_start):
    last_num = swt_start
    return_flag = 0
    cnt = 1
    while True:
        swt_num = SWT_PUSHED()
        LED_CONTROL(swt_num, HIGH)
        BUZ_CONTROL(swt_num, HIGH)
        if swt_num >= 1 and last_num == swt_num:
            cnt += 1
            
        elif swt_num >= 1 and last_num != swt_num:
            record_list.append([last_num, cnt])
            last_num = swt_num
            cnt = 1
            
        elif swt_num == 0 and last_num == 0:
            cnt += 1
            if cnt > 2 / TIME_INTERVALS:
                return_flag = 1
            
        elif swt_num == 0 and last_num != 0:
            record_list.append([last_num, cnt])
            last_num = swt_num
            cnt = 1

        time.sleep(TIME_INTERVALS)
        LED_CONTROL(swt_num, LOW)
        BUZ_CONTROL(swt_num, LOW)
        if return_flag: break
        

def play_record():
    for swt_num, cnts in record_list:
        LED_CONTROL(swt_num, HIGH)
        BUZ_CONTROL(swt_num, HIGH)
        time.sleep(TIME_INTERVALS * cnts)
        LED_CONTROL(swt_num, LOW)
        BUZ_CONTROL(swt_num, LOW)

record_list = []
try:
    while True:
        swt_start = SWT_PUSHED()
        if swt_start >= 1:
            record(swt_start)
            play_record()
        if record_list:
            print(record_list)
            record_list = []
        time.sleep(0.1)
        
    
except KeyboardInterrupt:
    controlLED(LEDs, LOW)
    p.stop()
    

GPIO.cleanup()
print(record_list)