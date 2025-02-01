import serial
import threading

import time

import imgCapture
from controls import gpios

# bluetooth Serial
bleSerial = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1.0)
gData = ""

# Image Saving Path
imgCapture.setSaveFolderPath("/home/pi/autonomous_vehicle2/img")
IMAGE_CAPTURE_INTERVAL = 0.4

# Motor Speed Values
MOTOR_SPD_DFT = 40
MOTOR_SPD_MIN = 20
MOTOR_SPD_MAX = 60

def serial_thread():
    global gData
    while True:
        newData = bleSerial.readline().decode().strip()
        if newData != "":
            gData = newData
            print(f"[{gData}]")
        if "k" in gData: break
        
            
def main():
    global gData
    last_gData = ""
    speed = MOTOR_SPD_DFT 
    last_speed = MOTOR_SPD_DFT    # Init
    start = time.time()
    try:
        while True:
            # Speed Change
            if gData == "FASTER":
                speed = min(MOTOR_SPD_MAX, speed+10)
                gData = last_gData
            elif gData == "SLOWER":
                speed = max(MOTOR_SPD_MIN, speed-10)
                gData = last_gData

            # Change in Speed or Action
            if gData != last_gData or speed != last_speed:
                if   gData == "STOP" : gpios.MOTOR.move_stop()
                elif gData == "GO"   : gpios.MOTOR.move_front(speed)
                elif gData == "BACK" : gpios.MOTOR.move_back(speed)
                elif gData == "LEFT" : gpios.MOTOR.move_left(speed)
                elif gData == "RIGHT": gpios.MOTOR.move_right(speed)
                elif gData == "kill" : break
                
                # Save gData, speed
                last_gData = gData
                last_speed = speed
                
            # Capture image and motion
            if last_gData in ['GO','LEFT','RIGHT']:
                imgCapture.capture(last_gData, interval=IMAGE_CAPTURE_INTERVAL)
                
            time.sleep(0.05)
            if gpios.SWT_PUSHED():
                gData="STOP"

    except KeyboardInterrupt:
        gpios.cleanup_GPIOs()

if __name__ == '__main__':
    task1 = threading.Thread(target = serial_thread)
    task1.start()
    main()
    gpios.cleanup_GPIOs()
    bleSerial.close()


