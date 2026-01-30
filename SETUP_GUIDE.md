# Medicinal Plant Identification - Complete Setup Guide

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [System Requirements](#system-requirements)
3. [Installation Steps](#installation-steps)
4. [Project Structure](#project-structure)
5. [Training the Model](#training-the-model)
6. [Running the Web Application](#running-the-web-application)
7. [API Documentation](#api-documentation)
8. [Model Evaluation](#model-evaluation)
9. [Troubleshooting](#troubleshooting)
10. [Future Enhancements](#future-enhancements)

---

## 📱 Project Overview

### Objective
Build an end-to-end deep learning system to identify medicinal plants from leaf images and provide information about their medicinal uses.

### Key Features
- **CNN-based Image Classification**: MobileNetV2 with transfer learning
- **Web Interface**: Flask-based web application with responsive UI
- **Real-time Predictions**: Upload leaf images and get instant predictions
- **Medicinal Information**: Display plant names and medicinal uses
- **Confidence Scores**: Show prediction confidence and alternative predictions
- **Data Augmentation**: Improve model robustness with augmented training data

### Supported Plants
1. **Aloevera** - Skin burns, wounds, digestive health
2. **Bhrami** - Memory enhancement, cognitive improvement
3. **Neem** - Skin health, antibacterial properties
4. **Tulsi** - Cough relief, respiratory health
5. **Turmeric** - Anti-inflammatory, antioxidant properties

---

## 🖥️ System Requirements

### Hardware Requirements
- **Processor**: Intel i5/i7 or equivalent (for training)
- **GPU**: NVIDIA GPU with CUDA support (optional but recommended)
- **RAM**: Minimum 8GB, recommended 16GB
- **Storage**: At least 5GB free space

### Software Requirements
- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, or Linux
- **Package Manager**: pip (comes with Python)

---

## 🚀 Installation Steps

### Step 1: Clone/Download Project
```bash
cd "c:\Final Year Project"
cd MedicinalPlantIdentification
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv env

# Activate virtual environment
# On Windows:
env\Scripts\activate
# On macOS/Linux:
source env/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation
```bash
python -c "import tensorflow; print(f'TensorFlow {tensorflow.__version__} installed successfully')"
```

---

## 📂 Project Structure

```
MedicinalPlantIdentification/
├── dataset/                    # Training dataset
│   ├── Aloevera/
│   ├── Bhrami/
│   ├── Neem/
│   ├── Tulsi/
│   └── Turmeric/
├── models/                     # Trained models and artifacts
│   ├── best_model.h5          # Trained CNN model
│   ├── label_encoder.pkl      # Label encoding
│   ├── preprocessing_params.pkl
│   └── model_info.pkl         # Model metadata
├── webapp/                     # Flask web application
│   ├── app.py                 # Main Flask app
│   ├── templates/             # HTML templates
│   │   ├── index.html
│   │   ├── about.html
│   │   ├── 404.html
│   │   └── 500.html
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── script.js
│   └── uploads/               # Uploaded images
├── src/                        # Source code
│   └── predictor.py           # Prediction utilities
├── notebooks/                  # Jupyter notebooks
│   └── 01_data_exploration.ipynb
├── docs/                       # Documentation
│   ├── MODEL_DOCUMENTATION.md
│   ├── SETUP_GUIDE.md
│   └── API_DOCUMENTATION.md
├── config.py                   # Configuration file
├── requirements.txt            # Python dependencies
├── PROJECT_GUIDE.md           # Project timeline
└── README.md                  # Main README
```

---

## 🤖 Training the Model

### Option 1: Using Jupyter Notebook

```bash
# Start Jupyter
jupyter notebook

# Open notebooks/01_data_exploration.ipynb
# Run all cells in sequence
```

### Option 2: Using Python Script

Create a training script if needed:
```bash
python train_model.py
```

### Training Process
1. **Data Loading**: Load images from dataset folder
2. **Preprocessing**: Resize to 224×224, normalize pixel values
3. **Data Splitting**: 70% train, 15% validation, 15% test
4. **Data Augmentation**: Apply rotation, flip, zoom transformations
5. **Model Training**: MobileNetV2 + custom dense layers
6. **Validation**: Monitor validation accuracy and loss
7. **Model Saving**: Save best model and preprocessing parameters

### Training Parameters
- **Epochs**: 50
- **Batch Size**: 32
- **Learning Rate**: 0.001
- **Early Stopping**: Patience = 10 epochs
- **Optimizer**: Adam

---

## 🌐 Running the Web Application

### Step 1: Navigate to Web App Directory
```bash
cd webapp
```

### Step 2: Start Flask Application
```bash
python app.py
```

### Step 3: Access Web Interface
```
Open your browser and go to: http://localhost:5000
```

### Using the Web Interface
1. **Upload Image**: Click or drag-drop a leaf image
2. **Process**: Click "Identify Plant" button
3. **View Results**: See plant name, confidence, and medicinal uses
4. **Explore**: View predictions for all plant classes

### Web Application Features
- **Image Upload**: Support for JPG, PNG, GIF formats
- **Real-time Prediction**: Instant plant identification
- **Confidence Display**: Visual confidence indicator
- **Medicinal Information**: Complete list of health benefits
- **Alternative Predictions**: Shows predictions for all plant classes
- **Responsive Design**: Works on desktop and mobile devices

---

## 📡 API Documentation

### Endpoints

#### 1. Home Page
```http
GET /
```
Returns the main page with upload interface.

#### 2. Predict
```http
POST /predict
```
**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Parameter: `file` (image file)

**Response:**
```json
{
    "plant": "Neem",
    "confidence": 0.95,
    "success": true,
    "medicinal_uses": [
        "Skin health",
        "Antibacterial properties",
        "Immune boost"
    ],
    "all_predictions": {
        "Neem": 0.95,
        "Tulsi": 0.03,
        "Turmeric": 0.01,
        "Aloevera": 0.01,
        "Bhrami": 0.00
    },
    "image_path": "/uploads/leaf.jpg"
}
```

#### 3. Plant Information
```http
GET /info/<plant_name>
```
**Response:**
```json
{
    "medicinal_uses": ["Use 1", "Use 2", "Use 3"],
    "image": "plant.jpg"
}
```

#### 4. Model Information
```http
GET /api/model-info
```
**Response:**
```json
{
    "model_type": "MobileNetV2 Transfer Learning",
    "test_accuracy": 0.92,
    "test_loss": 0.23,
    "classes": ["Aloevera", "Bhrami", "Neem", "Tulsi", "Turmeric"],
    "number_of_classes": 5
}
```

---

## 📊 Model Evaluation

### Evaluation Metrics
- **Accuracy**: Overall correctness of predictions
- **Precision**: Correctness among predicted positives per class
- **Recall**: Coverage of actual positives per class
- **F1-Score**: Harmonic mean of precision and recall
- **Confusion Matrix**: Shows prediction distribution

### Expected Performance
- **Test Accuracy**: 90-95%
- **Confidence Threshold**: 70% (adjustable in config.py)

### Viewing Results
Run the Jupyter notebook to see:
- Training vs Validation curves
- Confusion matrix visualization
- Per-class metrics
- Classification report

---

## 🔧 Troubleshooting

### Issue: Model Not Loading
```
Error: Model file not found at models/best_model.h5
```
**Solution:**
1. Ensure you've run the training notebook
2. Check that best_model.h5 exists in models/ directory
3. Verify the path is correct in app.py

### Issue: Image Upload Fails
```
Error: File type not allowed
```
**Solution:**
- Use supported formats: JPG, JPEG, PNG, GIF
- Check file size (max 16MB)
- Ensure image is not corrupted

### Issue: TensorFlow Version Conflict
```
Error: Module 'tensorflow' has no attribute 'keras'
```
**Solution:**
```bash
pip install --upgrade tensorflow==2.13.0
```

### Issue: CUDA/GPU Not Detected
```
Warning: GPU not available
```
**Solution:**
- Install NVIDIA CUDA Toolkit
- Install cuDNN
- Set CUDA_HOME environment variable
- Or continue using CPU (slower but works)

---

## 🚀 Future Enhancements

### Model Improvements
- [ ] Increase dataset size (more images per class)
- [ ] Fine-tune hyperparameters
- [ ] Ensemble multiple models
- [ ] Deploy on edge devices (TensorFlow Lite)

### Feature Additions
- [ ] User authentication and history
- [ ] Export predictions as PDF report
- [ ] Batch image processing
- [ ] Integration with medicinal plant database
- [ ] Multi-language support

### Technical Improvements
- [ ] Docker containerization
- [ ] Cloud deployment (AWS, Azure, GCP)
- [ ] REST API with Swagger documentation
- [ ] Database integration for image storage
- [ ] Model versioning and monitoring

### Deployment
- [ ] Deploy on Heroku
- [ ] Deploy on AWS EC2
- [ ] Deploy on Azure App Service
- [ ] Mobile app (React Native/Flutter)

---

## 📚 References

### Research Papers
- MobileNetV2: https://arxiv.org/abs/1801.04381
- Transfer Learning: https://arxiv.org/abs/1411.1792
- ImageNet Classification: https://arxiv.org/abs/1512.03385

### Documentation
- TensorFlow: https://www.tensorflow.org
- Flask: https://flask.palletsprojects.com
- Keras: https://keras.io

### Medicinal Plants
- Traditional Medicine Database
- Ayurvedic Plant Information
- Botanical Classification

---

## 📝 Notes for Evaluation

### For Your Evaluators/Reviewers:

1. **Dataset Location**: Plant images are in `dataset/` folder
2. **Model Training**: Run the Jupyter notebook in `notebooks/` to train
3. **Web Application**: Run `python app.py` from `webapp/` directory
4. **API Testing**: Use tools like Postman or cURL to test endpoints
5. **Model Accuracy**: Check metrics in the Jupyter notebook output

### Important Files:
- **Model**: `models/best_model.h5`
- **Configuration**: `config.py`
- **Web App**: `webapp/app.py`
- **Predictor**: `src/predictor.py`

---

**Project Completed: January 2026**  
**Status**: Ready for Evaluation  
**Student**: BTech CSE-AIML Final Year  

---

For questions or issues, refer to the Troubleshooting section or check the inline code comments.
