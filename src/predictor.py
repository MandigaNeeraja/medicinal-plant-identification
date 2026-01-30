"""
Prediction utilities for the Medicinal Plant Identification model
"""

import cv2
import numpy as np
import pickle
import os
from tensorflow import keras

class PlantPredictor:
    """
    Class to handle plant identification predictions
    """
    
    def __init__(self, model_path, label_encoder_path, preprocessing_params_path):
        """
        Initialize the predictor with model and preprocessing parameters
        
        Args:
            model_path: Path to the trained model (.h5 file)
            label_encoder_path: Path to the label encoder
            preprocessing_params_path: Path to preprocessing parameters
        """
        self.model = keras.models.load_model(model_path)
        self.label_encoder = pickle.load(open(label_encoder_path, 'rb'))
        self.preprocessing_params = pickle.load(open(preprocessing_params_path, 'rb'))
        
        self.IMG_HEIGHT = self.preprocessing_params['IMG_HEIGHT']
        self.IMG_WIDTH = self.preprocessing_params['IMG_WIDTH']
        self.NORMALIZATION = self.preprocessing_params['NORMALIZATION']
    
    def preprocess_image(self, image_path):
        """
        Preprocess an image for prediction
        
        Args:
            image_path: Path to the input image
            
        Returns:
            Preprocessed image array
        """
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
    
    def predict(self, image_path, confidence_threshold=0.7):
        """
        Predict plant class from an image
        
        Args:
            image_path: Path to the input image
            confidence_threshold: Minimum confidence for prediction
            
        Returns:
            Dictionary containing:
                - 'plant': Predicted plant name
                - 'confidence': Prediction confidence (0-1)
                - 'all_predictions': Probabilities for all classes
                - 'success': Boolean indicating if prediction is above threshold
        """
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
            
            # Check if confidence meets threshold
            success = confidence >= confidence_threshold
            
            # Create all predictions dictionary
            all_predictions = {
                self.label_encoder.classes_[i]: float(confidence_scores[i])
                for i in range(len(self.label_encoder.classes_))
            }
            
            return {
                'plant': predicted_class,
                'confidence': confidence,
                'all_predictions': all_predictions,
                'success': success,
                'message': 'Prediction successful' if success else f'Confidence ({confidence:.2%}) below threshold ({confidence_threshold:.0%})'
            }
        
        except Exception as e:
            return {
                'plant': None,
                'confidence': 0.0,
                'all_predictions': {},
                'success': False,
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
        model = keras.models.load_model(os.path.join(model_dir, 'best_model.h5'))
        label_encoder = pickle.load(open(os.path.join(model_dir, 'label_encoder.pkl'), 'rb'))
        preprocessing_params = pickle.load(open(os.path.join(model_dir, 'preprocessing_params.pkl'), 'rb'))
        model_info = pickle.load(open(os.path.join(model_dir, 'model_info.pkl'), 'rb'))
        
        return model, label_encoder, preprocessing_params, model_info
    except Exception as e:
        print(f"Error loading model artifacts: {e}")
        return None, None, None, None
