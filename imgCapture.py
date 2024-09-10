from picamera2 import Picamera2
from libcamera import Transform

import os
import time
from PIL import Image
from datetime import datetime

# Saving folder
default_path="/home/pi/autonomous_vehicle/img"
saveFoler_path = default_path + f"/{datetime.now().strftime('%y%m%d')}"
if not os.path.exists(saveFoler_path): os.makedirs(saveFoler_path)

# Initialization
start, end = time.time(), time.time()

picam2 = Picamera2()
capture_config = picam2.create_preview_configuration(transform=Transform(hflip=1, vflip=1),
                                                     main={"size": (1080, 480)})
picam2.configure(capture_config)
picam2.start()

def setSaveFolderPath(folder_path=default_path):
    saveFoler_path = folder_path + f"/{datetime.now().strftime('%y%m%d')}"

def capture(motion, timeDelay=0.0, timeStamp=False):
    global start, end
    file_name = f"{saveFoler_path}/{datetime.now().strftime('%y%m%d_%H%M%S%f')}"[:-3]+f"_{motion}.jpg"
    start = time.time()
    if start - end < timeDelay:
        return
    image = picam2.capture_array()
    image = Image.fromarray(image)
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    image.save(file_name)
    end = time.time()
    if timeStamp: print(f'{end-start:2f}')

if __name__ == "__main__":
    for i in range(10):
        start = time.time()
        capture("GO")
    pass
