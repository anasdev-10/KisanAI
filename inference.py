import torch
from torchvision import models, transforms
from PIL import Image
import json
from utils import predict


# Load class names
with open("class_names.json", "r") as f:
    class_names = json.load(f)


# Load the same model architecture
model = models.resnet18(pretrained=False)
model.fc = torch.nn.Linear(model.fc.in_features, len(class_names))
model.load_state_dict(torch.load("crop_disease_model.pth", map_location=torch.device('cpu')))
model.eval()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

#Define same transforms used during training
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

'''#Prediction Function 
def predict(image_path):
    image = Image.open(image_path).convert('RGB')
    img_tensor = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(img_tensor)
        _, predicted = torch.max(outputs, 1)
    
    predicted_class = class_names[predicted.item()]
    confidence = torch.softmax(outputs, dim=1)[0][predicted.item()].item() * 100

    return predicted_class, confidence'''

'''import inspect
print(inspect.signature(predict))
#Test inference
if __name__ == "__main__":
    img_path = "C:/Users/LENOVO/.vscode/Crop disease/backend/test_leaf.jpeg"  # sample test image
    label, conf = predict(model, img_path, transform, class_names, device)
    print(f"Predicted: {label} (Confidence: {conf:.2f}%)")'''