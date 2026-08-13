# ⚡ Quick Start Guide (5 Minutes)

## For Busy Evaluators - Start Here!

### The Absolute Fastest Way to See the Project

## Step 1: Install Dependencies (2 minutes)
```bash
cd "c:\Final Year Project\MedicinalPlantIdentification"
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
```

## Step 2: Train Model (20-30 minutes)
```bash
jupyter notebook
```
- Open: `notebooks/01_data_exploration.ipynb`
- Press `Ctrl+Shift+Enter` (or use Run menu to "Run All Cells")
- Models will be saved to `models/` directory
- You'll see:
  - 📊 Data visualization
  - 🤖 Model architecture
  - 📈 Training progress
  - 🎯 Evaluation metrics

## Step 3: Run Web App (1 minute)
```bash
cd webapp
python app.py
```
- Open browser: **http://localhost:5000**
- Upload a leaf image
- See instant predictions!

---

## 📁 Where to Find Everything

| What | Location | Purpose |
|------|----------|---------|
| **Dataset** | `dataset/` | Plant leaf images |
| **Model Training** | `notebooks/01_data_exploration.ipynb` | ML pipeline |
| **Web App** | `webapp/app.py` | Flask application |
| **Main Docs** | `README.md` | Project overview |
| **Setup Help** | `SETUP_GUIDE.md` | Detailed instructions |
| **API Ref** | `docs/API_DOCUMENTATION.md` | API endpoints |

---

## 🎯 What You'll See

### After Training (Jupyter)
✅ Class distribution plot  
✅ Sample leaf images  
✅ Model accuracy curve  
✅ Confusion matrix  
✅ Classification metrics  

### After Running Web App
✅ Beautiful UI at http://localhost:5000  
✅ Drag-and-drop upload  
✅ Instant plant identification  
✅ Confidence score  
✅ Medicinal uses listed  

---

## 🔧 Troubleshooting

**Q: "Module not found"**  
A: Run `pip install -r requirements.txt` again

**Q: "Port 5000 in use"**  
A: Change port in `webapp/app.py` line: `app.run(port=5001)`

**Q: "Model not found"**  
A: You need to train first (Step 2)

**Q: "GPU errors"**  
A: Just use CPU - it works fine

---

## 📊 Expected Timeline

| Task | Time |
|------|------|
| Setup | 5 min |
| Training | 20-30 min |
| Web App Test | 5 min |
| **Total** | **30-40 min** |

---

## ✨ Key Features to Try

1. **Drag-Drop Upload** - Drop image on upload box
2. **Multiple Formats** - Works with JPG, PNG, GIF
3. **Confidence Display** - See prediction confidence
4. **Medicinal Uses** - Learn about each plant
5. **All Predictions** - See scores for all plants

---

## 📞 Need More Help?

- **Setup Issues?** → Read `SETUP_GUIDE.md`
- **API Questions?** → Check `docs/API_DOCUMENTATION.md`
- **Want Details?** → See `README.md`
- **Project Timeline?** → Check `PROJECT_GUIDE.md`

---

## 🚀 Commands Cheat Sheet

```bash
# Activate environment
env\Scripts\activate

# Install packages
pip install -r requirements.txt

# Start Jupyter
jupyter notebook

# Run web app
cd webapp && python app.py

# Deactivate environment
deactivate
```

---

## ✅ Verification Checklist

After running the project:

- [ ] Jupyter notebook runs without errors
- [ ] Model training shows decreasing loss
- [ ] Flask app starts successfully
- [ ] Web interface loads at localhost:5000
- [ ] Can upload and predict plants
- [ ] Confidence scores display correctly
- [ ] Medicinal uses are listed

---

## 🎓 What This Project Demonstrates

✨ **Machine Learning** - CNN with transfer learning  
✨ **Web Development** - Flask + HTML/CSS/JavaScript  
✨ **API Design** - RESTful endpoints  
✨ **Best Practices** - Documentation, configuration, error handling  
✨ **Full Stack** - From ML model to deployed web app  

---

**That's it! You now know how to run the entire project. Happy evaluating! 🎉**

---

*For detailed information, see the main README.md file.*
