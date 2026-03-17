# 🏗️ Project Architecture & Technical Overview

## Complete System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER BROWSER                             │
│  (http://localhost:5000)                                   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Frontend (HTML/CSS/JavaScript)                      │  │
│  │  - index.html (Main UI)                              │  │
│  │  - style.css (Styling)                               │  │
│  │  - script_new.js (User interactions)                 │  │
│  │                                                       │  │
│  │  Features:                                           │  │
│  │  ✓ Drag-drop file upload                             │  │
│  │  ✓ Image preview before prediction                   │  │
│  │  ✓ Loading spinner                                   │  │
│  │  ✓ Results display with confidence bar               │  │
│  │  ✓ Medicinal uses list                               │  │
│  │  ✓ All predictions comparison                        │  │
│  └──────────────────────────────────────────────────────┘  │
│                          │                                   │
│                    Fetch API (POST)                          │
│                          │                                   │
└─────────────────────────┼─────────────────────────────────┘
                          │
┌─────────────────────────┼─────────────────────────────────┐
│         FLASK BACKEND (Python)                             │
│         (webapp/app.py)                                    │
│                          │                                  │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ HTTP Routes & Handlers                              │  │
│  │                                                      │  │
│  │ GET  /                - Serve index.html            │  │
│  │ GET  /about           - About page                  │  │
│  │ GET  /info/<plant>    - Plant information JSON      │  │
│  │ POST /predict         - Image upload & prediction   │  │
│  │ GET  /uploads/<file>  - Serve uploaded images       │  │
│  │ GET  /api/model-info  - Model metadata              │  │
│  └──────────────────────────────────────────────────────┘  │
│                          │                                  │
│                    Import & Process                         │
│                          │                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  PlantPredictor Class (src/predictor.py)             │  │
│  │                                                       │  │
│  │  Methods:                                            │  │
│  │  • __init__() - Load model & encoders                │  │
│  │  • preprocess_image() - Prepare image (224x224)      │  │
│  │  • predict() - Run model inference                   │  │
│  │                                                       │  │
│  │  Process Flow:                                       │  │
│  │  1. Read image with OpenCV                           │  │
│  │  2. Resize to 224x224 pixels                         │  │
│  │  3. Convert BGR → RGB color space                    │  │
│  │  4. Normalize pixel values (0-1)                     │  │
│  │  5. Add batch dimension                              │  │
│  │  6. Pass to TensorFlow model                         │  │
│  │  7. Get confidence scores for each plant             │  │
│  └──────────────────────────────────────────────────────┘  │
│                          │                                  │
│                    Load Models                              │
│                          │                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Trained Models & Artifacts (models/)                │  │
│  │                                                       │  │
│  │  • best_model.h5                                     │  │
│  │    - MobileNetV2 CNN (Transfer Learning)             │  │
│  │    - Input: 224x224x3 RGB images                     │  │
│  │    - Output: 5 plant classes                         │  │
│  │    - Trained on: 1000+ leaf images                   │  │
│  │                                                       │  │
│  │  • label_encoder.pkl                                 │  │
│  │    - Maps class indices → plant names                │  │
│  │    - Classes: Aloevera, Bhrami, Neem, Tulsi, Turmeric
│  │                                                       │  │
│  │  • preprocessing_params.pkl                          │  │
│  │    - Image height/width (224x224)                    │  │
│  │    - Normalization factor (255.0)                    │  │
│  │    - Used during prediction for consistency          │  │
│  │                                                       │  │
│  │  • model_info.pkl                                    │  │
│  │    - Model metadata (architecture, training time)    │  │
│  │    - Accuracy, loss metrics                          │  │
│  │    - Training configuration                          │  │
│  └──────────────────────────────────────────────────────┘  │
│                          │                                  │
│                    Return Results                           │
│                          │                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Response JSON (to browser)                          │  │
│  │                                                       │  │
│  │  {                                                    │  │
│  │    "success": true/false,                            │  │
│  │    "plant": "Plant Name",                            │  │
│  │    "confidence": 0.95,                               │  │
│  │    "medicinal_uses": ["use1", "use2", ...],          │  │
│  │    "all_predictions": {                              │  │
│  │      "Neem": 0.95,                                   │  │
│  │      "Tulsi": 0.03,                                  │  │
│  │      ...                                              │  │
│  │    },                                                │  │
│  │    "image_path": "/uploads/filename.jpg",            │  │
│  │    "message": "Prediction successful"                │  │
│  │  }                                                    │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘
```

---

## 📁 File Structure & Purpose

### Core Application Files

```
MedicinalPlantIdentification/
│
├── config.py                        # Configuration constants
│   ├── Plant classes & medicinal uses
│   ├── Image dimensions (224x224)
│   ├── Model confidence threshold (0.7)
│   ├── Allowed file extensions
│   └── Dataset paths
│
├── webapp/
│   ├── app.py                       # Main Flask application
│   │   ├── Initialize Flask app
│   │   ├── Load model & predictor
│   │   ├── Define all routes
│   │   ├── Handle file uploads
│   │   ├── Make predictions
│   │   └── Serve results
│   │
│   ├── templates/
│   │   ├── index.html               # Main page
│   │   │   ├── Upload form
│   │   │   ├── Results display
│   │   │   └── Plant gallery
│   │   ├── about.html               # About page
│   │   ├── 404.html                 # 404 error page
│   │   └── 500.html                 # 500 error page
│   │
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css            # Styling
│   │   │       ├── Colors & gradients
│   │   │       ├── Responsive layout
│   │   │       ├── Animation effects
│   │   │       └── Component styles
│   │   │
│   │   └── js/
│   │       ├── script.js            # Original script
│   │       └── script_new.js        # Enhanced script (USED)
│   │           ├── Image preview
│   │           ├── Form handling
│   │           ├── Fetch API calls
│   │           └── Results display
│   │
│   └── uploads/                     # User uploaded images
│       └── [uploaded files here]
│
├── src/
│   ├── predictor.py                 # Prediction logic
│   │   ├── PlantPredictor class
│   │   ├── Image preprocessing
│   │   ├── Model inference
│   │   └── Confidence calculation
│   │
│   └── __pycache__/                 # Compiled Python files
│
├── models/                          # Trained model artifacts
│   ├── best_model.h5                # CNN model weights
│   ├── label_encoder.pkl            # Class encoder
│   ├── preprocessing_params.pkl     # Image params
│   ├── model_info.pkl               # Metadata
│   ├── training_curves.png          # Training graph
│   ├── confusion_matrix.png         # Metrics visualization
│   ├── class_distribution.png       # Dataset distribution
│   └── sample_images.png            # Sample predictions
│
├── dataset/                         # Training dataset
│   ├── Aloevera/                    # ~250 images
│   ├── Bhrami/                      # ~250 images
│   ├── Neem/                        # ~250 images
│   ├── Tulsi/                       # ~250 images
│   └── Turmeric/                    # ~250 images
│
└── Documentation files
    ├── README.md                    # Project overview
    ├── QUICK_START.md               # 5-minute setup
    ├── SETUP_GUIDE.md               # Detailed setup
    ├── TESTING_GUIDE.md             # Testing procedures
    ├── PROJECT_GUIDE.md             # Development timeline
    └── docs/
        └── API_DOCUMENTATION.md     # API reference
```

---

## 🔄 Complete Request-Response Flow

### User Uploads Image & Clicks Predict

```
1. FRONTEND (Browser)
   ├─ User selects image
   ├─ JavaScript reads file
   ├─ Preview image displayed
   └─ User clicks "Identify Plant"

2. FRONTEND → BACKEND (JavaScript)
   ├─ Create FormData with image
   ├─ Send POST request to /predict
   ├─ Show loading spinner
   └─ Wait for response (5-10 seconds)

3. BACKEND (Flask - app.py)
   ├─ Receive POST request
   ├─ Validate file type & size
   ├─ Save file to uploads/ folder
   ├─ Print debug info to console
   └─ Call predictor.predict()

4. BACKEND (src/predictor.py)
   ├─ Load image with OpenCV
   ├─ Resize to 224x224 pixels
   ├─ Convert color space (BGR→RGB)
   ├─ Normalize pixel values
   ├─ Add batch dimension
   ├─ Pass to TensorFlow model
   ├─ Get confidence scores
   ├─ Find top prediction
   ├─ Check against threshold
   └─ Return results dict

5. BACKEND (app.py cont.)
   ├─ Get medicinal uses from config
   ├─ Build response JSON
   ├─ Return with status 200
   └─ Print success message

6. FRONTEND (JavaScript)
   ├─ Receive JSON response
   ├─ Parse results
   ├─ Hide loading spinner
   ├─ Extract plant name
   ├─ Extract confidence
   ├─ Extract medicinal uses
   ├─ Extract all predictions
   └─ Call displayResults()

7. FRONTEND (DOM Manipulation)
   ├─ Set uploaded image src
   ├─ Set plant name text
   ├─ Set confidence % width
   ├─ Create medicinal uses list
   ├─ Create prediction bars
   ├─ Show results section
   └─ Scroll to results

8. USER SEES
   ✓ Uploaded image
   ✓ Plant name with confidence
   ✓ Medicinal uses with checkmarks
   ✓ All plant predictions bars
   ✓ "Identify Another Plant" button
```

---

## 🤖 Machine Learning Pipeline

### Model Architecture (MobileNetV2 + Custom Head)

```
Input Layer (224 × 224 × 3)
    ↓
MobileNetV2 (Pre-trained on ImageNet)
    ├─ Depthwise Separable Convolutions
    ├─ Batch Normalization
    ├─ ReLU Activations
    └─ Residual Connections
    ↓
Global Average Pooling
    ↓
Fully Connected Layers (Dense)
    ├─ 512 units → ReLU
    ├─ Dropout (0.5)
    ├─ 256 units → ReLU
    ├─ Dropout (0.5)
    └─ 5 units → Softmax
    ↓
Output (5 classes)
    ├─ Aloevera
    ├─ Bhrami
    ├─ Neem
    ├─ Tulsi
    └─ Turmeric
```

### Training Configuration

```
Optimizer: Adam
Loss: Categorical Crossentropy
Metrics: Accuracy
Epochs: 50 (with Early Stopping)
Batch Size: 32
Learning Rate: 0.001
Validation Split: 15%
Test Split: 15%

Data Augmentation:
├─ Rotation (20°)
├─ Horizontal Flip
├─ Zoom (0.2)
├─ Brightness adjustment
└─ Width/Height shift
```

### Model Performance

```
Classes Trained: 5 medicinal plants
Total Images: 1000+
Train/Val/Test Split: 70% / 15% / 15%

Expected Accuracy:
├─ Training: ~95-98%
├─ Validation: ~85-92%
└─ Test: ~80-90%

Confidence Threshold: 0.70 (70%)
```

---

## 🔐 Configuration & Constants

### config.py

```python
# Image Processing
IMG_HEIGHT = 224
IMG_WIDTH = 224
IMG_CHANNELS = 3
BATCH_SIZE = 32

# Model Training
EPOCHS = 50
LEARNING_RATE = 0.001
PATIENCE = 10  # Early stopping

# Prediction
CONFIDENCE_THRESHOLD = 0.7  # 70% minimum confidence

# Files
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}

