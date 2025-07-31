import torch
from torchvision import models, transforms
from PIL import Image
import json
import os

# This file is for standalone inference testing
# The actual model loading is done in fast_api.py

def predict(model, image, transform, class_names, device):
    """
    Predict the disease class of a given leaf image.
    """
    if isinstance(image, str): 
        image = Image.open(image).convert('RGB')
    
    img_tensor = transform(image).unsqueeze(0).to(device)

    model.eval()
    with torch.no_grad():
        outputs = model(img_tensor)
        _, predicted = torch.max(outputs, 1)

    predicted_class = class_names[predicted.item()]
    confidence = torch.softmax(outputs, dim=1)[0][predicted.item()].item() * 100

    return predicted_class, confidence

# Define same transforms used during training
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

# Test inference (only for standalone testing)
if __name__ == "__main__":
    # This is for testing only - the actual app uses fast_api.py
    print("This file is for testing purposes only.")
    print("Run the application using: python run_app.py")