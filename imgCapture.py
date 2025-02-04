from picamera2 import Picamera2
from libcamera import Transform

import os
import time
from datetime import datetime
from PIL import Image

import torch

# Saving folder
current_path = os.getcwd()
#folder_path_img = "/home/pi/autonomous_vehicle/img"
folder_path_img = os.path.join(current_path, 'img')
folder_path_img_date = os.path.join(folder_path_img, datetime.now().strftime('%y%m%d'))
if not os.path.exists(folder_path_img_date):
    os.makedirs(folder_path_img_date)

# Initialization
last_time = 0

picam2 = Picamera2()
capture_config = picam2.create_preview_configuration(transform=Transform(hflip=1, vflip=1),
                                                     main={"size": (1080, 480)})
picam2.configure(capture_config)
picam2.start()

def setSaveFolderPath(folder_path=folder_path_img):
    folder_path_img_date = os.path.join(folder_path, datetime.now().strftime('%y%m%d'))
    if not os.path.exists(folder_path_img_date):
        os.makedirs(folder_path_img_date)

def capture(motion, interval=0.5, imgSave=False, timeStamp=False):
    global last_time
    
    # Check Interval
    now_time = time.time()
    if now_time - last_time < interval - 0.02:  # 0.02s Compensation Value
        return
    last_time = now_time
    
    # Capture Image
    image = picam2.capture_array()
    image = Image.fromarray(image)
    if image.mode == 'RGBA': image = image.convert('RGB')

    # Save Image
    file_name = f"{folder_path_img_date}/{datetime.now().strftime('%y%m%d_%H%M%S%f')}"[:-3]+f"_{motion}.jpg"
    if imgSave: image.save(file_name)

    # Print Time Stamp
    if timeStamp: print("finished:", now_time)
    
    return image

if __name__ == "__main__":
    for i in range(100):
        start = time.time()
        capture("GO", interval=0.03)
        #print(time.time() - start)
    pass
