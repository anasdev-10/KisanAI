# Crop Disease Detection using Deep Learning  

## Overview  
This project, **KissanAI**, is an AI-powered solution to detect plant diseases from leaf images. It uses a fine-tuned **ResNet18** model trained on the PlantVillage dataset to classify multiple crop diseases. The model is deployed with a **FastAPI backend** and integrated with a **React frontend**, providing an interactive interface for users to upload images and receive predictions.  

---

## Features  
- **Deep Learning Model**: Fine-tuned ResNet18 for accurate crop disease classification.  
- **FastAPI Backend**: Serves model predictions via a REST API.  
- **React Frontend**: Modern, responsive UI for uploading images and viewing results.  
- **Multi-Image Support**: Users can upload multiple images at once to get predictions.  
- **Confidence Scores**: Displays the confidence level of predictions.  
- **CORS Enabled**: Smooth integration between frontend and backend.  
- **Future Expansion**: Planned integration with an LLM to provide detailed disease descriptions and treatment suggestions.  

---

## Tech Stack  
- **Frontend**: React, Material UI, Framer Motion  
- **Backend**: FastAPI, PyTorch, Torchvision  
- **Model**: ResNet18 (Fine-tuned on PlantVillage dataset)  
- **Other Tools**: PIL, Python-Multipart, Fetch API  

---

## Installation & Setup  

### 1. Clone the Repository  
\`\`\`bash
git clone https://github.com/anasdev-10/KisanAI.git
cd KisanAI
\`\`\`

### 2. Backend Setup (FastAPI)  
\`\`\`bash
cd backend
python -m venv venv
source venv/bin/activate   # For Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn fast_api:app --reload
\`\`\`
The backend will start on \`http://127.0.0.1:8000\`.

### 3. Frontend Setup (React)  
\`\`\`bash
cd frontend
npm install
npm start
\`\`\`
The frontend will start on \`http://localhost:3000\`.

---

## API Endpoints  

### **POST** \`/predict/\`  
Uploads an image and returns the predicted class with confidence.  

**Request:**  
- Form-data: \`file\` (Image file)  

**Response:**  
\`\`\`json
{
  "predicted_class": "Tomato_Late_Blight",
  "confidence": "95.23%"
}
\`\`\`

---

## Screenshot  
Below is an example of a successful prediction:

![Prediction Screenshot](screenshot/prediction_example.png)

*(Place your screenshot in the \`screenshot\` folder and ensure the path is correct.)*

---

## Folder Structure  
\`\`\`
crop-disease-detection/
│── backend/
│   ├── fast_api.py          # FastAPI backend
│   ├── utils.py             # Prediction utilities
│   ├── crop_disease_model.pth  # Trained model weights
│   └── class_names.json     # Class labels
│
│── frontend/
│   ├── src/
│   │   └── App.js           # React app
│   └── package.json
│
│── screenshot/
│   └── prediction_example.png
│
│── README.md
\`\`\`

---

## Usage  
1. Run the backend server.  
2. Start the React frontend.  
3. Upload one or multiple leaf images.  
4. View the prediction results with confidence scores.  

---

## Future Work  
- Fine-tuning the model with a larger and more diverse dataset.  
- Integration with an **LLM** for dynamic disease descriptions and recommendations.  
- Cloud deployment for public access.  
- Mobile-friendly interface.  

---

## Author  
**Developed by Muhammad Anas**  
Feel free to connect for collaboration and feedback.  
