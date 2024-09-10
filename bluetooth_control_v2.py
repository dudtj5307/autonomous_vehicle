import serial
import threading

import time

import imgCapture
from controls import gpios

# bluetooth Serial
bleSerial = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1.0)

# Motor Speed Values
MOTOR_SPD_DFT = 40
MOTOR_SPD_MIN = 20
MOTOR_SPD_MAX = 60

# Image Saving Path
imgCapture.setSaveFolderPath("/home/pi/autonomous_vehicle/img")

gData = ""

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
    dirFlag = gpios.FRONT      # Moving direction (FRONT/BACK)
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
                if gData == "STOP": 
                    gpios.moveMotor_stop()
                elif gData == "GO":
                    gpios.moveMotor_front(speed)
                    dirFlag = gpios.FRONT
                elif gData == "BACK":
                    gpios.moveMotor_back(speed)
                    dirFlag = gpios.BACK
                elif gData == "LEFT":
                    gpios.moveMotor_left(speed, dirFlag)
                elif gData == "RIGHT":
                    gpios.moveMotor_right(speed, dirFlag)
                elif gData == "k" or gData == "kill":
                    break
                # Save gData, speed
                last_gData = gData
                last_speed = speed
                
            # Capture image and motion
            if last_gData in ['GO','LEFT','RIGHT']:
                imgCapture.capture(last_gData, timeDelay=0.4, timeStamp=True)
                
            time.sleep(0.1)
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


