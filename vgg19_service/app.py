from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
import librosa
import cv2
import base64
from io import BytesIO

from flask_cors import CORS 

app = Flask(__name__)
CORS(app)

model = tf.keras.models.load_model("vgg19_model_full_data.keras")


GENRES = ['blues', 'classical', 'country', 'disco', 'hiphop', 
          'jazz', 'metal', 'pop', 'reggae', 'rock']

def preprocess_audio(audio_data):
    """Convertir les données audio en spectrogramme Mel et les redimensionner pour VGG19."""
    try:
        # Charger l'audio
        y, sr = librosa.load(BytesIO(audio_data), sr=22050, duration=30)
        
        # Convertir en spectrogramme Mel
        mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
        mel_spectrogram_db = librosa.power_to_db(mel_spectrogram, ref=np.max)
        
        # Redimensionner à (128, 128) et empiler pour créer 3 canaux
        spectrogram_resized = cv2.resize(mel_spectrogram_db, (128, 128))
        spectrogram_3ch = np.stack([spectrogram_resized] * 3, axis=-1)  # Convertir en 3 canaux pour VGG19
        spectrogram_3ch = np.expand_dims(spectrogram_3ch, axis=0)  # Ajouter la dimension batch
        
        return spectrogram_3ch
    except Exception as e:
        print(f"Erreur lors de la conversion audio : {e}")
        return None

@app.route('/vgg19_predict', methods=['POST'])
def predict_genre():
    try:
        # Étape 1 : Vérifier la donnée reçue
        data = request.json.get('wav_music')
        if not data:
            return jsonify({'error': 'Données audio manquantes'}), 400

        # Étape 2 : Décoder les données audio
        try:
            audio_bytes = base64.b64decode(data)
        except Exception as decode_error:
            print(f"Erreur lors du décodage Base64 : {decode_error}")
            return jsonify({'error': 'Échec du décodage Base64'}), 400

        # Étape 3 : Prétraitement de l’audio
        spectrogram = preprocess_audio(audio_bytes)
        if spectrogram is None:
            return jsonify({'error': 'Échec du prétraitement de l’audio'}), 500

        # Étape 4 : Prédiction avec le modèle
        try:
            prediction = model.predict(spectrogram)
        except Exception as model_error:
            print(f"Erreur lors de la prédiction : {model_error}")
            return jsonify({'error': 'Échec de la prédiction'}), 500

        genre_index = np.argmax(prediction)
        genre_name = GENRES[genre_index]

        return jsonify({'genre': genre_name})

    except Exception as e:
        print(f"Erreur inattendue : {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
