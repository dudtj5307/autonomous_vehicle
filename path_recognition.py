import imgCapture
from controls import gpios

import time
import random

CAPTURE_INTERVAL = 0.5

# Motor Speed Values
MOTOR_SPD_DFT = 40

# Action Values
FRONT = 0
LEFT  = 1
RIGHT = 2

random_list = [0,0,0,0,0,0,0,0,1,2]

def main():
    speed = MOTOR_SPD_DFT
    action = FRONT
    last_action = action
    
    try:
        while True:
            # Image Capture
            img = imgCapture.capture("None", interval=CAPTURE_INTERVAL, timeStamp=True)
            print(img)
            
            # Action decision
            action = random.choice(random_list)
            
            # Change in Action
            if action != last_action:
                if   action == FRONT: gpios.MOTOR.move_front(speed)
                elif action == LEFT : gpios.MOTOR.move_left(speed)
                elif action == RIGHT: gpios.MOTOR.move_right(speed)
                
                # Update last Action
                last_action = action
                
            time.sleep(0.4)
            if gpios.SWT_PUSHED():
                return

    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
    gpios.cleanup_GPIOs()

