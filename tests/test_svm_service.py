import sys
import pytest
import base64
import os
from io import open

# Add the svm_service directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '../svm_service'))

from music_genre_classifier.svm_service.app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_predict_genre(client):
    audio_file_path = os.path.join(os.path.dirname(__file__), 'test_audio.wav')
    
    with open(audio_file_path, 'rb') as audio_file:
        audio_data = audio_file.read()
        audio_base64 = base64.b64encode(audio_data).decode('utf-8') 
    
    response = client.post('/predict', json={"wav_music": audio_base64})

    assert response.status_code == 200

    json_response = response.get_json()

    assert 'genre' in json_response

    assert json_response['genre'] == 'classical'  