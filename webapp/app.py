"""
Flask Web Application for Medicinal Plant Identification
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import sys
from werkzeug.utils import secure_filename
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.predictor import PlantPredictor
from config import PLANT_CLASSES, UPLOAD_FOLDER, ALLOWED_EXTENSIONS, IMG_HEIGHT, IMG_WIDTH, CONFIDENCE_THRESHOLD

# Initialize Flask app
app = Flask(__name__)

# Set absolute path for upload folder
UPLOAD_FOLDER_PATH = os.path.join(os.path.dirname(__file__), '..', UPLOAD_FOLDER)
UPLOAD_FOLDER_PATH = os.path.abspath(UPLOAD_FOLDER_PATH)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER_PATH
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload folder if not exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
print(f"Upload folder configured at: {app.config['UPLOAD_FOLDER']}")

# Initialize predictor
try:
    # Use relative paths from webapp directory
    model_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
    model_dir = os.path.abspath(model_dir)
    
    predictor = PlantPredictor(
        model_path=os.path.join(model_dir, 'best_model.h5'),
        label_encoder_path=os.path.join(model_dir, 'label_encoder.pkl'),
        preprocessing_params_path=os.path.join(model_dir, 'preprocessing_params.pkl')
    )
    print(f"✓ Model loaded successfully from {model_dir}!")
except Exception as e:
    print(f"Error loading model: {e}")
    import traceback
    traceback.print_exc()
    predictor = None


def allowed_file(filename):
    """Check if file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html', plants=list(PLANT_CLASSES.keys()))


@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')


@app.route('/info/<plant_name>')
def plant_info(plant_name):
    """Get plant information"""
    if plant_name in PLANT_CLASSES:
        return jsonify(PLANT_CLASSES[plant_name])
    return jsonify({'error': 'Plant not found'}), 404


@app.route('/plant/<plant_name>')
def plant_page(plant_name):
    """Render plant detail page"""
    if plant_name not in PLANT_CLASSES:
        return render_template('404.html'), 404

    plant_data = PLANT_CLASSES[plant_name]

    # Provide safe defaults for expected fields
    context = {
        'plant_name': plant_name,
        'scientific_name': plant_data.get('scientific_name', ''),
        'common_names': plant_data.get('common_names', []),
        'overview': plant_data.get('overview', 'Information not available.'),
        'medicinal_uses': plant_data.get('medicinal_uses', ['Information not available.']),
        'preparation': plant_data.get('preparation', {
            'juice': 'Information not available.',
            'powder': 'Information not available.',
            'decoction': 'Information not available.'
        }),
        'dosage': plant_data.get('dosage', 'Information not available.'),
        'safety': plant_data.get('safety', 'Information not available.'),
        'best_time': plant_data.get('best_time', 'Information not available.'),
        'did_you_know': plant_data.get('did_you_know', "Interesting facts will appear here.")
    }

    return render_template('plant_detail.html', **context)


@app.route('/predict', methods=['POST'])
def predict():
    """Handle image upload and prediction"""
    
    print("\n" + "="*70)
    print("PREDICTION REQUEST RECEIVED")
    print("="*70)
    
    if predictor is None:
        error_msg = 'Model not loaded. Please restart the application.'
        print(f"❌ Error: {error_msg}")
        return jsonify({'success': False, 'error': error_msg}), 500
    
    # Debug: Print request info
    print(f"Request method: {request.method}")
    print(f"Request files: {request.files.keys()}")
    print(f"Request content type: {request.content_type}")
    
    # Check if file is present
    if 'file' not in request.files:
        error_msg = 'No file provided in request'
        print(f"❌ Error: {error_msg}")
        print(f"Available keys: {list(request.files.keys())}")
        return jsonify({'success': False, 'error': error_msg}), 400
    
    file = request.files['file']
    
    print(f"File received: {file.filename}")
    
    if file.filename == '':
        error_msg = 'No file selected'
        print(f"❌ Error: {error_msg}")
        return jsonify({'success': False, 'error': error_msg}), 400
    
    if not allowed_file(file.filename):
        error_msg = f'File type not allowed. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}'
        print(f"❌ Error: {error_msg}")
        return jsonify({'success': False, 'error': error_msg}), 400
    
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print(f"Saving file to: {filepath}")
        file.save(filepath)
        print(f"✓ File saved successfully")
        
        # Verify file exists
        if not os.path.exists(filepath):
            raise Exception(f"File was not saved properly to {filepath}")
        
        file_size = os.path.getsize(filepath)
        print(f"✓ File size: {file_size} bytes")
        
        # Make prediction
        print("Making prediction...")
        result = predictor.predict(filepath, confidence_threshold=CONFIDENCE_THRESHOLD)
        print(f"✓ Prediction result: {result['plant']} ({result['confidence']:.2%})")
        
        # Get plant information if prediction is successful
        if result['success'] and result['plant'] in PLANT_CLASSES:
            plant_info_data = PLANT_CLASSES[result['plant']]
            result['medicinal_uses'] = plant_info_data['medicinal_uses']
            print(f"✓ Plant info added")
        
        # Add file path for display
        result['image_path'] = f'/uploads/{filename}'
        print(f"✓ Image path: {result['image_path']}")
        
        print("✓ Prediction completed successfully!")
        print("="*70)
        return jsonify(result)
    
    except Exception as e:
        error_msg = f'Error during prediction: {str(e)}'
        print(f"❌ Exception: {error_msg}")
        import traceback
        traceback.print_exc()
        print("="*70)
        return jsonify({'success': False, 'error': error_msg}), 500


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    print(f"Serving file: {filename} from {app.config['UPLOAD_FOLDER']}")
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        print(f"Error serving file: {e}")
        return jsonify({'error': str(e)}), 404


@app.route('/api/model-info')
def model_info():
    """Get model information"""
    try:
        import pickle
        model_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
        model_dir = os.path.abspath(model_dir)
        info_path = os.path.join(model_dir, 'model_info.pkl')
        info = pickle.load(open(info_path, 'rb'))
        return jsonify(info)
    except Exception as e:
        print(f"Error loading model info: {e}")
        return jsonify({'error': f'Could not load model info: {str(e)}'}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('500.html'), 500


if __name__ == '__main__':
    print("Starting Medicinal Plant Identification Web Application...")
    print("Open browser and navigate to http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
