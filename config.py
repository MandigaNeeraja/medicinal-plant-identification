"""
Configuration and constants for the Medicinal Plant Identification project
"""

# Dataset configuration
DATASET_PATH = 'dataset'
TRAIN_SPLIT = 0.7
VAL_SPLIT = 0.15
TEST_SPLIT = 0.15

# Image configuration
IMG_HEIGHT = 224
IMG_WIDTH = 224
IMG_CHANNELS = 3
BATCH_SIZE = 32

# Model configuration
EPOCHS = 50
LEARNING_RATE = 0.001
PATIENCE = 10  # For early stopping

# Plant classes
PLANT_CLASSES = {
    'Aloevera': {
        'medicinal_uses': ['Skin burns and wounds', 'Digestive health', 'Anti-inflammatory'],
        'image': 'aloevera.jpg'
    },
    'Bhrami': {
        'medicinal_uses': ['Memory enhancement', 'Cognitive improvement', 'Anxiety relief'],
        'image': 'bhrami.jpg'
    },
    'Neem': {
        'medicinal_uses': ['Skin health', 'Antibacterial properties', 'Immune boost'],
        'image': 'neem.jpg'
    },
    'Tulsi': {
        'medicinal_uses': ['Cough and cold relief', 'Respiratory health', 'Stress reduction'],
        'image': 'tulsi.jpg'
    },
    'Turmeric': {
        'medicinal_uses': ['Anti-inflammatory', 'Antioxidant', 'Joint health'],
        'image': 'turmeric.jpg'
    }
}

# Model confidence threshold
CONFIDENCE_THRESHOLD = 0.7

# Upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
