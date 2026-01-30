"""
Medicinal Plant Identification - CNN Model Training Script
Project: Identifying medicinal uses of plants using leaf images
Approach: CNN-based Image Classification with Web Interface
Author: BTech CSE-AIML Student
Date: January 2026
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import cv2
import pickle
import warnings
from pathlib import Path

warnings.filterwarnings('ignore')

# Deep Learning
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2

# ML utilities
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.metrics import precision_score, recall_score, f1_score
from sklearn.preprocessing import LabelEncoder

# Set random seeds for reproducibility
np.random.seed(42)
tf.random.set_seed(42)

# ============================================================================
# PHASE 1: CONFIGURATION & SETUP
# ============================================================================
print("=" * 70)
print("MEDICINAL PLANT IDENTIFICATION - MODEL TRAINING")
print("=" * 70)

# Define constants
DATASET_PATH = 'dataset'
MODELS_PATH = 'models'
IMG_HEIGHT = 224
IMG_WIDTH = 224
EPOCHS = 50
BATCH_SIZE = 32

# Create models directory if it doesn't exist
os.makedirs(MODELS_PATH, exist_ok=True)

print("\n✓ Configuration loaded")
print(f"✓ TensorFlow version: {tf.__version__}")
print(f"✓ Keras version: {keras.__version__}")

# ============================================================================
# PHASE 2: LOAD AND EXPLORE THE DATASET
# ============================================================================
print("\n" + "=" * 70)
print("PHASE 2: LOADING AND EXPLORING DATASET")
print("=" * 70)

# Get list of plant classes
plant_classes = os.listdir(DATASET_PATH)
plant_classes = sorted([cls for cls in plant_classes if os.path.isdir(os.path.join(DATASET_PATH, cls))])

print("\n🌿 Plant Classes Found:")
for i, plant in enumerate(plant_classes, 1):
    print(f"  {i}. {plant}")

# Analyze dataset structure
dataset_info = []
for plant in plant_classes:
    plant_path = os.path.join(DATASET_PATH, plant)
    image_count = len([f for f in os.listdir(plant_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
    dataset_info.append({'Plant': plant, 'Images': image_count})

df_info = pd.DataFrame(dataset_info)
print("\n📊 Dataset Distribution:")
print(df_info.to_string(index=False))
print(f"\nTotal Images: {df_info['Images'].sum()}")
print(f"Average images per class: {df_info['Images'].mean():.1f}")

# Visualize class distribution
print("\n📈 Creating class distribution chart...")
fig, ax = plt.subplots(1, 1, figsize=(10, 5))
colors = plt.cm.Set3(np.linspace(0, 1, len(df_info)))
ax.bar(df_info['Plant'], df_info['Images'], color=colors, edgecolor='black', alpha=0.7)
ax.set_ylabel('Number of Images', fontsize=12, fontweight='bold')
ax.set_xlabel('Plant Class', fontsize=12, fontweight='bold')
ax.set_title('Dataset Distribution Across Plant Classes', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(MODELS_PATH, 'class_distribution.png'), dpi=100, bbox_inches='tight')
plt.close()
print("✓ Class distribution chart saved!")

# Display sample images
print("\n🖼️ Loading sample images from each class...")
fig, axes = plt.subplots(len(plant_classes), 5, figsize=(15, len(plant_classes)*3))

for idx, plant in enumerate(plant_classes):
    plant_path = os.path.join(DATASET_PATH, plant)
    images = [f for f in os.listdir(plant_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    # Take 5 random samples
    sample_images = np.random.choice(images, min(5, len(images)), replace=False)
    
    for j, img_name in enumerate(sample_images):
        img_path = os.path.join(plant_path, img_name)
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        ax = axes[idx][j] if len(plant_classes) > 1 else axes[j]
        ax.imshow(img)
        ax.set_title(f"{plant}")
        ax.axis('off')

plt.suptitle('Sample Leaf Images from Each Plant Class', fontsize=16, fontweight='bold', y=0.995)
plt.tight_layout()
plt.savefig(os.path.join(MODELS_PATH, 'sample_images.png'), dpi=100, bbox_inches='tight')
plt.close()
print("✓ Sample images saved!")

# Analyze image dimensions
print("\n📐 Analyzing image dimensions...")
image_dimensions = []
for plant in plant_classes:
    plant_path = os.path.join(DATASET_PATH, plant)
    images = [f for f in os.listdir(plant_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    for img_name in images[:10]:  # Sample 10 images per class
        img_path = os.path.join(plant_path, img_name)
        img = cv2.imread(img_path)
        if img is not None:
            h, w, c = img.shape
            image_dimensions.append({'Plant': plant, 'Height': h, 'Width': w, 'Channels': c})

df_dims = pd.DataFrame(image_dimensions)
print("\n📐 Image Dimensions Statistics:")
print(df_dims.groupby('Plant')[['Height', 'Width']].describe().round(2))

# ============================================================================
# PHASE 3: DATA PREPROCESSING AND PREPARATION
# ============================================================================
print("\n" + "=" * 70)
print("PHASE 3: DATA PREPROCESSING")
print("=" * 70)

# Load all images and labels
print("\n📂 Loading all images...")
images = []
labels = []
error_count = 0

for plant in plant_classes:
    plant_path = os.path.join(DATASET_PATH, plant)
    image_files = [f for f in os.listdir(plant_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    for img_name in image_files:
        img_path = os.path.join(plant_path, img_name)
        try:
            img = cv2.imread(img_path)
            if img is not None:
                # Resize to standard dimensions
                img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))
                # Convert BGR to RGB
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                images.append(img)
                labels.append(plant)
        except Exception as e:
            print(f"  ⚠️ Error loading {img_path}: {e}")
            error_count += 1

X = np.array(images)
y = np.array(labels)

print(f"\n✓ Loaded {len(X)} images")
print(f"✓ Image shape: {X.shape}")
print(f"✓ Labels shape: {y.shape}")
if error_count > 0:
    print(f"⚠️ {error_count} images failed to load")

# Normalize pixel values to [0, 1]
print("\n🔧 Normalizing pixel values...")
X = X.astype('float32') / 255.0

# Encode labels
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)
num_classes = len(label_encoder.classes_)

print(f"✓ Normalized pixel values to [0, 1]")
print(f"✓ Number of classes: {num_classes}")
print(f"\nClass mapping:")
for i, label in enumerate(label_encoder.classes_):
    print(f"  {label} -> {i}")

# Split data into train, validation, and test sets (70-15-15)
print("\n📊 Splitting data into train/val/test sets...")
# First split: 70% train, 30% temp (val+test)
X_train, X_temp, y_train, y_temp = train_test_split(
    X, y_encoded, test_size=0.3, random_state=42, stratify=y_encoded
)

# Second split: Split temp into 50% val, 50% test (which gives 15% val, 15% test overall)
X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp
)

print(f"\n✓ Data split completed!")
print(f"  Train: {X_train.shape[0]} samples ({X_train.shape[0]/len(X)*100:.1f}%)")
print(f"  Validation: {X_val.shape[0]} samples ({X_val.shape[0]/len(X)*100:.1f}%)")
print(f"  Test: {X_test.shape[0]} samples ({X_test.shape[0]/len(X)*100:.1f}%)")

# Apply data augmentation to training set
print("\n🎨 Setting up data augmentation...")
datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    zoom_range=0.2,
    shear_range=0.2,
    fill_mode='nearest'
)

# Fit augmentation on training data
datagen.fit(X_train)

print("✓ Data augmentation configured!")
print("  Augmentation techniques:")
print("    - Rotation: ±20°")
print("    - Width/Height shift: 20%")
print("    - Horizontal flip")
print("    - Zoom: 20%")
print("    - Shear: 20%")

# ============================================================================
# PHASE 4: BUILD CNN MODEL ARCHITECTURE
# ============================================================================
print("\n" + "=" * 70)
print("PHASE 4: BUILDING CNN MODEL")
print("=" * 70)

print("\n🧠 Loading pre-trained MobileNetV2 model...")
# Load pre-trained MobileNetV2 model
base_model = MobileNetV2(input_shape=(IMG_HEIGHT, IMG_WIDTH, 3), 
                          include_top=False, 
                          weights='imagenet')

# Freeze base model layers (transfer learning)
base_model.trainable = False

print(f"✓ MobileNetV2 loaded and base layers frozen!")
print(f"✓ Base model parameters: {base_model.count_params():,}")

# Build complete model
print("\n🏗️ Building model architecture...")
model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(256, activation='relu'),
    layers.BatchNormalization(),
    layers.Dropout(0.5),
    layers.Dense(128, activation='relu'),
    layers.BatchNormalization(),
    layers.Dropout(0.3),
    layers.Dense(num_classes, activation='softmax')
])

# Compile model
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

print("✓ Model compiled successfully!")
print("\n📋 Model Summary:")
model.summary()

# ============================================================================
# PHASE 5: TRAIN THE CNN MODEL
# ============================================================================
print("\n" + "=" * 70)
print("PHASE 5: TRAINING THE MODEL")
print("=" * 70)

# Define callbacks
early_stopping = keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=10,
    restore_best_weights=True,
    verbose=1
)

model_checkpoint = keras.callbacks.ModelCheckpoint(
    os.path.join(MODELS_PATH, 'best_model.h5'),
    monitor='val_accuracy',
    save_best_only=True,
    verbose=1
)

reduce_lr = keras.callbacks.ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.5,
    patience=5,
    min_lr=0.00001,
    verbose=1
)

print("\n✓ Callbacks configured!")
print("  - Early Stopping: patience=10")
print("  - Model Checkpoint: saves best model")
print("  - Reduce LR on Plateau: adaptive learning rate")

# Train the model
print(f"\n🚀 Starting training with {EPOCHS} epochs and batch size {BATCH_SIZE}...")
print("=" * 70)

history = model.fit(
    datagen.flow(X_train, y_train, batch_size=BATCH_SIZE),
    epochs=EPOCHS,
    steps_per_epoch=len(X_train) // BATCH_SIZE,
    validation_data=(X_val, y_val),
    callbacks=[early_stopping, model_checkpoint, reduce_lr],
    verbose=1
)

print("\n" + "=" * 70)
print("✓ Training completed!")
print("=" * 70)

# Plot training history
print("\n📊 Creating training curves...")
fig, axes = plt.subplots(1, 2, figsize=(14, 4))

# Accuracy plot
axes[0].plot(history.history['accuracy'], label='Train Accuracy', linewidth=2)
axes[0].plot(history.history['val_accuracy'], label='Validation Accuracy', linewidth=2)
axes[0].set_xlabel('Epoch', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Accuracy', fontsize=12, fontweight='bold')
axes[0].set_title('Model Accuracy', fontsize=14, fontweight='bold')
axes[0].legend()
axes[0].grid(alpha=0.3)

# Loss plot
axes[1].plot(history.history['loss'], label='Train Loss', linewidth=2)
axes[1].plot(history.history['val_loss'], label='Validation Loss', linewidth=2)
axes[1].set_xlabel('Epoch', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Loss', fontsize=12, fontweight='bold')
axes[1].set_title('Model Loss', fontsize=14, fontweight='bold')
axes[1].legend()
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(MODELS_PATH, 'training_curves.png'), dpi=100, bbox_inches='tight')
plt.close()
print("✓ Training curves saved!")

# ============================================================================
# PHASE 6: EVALUATE MODEL PERFORMANCE
# ============================================================================
print("\n" + "=" * 70)
print("PHASE 6: MODEL EVALUATION")
print("=" * 70)

# Load best model
best_model = keras.models.load_model(os.path.join(MODELS_PATH, 'best_model.h5'))

# Evaluate on test set
test_loss, test_accuracy = best_model.evaluate(X_test, y_test, verbose=0)

print("\n📊 MODEL EVALUATION ON TEST SET")
print("=" * 70)
print(f"Test Loss: {test_loss:.4f}")
print(f"Test Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
print("=" * 70)

# Generate predictions
print("\n🔮 Generating predictions on test set...")
y_pred = best_model.predict(X_test, verbose=0)
y_pred_classes = np.argmax(y_pred, axis=1)

# Classification report
print("\n📈 CLASSIFICATION REPORT")
print("=" * 70)
print(classification_report(y_test, y_pred_classes, target_names=label_encoder.classes_))

# Calculate metrics per class
print("\n🎯 PER-CLASS METRICS")
print("=" * 70)
precision = precision_score(y_test, y_pred_classes, average=None)
recall = recall_score(y_test, y_pred_classes, average=None)
f1 = f1_score(y_test, y_pred_classes, average=None)

for i, plant in enumerate(label_encoder.classes_):
    print(f"{plant}:")
    print(f"  Precision: {precision[i]:.4f}")
    print(f"  Recall: {recall[i]:.4f}")
    print(f"  F1-Score: {f1[i]:.4f}")

# Confusion Matrix
print("\n🔲 Creating confusion matrix...")
cm = confusion_matrix(y_test, y_pred_classes)

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=label_encoder.classes_,
            yticklabels=label_encoder.classes_,
            cbar_kws={'label': 'Count'},
            ax=ax)
ax.set_ylabel('True Label', fontsize=12, fontweight='bold')
ax.set_xlabel('Predicted Label', fontsize=12, fontweight='bold')
ax.set_title('Confusion Matrix - Test Set', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(MODELS_PATH, 'confusion_matrix.png'), dpi=100, bbox_inches='tight')
plt.close()
print("✓ Confusion matrix saved!")

# ============================================================================
# PHASE 7: SAVE MODEL AND PREPROCESSING PARAMETERS
# ============================================================================
print("\n" + "=" * 70)
print("PHASE 7: SAVING MODEL AND PARAMETERS")
print("=" * 70)

# Save label encoder
pickle.dump(label_encoder, open(os.path.join(MODELS_PATH, 'label_encoder.pkl'), 'wb'))

# Save preprocessing parameters
preprocessing_params = {
    'IMG_HEIGHT': IMG_HEIGHT,
    'IMG_WIDTH': IMG_WIDTH,
    'IMG_CHANNELS': 3,
    'NORMALIZATION': 255.0
}
pickle.dump(preprocessing_params, open(os.path.join(MODELS_PATH, 'preprocessing_params.pkl'), 'wb'))

# Save model information
model_info = {
    'model_type': 'MobileNetV2 Transfer Learning',
    'architecture': 'MobileNetV2 + Dense Layers',
    'training_samples': len(X_train),
    'validation_samples': len(X_val),
    'test_samples': len(X_test),
    'number_of_classes': num_classes,
    'classes': list(label_encoder.classes_),
    'test_accuracy': float(test_accuracy),
    'test_loss': float(test_loss),
    'epochs_trained': len(history.history['loss'])
}
pickle.dump(model_info, open(os.path.join(MODELS_PATH, 'model_info.pkl'), 'wb'))

print("\n✓ Model artifacts saved!")
print(f"  - Best model: {os.path.join(MODELS_PATH, 'best_model.h5')}")
print(f"  - Label encoder: {os.path.join(MODELS_PATH, 'label_encoder.pkl')}")
print(f"  - Preprocessing params: {os.path.join(MODELS_PATH, 'preprocessing_params.pkl')}")
print(f"  - Model info: {os.path.join(MODELS_PATH, 'model_info.pkl')}")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 70)
print("TRAINING SUMMARY")
print("=" * 70)
print(f"\n✅ Model Training Complete!")
print(f"\n📊 Key Metrics:")
print(f"  • Test Accuracy: {test_accuracy*100:.2f}%")
print(f"  • Test Loss: {test_loss:.4f}")
print(f"  • Classes: {num_classes}")
print(f"  • Model Architecture: MobileNetV2 Transfer Learning")
print(f"\n📁 Output Files Generated:")
print(f"  • class_distribution.png")
print(f"  • sample_images.png")
print(f"  • training_curves.png")
print(f"  • confusion_matrix.png")
print(f"  • best_model.h5")
print(f"  • label_encoder.pkl")
print(f"  • preprocessing_params.pkl")
print(f"  • model_info.pkl")
print("\n🚀 Ready to use with Flask web interface!")
print("=" * 70)
