import os
import time
import random

import torch
import torch.nn as nn
from torchvision import models, transforms


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

quantized_model = torch.quantization.convert(model, inplace=False)
random_input = torch.randn(1, 3, 244, 244)
print("start trace")
scripted_model = torch.jit.trace(quantized_model, random_input)
print("trace complete")
scripted_model.saved("weight/effnetlite_250211_q_s.pt")

print("Quantization Complete")