# Plant Classes with Medicinal Uses
PLANT_CLASSES = {
    'Aloevera': {
        'medicinal_uses': [
            'Skin burns and wounds',
            'Digestive health',
            'Anti-inflammatory'
        ]
    },
    'Bhrami': {
        'medicinal_uses': [
            'Memory enhancement',
            'Cognitive improvement',
            'Anxiety relief'
        ]
    },
    'Neem': {
        'medicinal_uses': [
            'Skin health',
            'Antibacterial properties',
            'Immune boost'
        ]
    },
    'Tulsi': {
        'medicinal_uses': [
            'Cough and cold relief',
            'Respiratory health',
            'Stress reduction'
        ]
    },
    'Turmeric': {
        'medicinal_uses': [
            'Anti-inflammatory',
            'Antioxidant',
            'Joint health'
        ]
    }
}
```

---

## 🚀 Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Backend Framework** | Flask 3.0+ | Web application |
| **ML Framework** | TensorFlow 2.14+ | Deep learning |
| **Image Processing** | OpenCV 4.8+ | Image manipulation |
| **Data Processing** | NumPy, Pandas | Data handling |
| **ML Utilities** | Scikit-learn | Label encoding |
| **Frontend** | HTML5/CSS3 | User interface |
| **Interactivity** | JavaScript (ES6) | User interactions |
| **File Handling** | Werkzeug | Secure uploads |
| **Visualization** | Matplotlib, Seaborn | Charts & graphs |
| **Virtual Env** | venv | Python isolation |
| **Package Mgmt** | pip | Dependency management |

---

## 📊 Data Flow Diagram

```
User Input (Image)
    ↓
