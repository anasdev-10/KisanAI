import torch
from torchvision import models, transforms
from fastapi import FastAPI, File, UploadFile
import sys
import os

# Add src/utils to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from utils import predict as predict_image

import json
from PIL import Image
import io

#Api 
app = FastAPI(title="KissanAI Api", description="Farming Asistant")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load Class Names - look in models directory
model_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'models')
class_names_path = os.path.join(model_dir, "class_names.json")
model_path = os.path.join(model_dir, "crop_disease_model.pth")

try:
    with open(class_names_path, "r") as f:
        class_names = json.load(f)
except FileNotFoundError:
    print(f"Warning: class_names.json not found at {class_names_path}")
    print("Please ensure the model files are in the models/ directory")
    class_names = ["Unknown"]

# Load the model
try:
    model = models.resnet18(pretrained=False)
    model.fc = torch.nn.Linear(model.fc.in_features, len(class_names))
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()
    print("✅ Model loaded successfully")
except FileNotFoundError:
    print(f"Warning: crop_disease_model.pth not found at {model_path}")
    print("Please ensure the model files are in the models/ directory")
    model = None

#Define same transforms
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

#Api endpoint 
@app.post("/predict/")
async def predict(file: UploadFile = File(...)): 
    if model is None:
        return {"error": "Model not loaded. Please check model files."}
    
    image_bytes = await file.read() 
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    
    #Call Utility Function 
    predicted_class, confidence = predict_image(model, image, transform, class_names, device)
    print("Predicted:", predicted_class, "Confidence:", confidence)
    return {
        "predicted_class": predicted_class,
        "confidence": f"{confidence:.2f}%"
    }

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

