import imgCapture
from controls import gpios

import os
import time
import random

import torch
import torch.nn as nn
from torchvision import models, transforms

CAPTURE_INTERVAL = 0.5

# Motor Speed Values
MOTOR_SPD_DFT = 40

# Action Values
FRONT = 0
LEFT  = 1
RIGHT = 2

random_list = [0,0,0,0,0,0,0,0,1,2]


preprocess = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),])

current_path = os.getcwd()
saved_model_path = os.path.join(current_path, "weight/effnetlite_250211.pth")
print(saved_model_path)

model = models.efficientnet_b0(weights='DEFAULT')
model.classifier[1] = nn.Linear(in_features=1280, out_features=3)
model.qconfig = torch.quantization.get_default_qconfig('qnnpack')
torch.quantization.prepare_qat(model, inplace=True)
torch.backends.quantized.engine = 'qnnpack'

state_dict = torch.load(saved_model_path, map_location=torch.device("cpu"))

model_state_dict = model.state_dict()
for key in state_dict.keys():
    if key not in model_state_dict:
        print(f"Warning: {key} is not in the model's state_dict")
        
model.load_state_dict(state_dict)

model.eval()

print('model loading complete!')

def main():
    speed = MOTOR_SPD_DFT
    action = FRONT
    last_action = action
    

    try:
        while True:
            start = time.time()
            # Image Capture
            img = imgCapture.capture("None", interval=CAPTURE_INTERVAL, timeStamp=True)

            # Sample input tensor
            input_tensor = torch.randn(1, 3, 224, 224)
            
            # Model Estimation
            with torch.no_grad():
                output = model(input_tensor)
            probabilities = torch.nn.functional.softmax(output, dim=1)
            action = torch.argmax(probabilities, dim=1)
            print(action)

            # Change in Action
            if action.item() != last_action:
                if   action == FRONT: gpios.MOTOR.move_front(speed)
                elif action == LEFT : gpios.MOTOR.move_left(speed)
                elif action == RIGHT: gpios.MOTOR.move_right(speed)
                
                # Update last Action
                last_action = action
            
            print(f"time:{time.time()-start}")
                
            if gpios.SWT_PUSHED():
                return

    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
    gpios.cleanup_GPIOs()

