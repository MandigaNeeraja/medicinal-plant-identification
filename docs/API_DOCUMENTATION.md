# Medicinal Plant Identification - API Documentation

## Overview
REST API for medicinal plant identification using CNN-based image classification.

## Base URL
```
http://localhost:5000
```

## Authentication
No authentication required for current version.

## Rate Limiting
Currently no rate limiting implemented.

---

## Endpoints

### 1. Get Home Page
**Endpoint:** `GET /`

**Description:** Returns the main web interface

**Response:**
- Status: 200 OK
- Content-Type: text/html

**Example:**
```bash
curl http://localhost:5000/
```

---

### 2. Upload Image and Predict
**Endpoint:** `POST /predict`

**Description:** Upload a leaf image and get plant identification with medicinal information

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Parameter: `file` (required) - Image file (JPG, PNG, GIF)

**Response:**
- Status: 200 OK (success) or 400/500 (error)
- Content-Type: application/json

**Success Response:**
```json
{
    "plant": "Neem",
    "confidence": 0.9534,
    "success": true,
    "medicinal_uses": [
        "Skin health",
        "Antibacterial properties",
        "Immune boost"
    ],
    "all_predictions": {
        "Aloevera": 0.0012,
        "Bhrami": 0.0001,
        "Neem": 0.9534,
        "Tulsi": 0.0401,
        "Turmeric": 0.0052
    },
    "image_path": "/uploads/sample_image.jpg",
    "message": "Prediction successful"
}
```

**Error Response:**
```json
{
    "error": "File type not allowed. Allowed types: png, jpg, jpeg, gif"
}
```

**Curl Example:**
```bash
curl -X POST -F "file=@leaf.jpg" http://localhost:5000/predict
```

**Python Example:**
```python
import requests

files = {'file': open('leaf.jpg', 'rb')}
response = requests.post('http://localhost:5000/predict', files=files)
result = response.json()
print(f"Plant: {result['plant']}")
print(f"Confidence: {result['confidence']:.2%}")
```

**JavaScript Example:**
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:5000/predict', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => {
    console.log(`Plant: ${data.plant}`);
    console.log(`Confidence: ${(data.confidence * 100).toFixed(1)}%`);
});
```

---

### 3. Get Plant Information
**Endpoint:** `GET /info/<plant_name>`

**Description:** Get medicinal information about a specific plant

**Parameters:**
- `plant_name` (string, required) - Name of the plant
  - Valid values: `Aloevera`, `Bhrami`, `Neem`, `Tulsi`, `Turmeric`

**Response:**
- Status: 200 OK (found) or 404 (not found)
- Content-Type: application/json

**Success Response:**
```json
{
    "medicinal_uses": [
        "Skin burns and wounds",
        "Digestive health",
        "Anti-inflammatory"
    ],
    "image": "aloevera.jpg"
}
```

**Error Response:**
```json
{
    "error": "Plant not found"
}
```

**Curl Example:**
```bash
curl http://localhost:5000/info/Neem
```

---

### 4. Get Model Information
**Endpoint:** `GET /api/model-info`

**Description:** Get information about the trained model

**Response:**
- Status: 200 OK
- Content-Type: application/json

**Response Format:**
```json
{
    "model_type": "MobileNetV2 Transfer Learning",
    "architecture": "MobileNetV2 + Dense Layers",
    "training_samples": 1400,
    "validation_samples": 300,
    "test_samples": 200,
    "number_of_classes": 5,
    "classes": ["Aloevera", "Bhrami", "Neem", "Tulsi", "Turmeric"],
    "test_accuracy": 0.92,
    "test_loss": 0.2341
}
```

**Curl Example:**
```bash
curl http://localhost:5000/api/model-info
```

---

### 5. Get About Page
**Endpoint:** `GET /about`

**Description:** Returns the about page with project information

**Response:**
- Status: 200 OK
- Content-Type: text/html

**Curl Example:**
```bash
curl http://localhost:5000/about
```

---

## Error Handling

### Common Error Codes

#### 400 Bad Request
```json
{
    "error": "No file provided"
}
```

#### 404 Not Found
```json
{
    "error": "Plant not found"
}
```

#### 500 Internal Server Error
```json
{
    "error": "Model not loaded. Please restart the application."
}
```

---

## Request/Response Examples

### Example 1: Complete Prediction Flow

```bash
# Step 1: Upload and predict
curl -X POST -F "file=@my_leaf.jpg" http://localhost:5000/predict > prediction.json

