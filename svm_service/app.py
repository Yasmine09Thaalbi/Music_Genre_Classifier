from flask import Flask, request, jsonify
import joblib
import numpy as np
import librosa
import base64
from io import BytesIO
from flask_cors import CORS 

app = Flask(__name__)
CORS(app)

model = joblib.load('svm_model.pkl')

@app.route('/predict', methods=['POST'])
def predict_genre():
    data = request.json['wav_music']
    audio_bytes = base64.b64decode(data)
    y, sr = librosa.load(BytesIO(audio_bytes))
    features = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13).T, axis=0)
    prediction = model.predict([features])[0]
    return jsonify({'genre': prediction})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
