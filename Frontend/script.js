const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const uploadText = document.getElementById('uploadText');
const resultText = document.getElementById('result');
const classifySvmButton = document.querySelector('.classify-svm');
const classifyVgg19Button = document.querySelector('.classify-vgg19');


uploadArea.addEventListener('click', () => {
    fileInput.click();
});


fileInput.addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
        displayFileName(file.name);
    }
});


uploadArea.addEventListener('dragover', (event) => {
    event.preventDefault();
    uploadArea.style.backgroundColor = '#e6f7ff';
});


uploadArea.addEventListener('dragleave', () => {
    uploadArea.style.backgroundColor = '';
});


uploadArea.addEventListener('drop', (event) => {
    event.preventDefault();
    uploadArea.style.backgroundColor = '';

    const file = event.dataTransfer.files[0];
    if (file) {
        if (file.type === 'audio/wav') {
            displayFileName(file.name);
            fileInput.files = event.dataTransfer.files; 
        } else {
            uploadText.textContent = 'Veuillez télécharger un fichier .wav valide';
        }
    } else {
        uploadText.textContent = 'Aucun fichier sélectionné ou fichier invalide';
    }
});


function displayFileName(fileName) {
    uploadText.textContent = `Fichier sélectionné: ${fileName}`;
}

async function classifyAudio(url) {
    const file = fileInput.files[0];
    if (!file) {
        alert("Veuillez d'abord sélectionner un fichier .wav.");
        return;
    }

    const reader = new FileReader();
    reader.onloadend = async function() {
        const base64Audio = reader.result.split(',')[1]; 

        const payload = {
            "wav_music": base64Audio
        };

        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'  
                },
                body: JSON.stringify(payload)  
            });

            if (response.ok) {
                const result = await response.json();
                resultText.textContent = `Résultat de la classification: ${result.genre}`;
            } else {
                resultText.textContent = `Erreur: ${response.statusText}`;
            }
        } catch (error) {
            resultText.textContent = `Erreur lors de la connexion au serveur: ${error.message}`;
        }
    };
    reader.readAsDataURL(file); 
}


classifySvmButton.addEventListener('click', () => {
    classifySvmButton.disabled = true; 
    classifyAudio('http://localhost:5001/predict').finally(() => {
        classifySvmButton.disabled = false;
    });
    
});


classifyVgg19Button.addEventListener('click', () => {
    classifyVgg19Button.disabled = true; 
    classifyAudio('http://localhost:5002/vgg19_predict').finally(() => {
        classifyVgg19Button.disabled = false;
    });
    
});
