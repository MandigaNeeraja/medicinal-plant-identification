"""
Configuration and constants for the Medicinal Plant Identification project
"""
import os

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

# Plant classes - auto-detected from the `dataset/` folder (fallback to defaults)
_default_plant_classes = {
    'Aloevera': {
        'medicinal_uses': ['Skin burns and wounds', 'Digestive health', 'Anti-inflammatory'],
        'image': 'aloevera.jpg'
    },
    'Amla': {
        'medicinal_uses': ['Rich in Vitamin C', 'Antioxidant', 'Immunity booster'],
        'image': 'amla.jpg'
    },
    'Amruthaballi': {
        'medicinal_uses': ['Immune modulation', 'Antipyretic', 'Liver tonic'],
        'image': 'amruthaballi.jpg'
    },
    'Badipala': {
        'medicinal_uses': ['Traditional remedy', 'Digestive aid'],
        'image': 'badipala.jpg'
    },
    'Balloon_Vine': {
        'medicinal_uses': ['Anti-inflammatory', 'Respiratory support'],
        'image': 'balloon_vine.jpg'
    },
    'Bhrami': {
        'medicinal_uses': ['Memory enhancement', 'Cognitive improvement', 'Anxiety relief'],
        'image': 'bhrami.jpg'
    },
    'camphor': {
        'medicinal_uses': ['Topical analgesic', 'Antiseptic', 'Decongestant'],
        'image': 'camphor.jpg'
    },
    'Catharanthus': {
        'medicinal_uses': ['Medicinal alkaloids', 'Traditional uses'],
        'image': 'catharanthus.jpg'
    },
    'Coffee': {
        'medicinal_uses': ['Stimulant', 'Antioxidant'],
        'image': 'coffee.jpg'
    },
    'Curry': {
        'medicinal_uses': ['Antimicrobial', 'Digestive aid'],
        'image': 'curry.jpg'
    },
    'Doddpathre': {
        'medicinal_uses': ['Topical antiseptic', 'Skin care'],
        'image': 'doddpathre.jpg'
    },
    'Drumstick': {
        'medicinal_uses': ['Nutritional', 'Anti-inflammatory', 'Antioxidant'],
        'image': 'drumstick.jpg'
    },
    'Eucalyptus': {
        'medicinal_uses': ['Respiratory decongestant', 'Antiseptic'],
        'image': 'eucalyptus.jpg'
    },
    'Ginger': {
        'medicinal_uses': ['Digestive aid', 'Anti-inflammatory', 'Nausea relief'],
        'image': 'ginger.jpg'
    },
    'Henna': {
        'medicinal_uses': ['Skin conditioning', 'Antifungal properties'],
        'image': 'henna.jpg'
    },
    'Mint': {
        'medicinal_uses': ['Digestive aid', 'Cooling', 'Respiratory relief'],
        'image': 'mint.jpg'
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

PLANT_CLASSES = {}
if os.path.isdir(DATASET_PATH):
    for plant in sorted([d for d in os.listdir(DATASET_PATH) if os.path.isdir(os.path.join(DATASET_PATH, d))]):
        PLANT_CLASSES[plant] = {
            'medicinal_uses': _default_plant_classes.get(plant, {}).get('medicinal_uses', ['Information not available yet']),
            'image': _default_plant_classes.get(plant, {}).get('image', f"{plant.lower()}.jpg")
        }
else:
    PLANT_CLASSES = _default_plant_classes

# Model confidence threshold
CONFIDENCE_THRESHOLD = 0.7

# Upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
