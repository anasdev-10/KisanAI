# 🌱 KissanAI - Crop Disease Detection

An AI-powered solution to detect plant diseases from leaf images using deep learning, built with **Streamlit frontend** and **FastAPI backend**.

## 🚀 Features

- **Deep Learning Model**: Fine-tuned ResNet18 for accurate crop disease classification
- **FastAPI Backend**: RESTful API for model predictions
- **Streamlit Frontend**: Modern, responsive UI with dark mode support
- **Multi-Image Support**: Upload multiple images for batch processing
- **Real-time Predictions**: Instant results with confidence scores
- **Progress Tracking**: Visual feedback during processing
- **Cross-platform**: Works on Windows, macOS, and Linux

## 📁 Project Structure

```
KisanAI/
├── src/
│   ├── backend/
│   │   └── fast_api.py          # FastAPI server
│   ├── frontend/
│   │   └── streamlit_app.py     # Streamlit UI
│   └── utils/
│       ├── utils.py             # Utility functions
│       └── inference.py         # ML inference logic
├── models/
│   ├── crop_disease_model.pth   # Trained model (not in repo)
│   ├── class_names.json         # Class labels (not in repo)
│   └── README.md               # Model documentation
├── data/
│   └── README.md               # Data directory info
├── scripts/
│   ├── model_training.ipynb    # Training notebook
│   └── README.md               # Scripts documentation
├── docs/
│   └── README_STREAMLIT.md     # Detailed documentation
├── assets/
│   └── Screenshot 2025-07-27 230856.png
├── requirements.txt            # Python dependencies
├── run_app.py                 # Application launcher
├── run_app.bat               # Windows batch script
├── .gitignore                # Git ignore rules
├── LICENSE                   # Project license
└── README.md                 # This file
```

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- Git

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/KisanAI.git
   cd KisanAI
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Add model files** (Required)
   - Place `crop_disease_model.pth` in `models/` directory
   - Place `class_names.json` in `models/` directory

## 🚀 Running the Application

### Option 1: Quick Start (Recommended)
```bash
python run_app.py
```

### Option 2: Windows Users
```bash
# Double-click run_app.bat
```

### Option 3: Manual Start
```bash
# Terminal 1 - Backend
cd src/backend
uvicorn fast_api:app --host 127.0.0.1 --port 8000 --reload

# Terminal 2 - Frontend
cd src/frontend
streamlit run streamlit_app.py --server.port 8501
```

## 🌐 Access Points

- **Streamlit Frontend**: http://localhost:8501
- **FastAPI Backend**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📱 How to Use

1. **Start the application** using any method above
2. **Open your browser** and go to http://localhost:8501
3. **Upload images** using the file uploader (supports multiple images)
4. **Click "Predict Diseases"** to start analysis
5. **View results** with confidence scores and progress bars
6. **Toggle dark mode** using the theme button

## 🔧 Configuration

### Environment Variables
- `MODEL_PATH`: Path to the trained model file
- `CLASS_NAMES_PATH`: Path to class names JSON file

### Customization
- Modify `src/frontend/streamlit_app.py` for UI changes
- Update `src/backend/fast_api.py` for API modifications
- Adjust styling in the CSS section of the Streamlit app

## 📊 API Endpoints

- `POST /predict/`: Upload image and get disease prediction
  - Input: Image file
  - Output: JSON with predicted class and confidence

## 🎨 UI Features

- **Responsive Design**: Works on desktop and mobile
- **Dark Mode**: Toggle between light and dark themes
- **Progress Indicators**: Visual feedback during processing
- **Image Previews**: Grid layout for uploaded images
- **Result Cards**: Clean display of prediction results

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Muhammad Anas** - 🚀

## 🙏 Acknowledgments

- PlantVillage dataset for training data
- Streamlit and FastAPI communities
- PyTorch and torchvision for deep learning capabilities

---

**Note**: This project has been converted from React to Streamlit for easier deployment and maintenance while maintaining all original functionality.