Browser Upload Form
    ↓
JavaScript FormData
    ↓
HTTP POST /predict
    ↓
Flask Route Handler
    ↓
File Validation
    ↓
Save to Disk (uploads/)
    ↓
Load with OpenCV
    ↓
Preprocess (Resize, Normalize)
    ↓
TensorFlow Model Inference
    ↓
Get Confidence Scores (5 values)
    ↓
Find Max Score & Class
    ↓
Check Threshold (>0.7?)
    ↓
    ├─ YES → Fetch Medicinal Uses
    │        → Build Success Response
    │
    └─ NO  → Build Low Confidence Response
    ↓
Return JSON Response
    ↓
JavaScript Parse & Display
    ↓
Update DOM with Results
    ↓
User Sees Plant Info
```

---

## 🔧 Key Features & Implementation

### 1. Drag-Drop Upload
```javascript
// In script_new.js
fileInputWrapper.addEventListener('drop', handleDrop)
→ Prevents default behavior
→ Gets file from DataTransfer
→ Triggers preview
```

### 2. Image Preview
```javascript
// Before prediction, show preview
FileReader() → DataURL → IMG src
→ User can change before predicting
```

### 3. Loading Indicator
```javascript
// Show during prediction (5-10s wait)
spinner.style.display = 'flex'
→ User knows app is processing
→ Hide on success/error
```

### 4. Confidence Visualization
```css
/* Confidence bar fills to percentage */
<div class="confidence-fill" style="width: 85%">
→ Visual feedback of model confidence
```

### 5. Comparison View
```javascript
// Show all 5 plant predictions
Object.entries(data.all_predictions).sort()
→ Sorted by confidence
→ Bar charts for each plant
```

---

## 🛡️ Error Handling

### Frontend Errors
```javascript
.catch(error => {
    displayError('Error: ' + error.message)
})
```

### Backend Errors
```python
try:
    # prediction logic
except Exception as e:
    return {'success': False, 'error': str(e)}
```

### File Upload Errors
- File type validation
- File size validation (max 16MB)
- File save verification
- Model loading verification

---

## 📈 Performance Optimization

1. **Model Loading**: Once on startup (not per request)
2. **Image Caching**: Saved uploads available for display
3. **Efficient Preprocessing**: OpenCV for fast resizing
4. **Async Frontend**: Fetch API with loading indicator
5. **Minimal CSS**: Single stylesheet with reusable classes

---

## 🎯 Summary

Your project implements:
- ✅ **CNN-based classification** with Transfer Learning
- ✅ **Web interface** with drag-drop upload
- ✅ **Real-time predictions** with confidence scores
- ✅ **Medicinal information** database
- ✅ **Error handling** and validation
- ✅ **Responsive design** for all devices
- ✅ **Professional UI/UX** with animations
- ✅ **Production-ready code** with logging

This is a complete, working medicinal plant identification system!

