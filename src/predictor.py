"""
Prediction utilities for the Medicinal Plant Identification model
"""

import pickle
import os


class PlantPredictor:
    """
    Class to handle plant identification predictions
    """

    def __init__(self, model_path, label_encoder_path, preprocessing_params_path):
        import cv2  # noqa: F401 - loaded lazily for faster app startup
        from tensorflow import keras

        self._cv2 = cv2
        self.model = keras.models.load_model(model_path)
        self.label_encoder = pickle.load(open(label_encoder_path, 'rb'))
        self.preprocessing_params = pickle.load(open(preprocessing_params_path, 'rb'))
        
        self.IMG_HEIGHT = self.preprocessing_params['IMG_HEIGHT']
        self.IMG_WIDTH = self.preprocessing_params['IMG_WIDTH']
        self.NORMALIZATION = self.preprocessing_params['NORMALIZATION']
    
    def preprocess_image(self, image_path):
        import numpy as np

        cv2 = self._cv2
        # Read image
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Could not read image from {image_path}")
        
        # Resize to standard dimensions
        img = cv2.resize(img, (self.IMG_WIDTH, self.IMG_HEIGHT))
        
        # Convert BGR to RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Normalize pixel values
        img = img.astype('float32') / self.NORMALIZATION
        
        # Add batch dimension
        img = np.expand_dims(img, axis=0)
        
        return img
    
    def predict(self, image_path, confidence_threshold=0.7, non_leaf_threshold=0.3):
        import numpy as np

        try:
            # Preprocess image
            preprocessed_img = self.preprocess_image(image_path)
            
            # Make prediction
            predictions = self.model.predict(preprocessed_img, verbose=0)
            confidence_scores = predictions[0]
            
            # Get predicted class
            predicted_class_idx = np.argmax(confidence_scores)
            predicted_class = self.label_encoder.classes_[predicted_class_idx]
            confidence = float(confidence_scores[predicted_class_idx])
            
            # Determine prediction status
            if confidence >= confidence_threshold:
                status = 'success'
                success = True
                message = 'Prediction successful'
            elif confidence >= non_leaf_threshold:
                status = 'low_confidence'
                success = False
                message = 'Please upload valid leaf image.'
            else:
                status = 'non_leaf'
                success = False
                message = 'Please upload valid leaf image.'

            # Create all predictions dictionary
            all_predictions = {
                self.label_encoder.classes_[i]: float(confidence_scores[i])
                for i in range(len(self.label_encoder.classes_))
            }

            return {
                'plant': predicted_class if success else None,
                'confidence': confidence,
                'all_predictions': all_predictions,
                'success': success,
                'status': status,
                'message': message
            }
        
        except Exception as e:
            return {
                'plant': None,
                'confidence': 0.0,
                'all_predictions': {},
                'success': False,
                'status': 'error',
                'message': f'Error during prediction: {str(e)}'
            }


def load_model_artifacts(model_dir='../models'):
    """
    Load all model artifacts
    
    Args:
        model_dir: Directory containing model files
        
    Returns:
        Tuple of (model, label_encoder, preprocessing_params, model_info)
    """
    try:
        from tensorflow import keras

        model = keras.models.load_model(os.path.join(model_dir, 'best_model.h5'))
        label_encoder = pickle.load(open(os.path.join(model_dir, 'label_encoder.pkl'), 'rb'))
        preprocessing_params = pickle.load(open(os.path.join(model_dir, 'preprocessing_params.pkl'), 'rb'))
        model_info = pickle.load(open(os.path.join(model_dir, 'model_info.pkl'), 'rb'))
        
        return model, label_encoder, preprocessing_params, model_info
    except Exception as e:
        print(f"Error loading model artifacts: {e}")
        return None, None, None, None
