import os
import numpy as np
import librosa
import cv2
from tensorflow.keras.applications import VGG19
from tensorflow.keras.layers import Dense, Flatten, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.preprocessing import LabelEncoder
from pathlib import Path

# Set paths
DATA_PATH = "../data/genres_original"
MODEL_SAVE_PATH = "vgg19_model_saved"  # Sauvegarde dans le format SavedModel (dossier)

# Number of genres (assuming you have 10 genres)
GENRES = ['blues', 'classical', 'country', 'disco', 'hiphop', 
          'jazz', 'metal', 'pop', 'reggae', 'rock']
NUM_GENRES = len(GENRES)

def data_generator(batch_size=8, target_shape=(128, 128), subset='train'):
    """Generator to load and preprocess audio files on the fly, with subset for training or validation."""
    label_encoder = LabelEncoder()
    label_encoder.fit(GENRES)
    genre_labels = {genre: idx for idx, genre in enumerate(GENRES)}

    while True:
        X, y = [], []
        for genre in GENRES:
            genre_path = Path(DATA_PATH) / genre
            for i, filename in enumerate(os.listdir(genre_path)):
                if filename.endswith(".wav"):
                    file_path = genre_path / filename
                    if subset == 'train' and i % 5 == 0:
                        continue  # Skip 20% of data for validation
                    elif subset == 'val' and i % 5 != 0:
                        continue  # Use 20% of data for validation

                    features = extract_features(file_path, target_shape)
                    if features is not None:
                        X.append(features)
                        y.append(genre_labels[genre])

                        if len(X) == batch_size:
                            X = np.array(X)
                            y = to_categorical(np.array(y), num_classes=NUM_GENRES)
                            yield X, y
                            X, y = [], []  # Reset for next batch

def extract_features(file_path, target_shape=(128, 128)):
    """Extract Mel spectrogram features from an audio file and prepare for VGG19."""
    try:
        y, sr = librosa.load(file_path, sr=22050, duration=30)
        mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
        mel_spectrogram_db = librosa.power_to_db(mel_spectrogram, ref=np.max)
        spectrogram_resized = cv2.resize(mel_spectrogram_db, target_shape)
        spectrogram_3ch = np.stack([spectrogram_resized]*3, axis=-1)
        return spectrogram_3ch
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

# Set up VGG19 model with adjusted input shape
print("Setting up VGG19 model...")
vgg19_base = VGG19(weights="imagenet", include_top=False, input_shape=(128, 128, 3))

# Freeze the base VGG19 layers to retain pre-trained features
for layer in vgg19_base.layers:
    layer.trainable = False

# Add custom layers on top of VGG19 for our specific task
x = Flatten()(vgg19_base.output)
x = Dense(256, activation="relu")(x)
x = Dropout(0.5)(x)
x = Dense(128, activation="relu")(x)
x = Dropout(0.5)(x)
output = Dense(NUM_GENRES, activation="softmax")(x)
model = Model(inputs=vgg19_base.input, outputs=output)

# Compile model
model.compile(optimizer=Adam(learning_rate=0.0001), loss="categorical_crossentropy", metrics=["accuracy"])

# Early stopping callback
early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

# Determine steps per epoch and validation steps
batch_size = 8
total_files = sum(len(files) for _, _, files in os.walk(DATA_PATH))
steps_per_epoch = int((total_files * 0.8) // batch_size)  # 80% pour l'entraînement
validation_steps = int((total_files * 0.2) // batch_size)  # 20% pour la validation

# Separate generators for training and validation
train_generator = data_generator(batch_size=batch_size, target_shape=(128, 128), subset='train')
val_generator = data_generator(batch_size=batch_size, target_shape=(128, 128), subset='val')

# Train model with separate train and validation generators
print("Training the model...")
history = model.fit(train_generator, epochs=10, steps_per_epoch=steps_per_epoch,
                    validation_data=val_generator, validation_steps=validation_steps,
                    callbacks=[early_stopping])

# Chemin pour le modèle en format .keras
MODEL_SAVE_PATH = "vgg19_model_full_data.keras"

# Sauvegarde du modèle au format .keras
model.save(MODEL_SAVE_PATH)  # Keras sauvegardera automatiquement au format .keras
print(f"Model saved to {MODEL_SAVE_PATH}")
