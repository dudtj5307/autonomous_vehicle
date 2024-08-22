import serial
import threading

import RPi.GPIO as GPIO
import time
import booting_music

from controls import controls

# bluetooth Serial
bleSerial = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1.0)
gData = ""

# GPIO VALUES
HIGH, LOW = GPIO.HIGH, GPIO.LOW
FRONT, BACK = 0, 1

BUZZER = 12

# GPIO SETUPS
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

def serial_thread():
    global gData
    while True:
        newData = bleSerial.readline().decode()
        if newData != "":
            gData = newData
        if "k" in gData: break
        
            
def main():
    global gData
    last_gData = ""             # Save gData info
    speed, last_speed = 30, 30  # Save speed info
    dirFlag = FRONT             # Save moving direction (FRONT: 0, BACK: 1)
    try:
        while True:
            if "FASTER" in gData:
                speed = min(60, speed+10)
                gData = last_gData

            elif "SLOWER" in gData:
                speed = max(20, speed-10)
                gData = last_gData

            if gData != last_gData or speed != last_speed:
                if "STOP" in gData: 
                    controls.moveMotor_stop()
                    controls.LED_CONTROL([0,1,2,3], LOW)
                    
                elif "GO" in gData:
                    controls.moveMotor_front(speed)
                    controls.LED_CONTROL([0,1], HIGH)
                    controls.LED_CONTROL([2,3], LOW)
                    dirFlag = FRONT
                    
                elif "BACK" in gData:
                    controls.moveMotor_back(speed)
                    controls.LED_CONTROL([0,1], LOW)
                    controls.LED_CONTROL([2,3], HIGH)
                    dirFlag = BACK
                    
                elif "LEFT" in gData:
                    controls.moveMotor_left(speed, dirFlag)
                    controls.LED_CONTROL([0,2], HIGH)
                    controls.LED_CONTROL([1,3], LOW)
                    
                elif "RIGHT" in gData:
                    controls.moveMotor_right(speed, dirFlag)
                    controls.LED_CONTROL([0,2], LOW)
                    controls.LED_CONTROL([1,3], HIGH)

                elif "k" in gData or "kill" in gData:
                    break

                last_gData = gData
                last_speed = speed

            time.sleep(0.1)
            if controls.SWT_PUSHED():
                gData="STOP"

    except KeyboardInterrupt:
        controls.cleanup_GPIOs()

if __name__ == '__main__':
    task1 = threading.Thread(target = serial_thread)
    task1.start()
    main()
    controls.cleanup_GPIOs()
    bleSerial.close()
    GPIO.cleanup()


