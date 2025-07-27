import torch
from torchvision import models, transforms
from fastapi import FastAPI, File, UploadFile
from utils import predict as predict_image

import json
from PIL import Image
import io

#Api 
app = FastAPI(title="KissanAI Api", description="Farming Asistant")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

#Load Class Names 
with open("class_names.json", "r") as f:
    class_names = json.load(f)

# Load the model
model = models.resnet18(pretrained=False)
model.fc = torch.nn.Linear(model.fc.in_features, len(class_names))
model.load_state_dict(torch.load("crop_disease_model.pth", map_location=device))
model.to(device)
model.eval()

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

