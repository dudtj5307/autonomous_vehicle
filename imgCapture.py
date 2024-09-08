from picamera2 import Picamera2
from libcamera import Transform

import os
import time
from datetime import datetime

picam2 = Picamera2()
capture_config = picam2.create_still_configuration(transform=Transform(hflip=1, vflip=1))
picam2.configure(capture_config)
picam2.start()

def capture_with_motion(motion, folder_path="/home/pi/autonomous_vehicle/img"):
    if motion=="GO" or motion=="LEFT" or motion =="RIGHT":
        new_path = folder_path + f"/{datetime.now().strftime('%y%m%d')}"
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        file_name = f"{new_path}/{datetime.now().strftime('%y%m%d_%H%M%S')}_{motion}.jpg"
        start = time.time()
        picam2.capture_file(file_name)
        print(time.time() - start)

if __name__ == "__main__":
    capture_with_motion("GO")
    pass
