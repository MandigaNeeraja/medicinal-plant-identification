# 🧪 Testing Guide - Complete System Validation

## Quick Test Checklist

Use this checklist to verify every part of your project works correctly.

---

## ✅ Step 1: Setup & Dependencies (5 minutes)

- [ ] Open PowerShell/Command Prompt
- [ ] Navigate to project: `cd "c:\Final Year Project\MedicinalPlantIdentification"`
- [ ] Create virtual environment: `python -m venv env`
- [ ] Activate environment: `env\Scripts\activate`
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Verify installation:
  ```bash
  python -c "import tensorflow; print('TensorFlow OK')"
  python -c "import cv2; print('OpenCV OK')"
  python -c "import flask; print('Flask OK')"
  ```

---

## ✅ Step 2: Model Files Verification

- [ ] Model file exists: `models/best_model.h5` 
- [ ] Label encoder exists: `models/label_encoder.pkl`
- [ ] Preprocessing params exist: `models/preprocessing_params.pkl`
- [ ] Model info exists: `models/model_info.pkl`

Check by running:
```bash
ls models/
```

Expected output:
```
best_model.h5
label_encoder.pkl
preprocessing_params.pkl
model_info.pkl
```

---

## ✅ Step 3: Backend Flask Application Test

### 3.1 Start the Flask App

```bash
cd webapp
python app.py
```

**Expected output:**
```
Upload folder configured at: [...]/uploads
✓ Model loaded successfully from [...]/models!
Starting Medicinal Plant Identification Web Application...
Open browser and navigate to http://localhost:5000
 * Running on http://0.0.0.0:5000
```

- [ ] No errors in startup
- [ ] Model loads successfully
- [ ] Flask server starts on port 5000
- [ ] Output shows upload folder path

### 3.2 Verify Routes

Open a new terminal (keep Flask running):

```bash
# Test home route
curl http://localhost:5000/

# Test API routes
curl http://localhost:5000/api/model-info

# Test plant info
curl http://localhost:5000/info/Neem
```

- [ ] Home page loads (should return HTML)
- [ ] API endpoints respond with JSON
- [ ] Plant info returns medicinal uses

---

## ✅ Step 4: Frontend Testing

### 4.1 Open Web Interface

- [ ] Open browser to **http://localhost:5000**
- [ ] Page loads with no errors
- [ ] See "Medicinal Plant Identifier" header
- [ ] Upload section visible with file input
- [ ] "Supported Plant Species" section visible at bottom

### 4.2 Test UI Elements

- [ ] Click on file input → file picker opens
- [ ] Upload button appears
- [ ] Plant species cards display (Aloevera, Bhrami, Neem, Tulsi, Turmeric)
- [ ] Responsive design works on different screen sizes

---

## ✅ Step 5: Image Upload & Prediction Testing

### 5.1 Test with Sample Images

**Option A: Use Dataset Images**

Pick an image from the dataset:
```
dataset/Neem/[any_image].jpg
```

**Option B: Use from Models (Sample Images)**
- Check `models/sample_images.png` for reference

### 5.2 Upload Test Procedure

1. **Click upload area** or **drag-and-drop** an image
2. **Verify preview appears**:
   - [ ] Selected image shows in preview section
   - [ ] "Identify Plant" button visible
   - [ ] Can change image with "Choose Another Image"

3. **Click "Identify Plant"** button
4. **Wait for prediction**:
   - [ ] Loading spinner appears
   - [ ] After 5-10 seconds, results should appear
   - [ ] **NO errors in browser console**

### 5.3 Verify Results Display

After prediction, check:

- [ ] **Predicted plant name** displays (e.g., "Neem")
- [ ] **Confidence score** shows as percentage (e.g., 95.3%)
- [ ] **Confidence bar** fills proportionally
- [ ] **Medicinal uses** list displays:
  - [ ] Uses are relevant to the plant
  - [ ] Multiple uses shown
  - [ ] Formatted correctly with checkmarks

- [ ] **All Plant Predictions** section shows:
  - [ ] All 5 plants listed
  - [ ] Scores in descending order
  - [ ] Prediction bars visible
  - [ ] Percentages correct

### 5.4 Test Multiple Predictions

- [ ] Upload different plant images
- [ ] Verify different predictions
- [ ] Check accuracy on known plants
- [ ] Test edge cases:
  - [ ] Blurry images
  - [ ] Rotated images
  - [ ] Different lighting

---

## ✅ Step 6: Error Handling Tests

### 6.1 Test Invalid Files

- [ ] Upload non-image file (.txt, .pdf)
  - Expected: Error message about invalid file type
- [ ] Upload without selecting file
  - Expected: Error message about no file selected
- [ ] Upload very large file (>16MB)
  - Expected: Error message about file size

### 6.2 Test Network/Recovery

