import pytest
import base64
from io import open
from svm_service.app import app 

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_predict_genre(client):
    with open('tests/test_audio.wav', 'rb') as audio_file:
        audio_data = audio_file.read()
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')  
    
    response = client.post('/predict', json={"wav_music": audio_base64})

    assert response.status_code == 200

    assert 'genre' in response.get_json()
