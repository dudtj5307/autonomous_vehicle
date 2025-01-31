from picamera2 import Picamera2
from libcamera import Transform

import os
import time
from PIL import Image
from datetime import datetime

# Saving folder
current_path = os.getcwd()
#folder_path_img = "/home/pi/autonomous_vehicle/img"
folder_path_img = os.path.join(current_path, 'img')
folder_path_img_date = os.path.join(folder_path_img, datetime.now().strftime('%y%m%d'))
if not os.path.exists(folder_path_img_date):
    os.makedirs(folder_path_img_date)

# Initialization
start, end = time.time(), time.time()

picam2 = Picamera2()
capture_config = picam2.create_preview_configuration(transform=Transform(hflip=1, vflip=1),
                                                     main={"size": (1080, 480)})
picam2.configure(capture_config)
picam2.start()

def setSaveFolderPath(folder_path=folder_path_img):
    folder_path_img_date = os.path.join(folder_path_img, datetime.now().strftime('%y%m%d'))
    if not os.path.exists(folder_path_img_date):
        os.makedirs(folder_path_img_date)

def capture(motion, timeDelay=0.0, timeStamp=False):
    global start, end
    file_name = f"{folder_path_img_date}/{datetime.now().strftime('%y%m%d_%H%M%S%f')}"[:-3]+f"_{motion}.jpg"
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
