import serial
import threading

import time

import imgCapture
from controls import controls

# bluetooth Serial
bleSerial = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1.0)
gData = ""

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
    dirFlag = controls.FRONT      # Moving direction (FRONT/BACK)
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
                    controls.moveMotor_stop()
                elif gData == "GO":
                    controls.moveMotor_front(speed)
                    dirFlag = controls.FRONT
                elif gData == "BACK":
                    controls.moveMotor_back(speed)
                    dirFlag = controls.BACK
                elif gData == "LEFT":
                    controls.moveMotor_left(speed, dirFlag)
                elif gData == "RIGHT":
                    controls.moveMotor_right(speed, dirFlag)
                elif gData == "k" or gData == "kill":
                    break
                # Save gData, speed
                last_gData = gData
                last_speed = speed
                
            # Capture image and motion
            start = time.time()
            if last_gData:
                imgCapture.capture_with_motion(last_gData)
                print(time.time()-start)
                
            time.sleep(0.1)
            if controls.SWT_PUSHED():
                gData="STOP"

    except KeyboardInterrupt:
        controls.cleanup_GPIOs()

if __name__ == '__main__':
    # Saving Folder
    new_path = folder_path + f"/{datetime.now().strftime('%y%m%d')}"
    if not os.path.exists(new_path):
        os.makedirs(new_path)
            
    task1 = threading.Thread(target = serial_thread)
    task1.start()
    main()
    controls.cleanup_GPIOs()
    bleSerial.close()


