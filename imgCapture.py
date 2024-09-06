from picamera2 import Picamera2
from libcamera import Transform

from datetime import datetime

picam2 = Picamera2()
capture_config = picam2.create_still_configuration(transform=Transform(hflip=1, vflip=1))
picam2.configure(capture_config)
picam2.start()

def capture(motion, folder_path="img"):
    file_name = f"{folder_path}/{datetime.now().strftime('%y%m%d_%H%M%S')}_{motion}.jpg"
    picam2.capture_file(file_name)

if __name__ == "__main__":
    capture("GO")
    pass