# Step 2: Get model info
curl http://localhost:5000/api/model-info > model_info.json
```

### Example 2: Python Integration

```python
import requests
from PIL import Image
from io import BytesIO

def identify_plant(image_path):
    """Identify a plant from an image"""
    
    with open(image_path, 'rb') as f:
        files = {'file': f}
        response = requests.post('http://localhost:5000/predict', files=files)
    
    if response.status_code == 200:
        data = response.json()
        if data['success']:
            return {
                'plant': data['plant'],
                'confidence': data['confidence'],
                'uses': data['medicinal_uses']
            }
    return None

# Usage
result = identify_plant('leaf.jpg')
print(f"Identified Plant: {result['plant']}")
print(f"Confidence: {result['confidence']:.1%}")
print(f"Uses: {', '.join(result['uses'])}")
```

### Example 3: JavaScript Integration

```javascript
async function predictPlant(fileInput) {
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    
    try {
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            console.log(`Plant: ${data.plant}`);
            console.log(`Confidence: ${(data.confidence * 100).toFixed(1)}%`);
            console.log(`Medicinal Uses:`);
            data.medicinal_uses.forEach(use => console.log(`  - ${use}`));
        } else {
            console.error(`Prediction failed: ${data.message}`);
        }
    } catch (error) {
        console.error('API Error:', error);
    }
}
```

---

## Response Fields Explanation

### Prediction Response Fields
- **plant** (string): Identified plant name
- **confidence** (float): Confidence score (0-1)
- **success** (boolean): Whether prediction was successful
- **medicinal_uses** (array): List of medicinal uses
- **all_predictions** (object): Probabilities for all plant classes
- **image_path** (string): Path to uploaded image on server
- **message** (string): Status message

### Model Info Fields
- **model_type** (string): Type of model used
- **architecture** (string): Model architecture details
- **training_samples** (integer): Number of training samples
- **validation_samples** (integer): Number of validation samples
- **test_samples** (integer): Number of test samples
- **number_of_classes** (integer): Number of plant classes
- **classes** (array): List of plant class names
- **test_accuracy** (float): Accuracy on test set
- **test_loss** (float): Loss on test set

---

## Supported Formats

### Image Formats
- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)

### Maximum File Size
- 16 MB

---

## Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 400 | Bad Request | Invalid request or missing parameters |
| 404 | Not Found | Resource not found |
| 500 | Server Error | Internal server error |

---

## Rate Limiting & Quotas

Currently not implemented. Future versions may include:
- Rate limiting per IP
- Request quotas
- Authentication tokens

---

## Versioning

**Current Version:** 1.0  
**Release Date:** January 2026

---

## Support & Issues

For issues or questions:
1. Check the SETUP_GUIDE.md for troubleshooting
2. Verify all dependencies are installed
3. Ensure the model files are present in `models/` directory
4. Check Flask application logs for errors

---

## Changelog

### Version 1.0 (Current)
- Initial release
- Image upload and plant identification
- Confidence scoring
- Medicinal use information
- All predictions display

---

## Best Practices

1. **Image Quality**: Use clear, well-lit images of leaves
2. **Image Angle**: Take photos from multiple angles for best results
3. **Background**: Simple backgrounds work better
4. **File Size**: Smaller files process faster
5. **Error Handling**: Always check `success` field in response

---

## Future Enhancements

- [ ] Batch image processing
- [ ] Image preprocessing options
- [ ] Advanced filtering
- [ ] Historical prediction storage
- [ ] User authentication
- [ ] API key management
- [ ] Webhook support
- [ ] GraphQL endpoint

---

**API Documentation Version 1.0**  
**Last Updated: January 2026**
