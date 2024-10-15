const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const uploadText = document.getElementById('uploadText');

        // Handle clicking the upload area to trigger file input
        uploadArea.addEventListener('click', () => {
            fileInput.click();  // Simulate click on hidden file input
        });

        // Handle file selection from file input
        fileInput.addEventListener('change', (event) => {
            const file = event.target.files[0];
            if (file) {
                displayFileName(file.name);
            }
        });

        // Handle drag and drop functionality
        uploadArea.addEventListener('dragover', (event) => {
            event.preventDefault(); // Prevent default behavior (Prevent file from opening)
            uploadArea.style.backgroundColor = '#e6f7ff'; // Optional: Change background color to indicate dragover
        });

        uploadArea.addEventListener('dragleave', () => {
            uploadArea.style.backgroundColor = ''; // Reset background when dragging ends
        });

        uploadArea.addEventListener('drop', (event) => {
            event.preventDefault(); // Prevent default behavior
            uploadArea.style.backgroundColor = ''; // Reset background

            const file = event.dataTransfer.files[0]; // Get the dropped file
            if (file && file.type === 'audio/wav') {
                displayFileName(file.name);
            } else {
                uploadText.textContent = 'Please upload a valid .wav file';
            }
        });

        // Function to display the file name
        function displayFileName(fileName) {
            uploadText.textContent = `Selected file: ${fileName}`;
        }