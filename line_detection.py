from picamera2 import Picamera2
import cv2
import numpy as np
from datetime import datetime

picam2 = Picamera2()
config = picam2.create_still_configuration(main={"size": (640, 480)})
picam2.configure(config)


picam2.start()
image = picam2.capture_array()
picam2.stop()
    
height, width, _ = image.shape
print(height, width)

file_name = f"img/capture_image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
cv2.imwrite(file_name, image)

cv2.imshow("Cropped Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
