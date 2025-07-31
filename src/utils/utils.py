from PIL import Image
import torch

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