- [ ] Disconnect/reconnect network during upload
  - Expected: Appropriate error message
- [ ] Fix error and retry
  - Expected: Works after retry

### 6.3 Test Form Reset

- [ ] After prediction, click "Identify Another Plant"
- [ ] Form clears completely
- [ ] Can upload new image
- [ ] Previous results gone

---

## ✅ Step 7: Backend Debugging (Optional)

When Flask is running, check the terminal for:

```
======================================================================
PREDICTION REQUEST RECEIVED
======================================================================
Request method: POST
Request files: dict_keys(['file'])
Request content type: multipart/form-data
File received: [filename]
✓ File saved successfully
✓ File size: [size] bytes
Making prediction...
✓ Prediction result: [plant] ([confidence])
✓ Plant info added
✓ Image path: /uploads/[filename]
✓ Prediction completed successfully!
======================================================================
```

- [ ] All ✓ symbols present
- [ ] No ❌ errors
- [ ] File size reasonable (>10KB)

---

## ✅ Step 8: Browser Console Check

Open browser Developer Tools (F12):

1. **Console Tab**:
   - [ ] No red error messages
   - [ ] "Form submitted!" logs visible when uploading
   - [ ] "Response data:" logs show prediction results
   - [ ] No 404 errors for resources

2. **Network Tab**:
   - [ ] POST request to `/predict` returns 200 status
   - [ ] Response contains `"success": true`
   - [ ] No failed requests

3. **Application Tab**:
   - [ ] Local storage working (if used)
   - [ ] Session storage OK

---

## ✅ Step 9: Performance Tests (Optional)

Time these operations:

- [ ] **Model loading**: Should be < 5 seconds
- [ ] **Image upload**: Should be < 2 seconds
- [ ] **Prediction**: Should be < 10 seconds
- [ ] **Results display**: Should be instant

---

## ✅ Step 10: Complete Workflow Test

**Final integration test** - do this end-to-end:

1. Start fresh
2. Navigate to http://localhost:5000
3. Upload image from `dataset/`
4. Click predict
5. See results
6. Click "Identify Another"
7. Upload different plant
8. Verify different prediction
9. Close and reopen browser
10. Repeat test

All steps should work without any issues.

---

## 📋 Test Results Summary

Create a test results file showing:

### Test Case Results

| Test Case | Status | Notes |
|-----------|--------|-------|
| App Startup | ✅ | Model loaded, server running |
| Home Page | ✅ | Page loads, all elements visible |
| File Upload | ✅ | Image preview shows |
| Prediction | ✅ | Plant identified correctly |
| Results Display | ✅ | Confidence, uses, and predictions visible |
| Error Handling | ✅ | Invalid files rejected |
| Form Reset | ✅ | Can upload multiple times |
| Browser Console | ✅ | No errors or warnings |

---

## 🔧 Common Issues & Solutions

### Issue: "Model not loaded" Error

**Solution:**
```bash
# Verify model files exist
ls models/

# Check paths in app.py are correct
# Should use relative paths like:
os.path.join(os.path.dirname(__file__), '..', 'models')
```

### Issue: "Port 5000 already in use"

**Solution:**
```bash
# Kill the process using port 5000
netstat -ano | findstr :5000
taskkill /PID [PID] /F

# Or change port in app.py
app.run(port=5001)
```

### Issue: File Upload Fails / 400 Error

**Solution:**
```bash
# Check upload folder exists
ls uploads/

# Check file permissions
# Check file size < 16MB
# Check file format is image
```

### Issue: Prediction Shows "Confidence Below Threshold"

**Solution:**
```bash
# This is normal - the image might not look like the trained plants
# Try with clearer leaf images from the dataset
# Check CONFIDENCE_THRESHOLD in config.py (default 0.7 = 70%)
```

### Issue: JavaScript Console Shows "fetch failed"

**Solution:**
```bash
# Check Flask server is running
# Check URL: http://localhost:5000 (not localhost:5000/)
# Check CORS if needed (check app.py has proper headers)
# Check file upload endpoint: /predict
```

---

## 📊 Expected Predictions

Test with images from dataset and verify reasonable predictions:

| Plant | Expected Confidence | Medicinal Uses Count |
|-------|-------------------|----------------------|
| Aloevera | 70-95% | 3+ uses listed |
| Bhrami | 70-95% | 3+ uses listed |
| Neem | 70-95% | 3+ uses listed |
| Tulsi | 70-95% | 3+ uses listed |
| Turmeric | 70-95% | 3+ uses listed |

---

## ✨ Testing Complete!

If all checkboxes are ✅, your project is:
- ✅ Fully functional
- ✅ No errors
- ✅ Ready for evaluation
- ✅ All features working

Congratulations! Your Medicinal Plant Identification system is complete and tested!

