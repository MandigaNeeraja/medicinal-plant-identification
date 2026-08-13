# 🚀 GETTING STARTED - Quick Reference

## ⚡ 5-Minute Quick Start

### Prerequisites
- Python 3.8+ installed
- Virtual environment set up
- Dependencies installed

### Step 1: Start the Application
```powershell
cd "c:\Final Year Project\MedicinalPlantIdentification"
env\Scripts\activate
cd webapp
python app.py
```

**Expected Output:**
```
Upload folder configured at: ...
✓ Model loaded successfully from .../models!
Starting Medicinal Plant Identification Web Application...
Open browser and navigate to http://localhost:5000
 * Running on http://0.0.0.0:5000
```

### Step 2: Open in Browser
Open **http://localhost:5000**

You should see:
- 🌿 Header "Medicinal Plant Identifier"
- 📷 Upload area with dashed border
- 🌱 Plant species cards at bottom

### Step 3: Upload Image & Predict

1. **Click upload area** or **drag-drop image**
   - Use images from `dataset/` folder
   - JPG, PNG, GIF, BMP, WebP formats supported

2. **See image preview** automatically

3. **Click "Identify Plant"** button

4. **Wait for results** (loading spinner shows)

5. **See results:**
   - ✅ Plant name
   - ✅ Confidence percentage
   - ✅ Medicinal uses
   - ✅ All predictions

### Step 4: Try Again

Click **"Identify Another Plant"** to reset and upload another image.

---

## 📁 Key Folders

| Folder | Purpose | Contains |
|--------|---------|----------|
| `dataset/` | Training images | 1000+ leaf photos |
| `models/` | Trained model | best_model.h5 + encoders |
| `webapp/` | Web app code | Flask app + templates |
| `webapp/uploads/` | User uploads | Prediction images |
| `src/` | Model logic | predictor.py |

---

## 🎯 Test Images

Use images from these folders for testing:

```
c:\Final Year Project\MedicinalPlantIdentification\dataset\

├── Aloevera/        ← Aloe Vera leaves
├── Bhrami/          ← Brahmi/Bacopa plant
├── Neem/            ← Neem tree leaves
├── Tulsi/           ← Holy Basil leaves
└── Turmeric/        ← Turmeric plant leaves
```

**Tip:** Pick any clear leaf image for best predictions!

---

## 🔧 Troubleshooting

### Problem: "Module not found"
```bash
pip install -r requirements.txt
```

### Problem: "Port 5000 already in use"
```bash
# Kill process or use different port
# Edit webapp/app.py: app.run(port=5001)
```

### Problem: "Model not loaded"
```bash
# Verify model files exist
ls models/
# Should show: best_model.h5, label_encoder.pkl, preprocessing_params.pkl
```

### Problem: "No results showing"
```bash
# Check browser console (F12) for errors
# Check Flask console for error messages
# Try with clear leaf image
```

---

## 📊 Expected Results

When you upload a plant leaf image:

```json
{
  "success": true,
  "plant": "Neem",
  "confidence": 0.95,
  "medicinal_uses": [
    "Skin health",
    "Antibacterial properties",
    "Immune boost"
  ],
  "all_predictions": {
    "Neem": 0.95,
    "Tulsi": 0.03,
    "Aloevera": 0.01,
    "Bhrami": 0.01,
    "Turmeric": 0.00
  }
}
```

---

## 📚 Full Documentation

For detailed information, read:

| Document | Content |
|----------|---------|
| **README.md** | Project overview |
| **QUICK_START.md** | Setup instructions |
| **TESTING_GUIDE.md** | Testing checklist |
| **PROJECT_ARCHITECTURE.md** | Technical details |
| **FIXES_APPLIED.md** | What was fixed |
| **SETUP_GUIDE.md** | Detailed setup |
| **docs/API_DOCUMENTATION.md** | API reference |

---

## ✨ Features

✅ Upload leaf images (drag-drop or click)  
✅ See image preview before predicting  
✅ Get instant plant identification  
✅ View confidence score with visual bar  
✅ Read medicinal uses  
✅ Compare all plant predictions  
✅ Beautiful responsive design  
✅ Works on any device  

---

## 🎓 Project Info

**Course:** BTech CSE - AIML  
**Project:** Medicinal Plant Identification  
**Status:** ✅ Complete & Tested  
**Date:** January 2026  

**Technology:**
- Python 3.8+
- Flask 3.0+
- TensorFlow 2.14+
- OpenCV 4.8+
- HTML5 / CSS3 / JavaScript

**Model:**
- MobileNetV2 (Transfer Learning)
- Trained on 1000+ leaf images
- 5 plant species
- ~90% accuracy

---

## 🚀 Summary

1. **Start:** Run `python app.py` in webapp folder
2. **Open:** Go to http://localhost:5000
3. **Upload:** Select a leaf image
4. **Predict:** Click "Identify Plant"
5. **Enjoy:** See results!

**That's it! Your system is ready to use.** 🎉

---

## 💡 Tips

- Use clear, well-lit leaf images for best results
- Test with different plants from `dataset/` folder
- Confidence score > 70% means high confidence
- Check browser console (F12) if issues occur
- Keep Flask terminal window visible to see logs

---

## 📞 Need Help?

1. **Check TESTING_GUIDE.md** for detailed testing
2. **Check FIXES_APPLIED.md** for what was fixed
3. **Check PROJECT_ARCHITECTURE.md** for how it works
4. **Check Flask console output** for error messages
5. **Check browser console (F12)** for JavaScript errors

---

**Happy Plant Identification! 🌿**

