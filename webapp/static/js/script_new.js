document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const fileInput = document.getElementById('fileInput');
    const previewSection = document.getElementById('previewSection');
    const previewImage = document.getElementById('previewImage');
    const predictBtn = document.getElementById('predictBtn');
    const resultsSection = document.getElementById('resultsSection');
    const errorSection = document.getElementById('errorSection');
    const loadingSpinner = document.getElementById('loadingSpinner');

    let selectedFile = null;

    // Drag and drop functionality
    const fileInputWrapper = document.querySelector('.file-input-wrapper');
    
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        fileInputWrapper.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        fileInputWrapper.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        fileInputWrapper.addEventListener(eventName, unhighlight, false);
    });

    function highlight(e) {
        fileInputWrapper.style.borderColor = '#764ba2';
        fileInputWrapper.style.background = '#f0f1ff';
    }

    function unhighlight(e) {
        fileInputWrapper.style.borderColor = '#667eea';
        fileInputWrapper.style.background = '#f8f9ff';
    }

    // Handle dropped files
    fileInputWrapper.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        fileInput.files = files;
        displayPreview();
    }

    // Handle file selection
    fileInput.addEventListener('change', displayPreview);

    function displayPreview() {
        if (!fileInput.files.length) {
            previewSection.style.display = 'none';
            return;
        }

        selectedFile = fileInput.files[0];
        const reader = new FileReader();

        reader.onload = function(e) {
            console.log("Image preview loaded");
            previewImage.src = e.target.result;
            previewSection.style.display = 'block';
            resultsSection.style.display = 'none';
            errorSection.style.display = 'none';
            loadingSpinner.style.display = 'none';

            // Scroll to preview
            previewSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
        };

        reader.readAsDataURL(selectedFile);
    }

    // Predict button click
    predictBtn.addEventListener('click', function() {
        if (!selectedFile) {
            alert('No image selected');
            return;
        }

        const formData = new FormData();
        formData.append('file', selectedFile);

        console.log("Sending prediction request...");
        console.log("File:", selectedFile.name);
        
        // Show loading spinner
        loadingSpinner.style.display = 'flex';
        resultsSection.style.display = 'none';
        errorSection.style.display = 'none';
        previewSection.style.display = 'none';

        // Send prediction request
        fetch('/predict', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            console.log("Response status:", response.status);
            return response.json();
        })
        .then(data => {
            console.log("Response data:", data);
            loadingSpinner.style.display = 'none';
            
            if (data.success) {
                console.log("Prediction successful!");
                displayResults(data);
            } else {
                console.log("Prediction failed:", data.error || data.message);
                displayError(data.error || data.message || 'Prediction failed. Please try again.');
            }
        })
        .catch(error => {
            console.error("Fetch error:", error);
            loadingSpinner.style.display = 'none';
            displayError('Error during prediction: ' + error.message);
        });
    });

    function displayResults(data) {
        // Display uploaded image
        document.getElementById('uploadedImage').src = data.image_path;

        // Display plant name
        document.getElementById('plantName').textContent = data.plant;

        // Display confidence
        const confidence = data.confidence * 100;
        const confidenceBar = document.getElementById('confidenceBar');
        const confidencePercent = document.getElementById('confidencePercent');
        
        confidenceBar.style.width = confidence + '%';
        confidencePercent.textContent = confidence.toFixed(1) + '%';

        // Display medicinal uses
        if (data.medicinal_uses) {
            const usesList = document.getElementById('useslist');
            usesList.innerHTML = '';
            data.medicinal_uses.forEach(use => {
                const li = document.createElement('li');
                li.textContent = use;
                usesList.appendChild(li);
            });
        }

        // Display all predictions
        const predictionsList = document.getElementById('predictionsList');
        predictionsList.innerHTML = '';
        
        Object.entries(data.all_predictions)
            .sort((a, b) => b[1] - a[1])
            .forEach(([plant, score]) => {
                const percentage = (score * 100).toFixed(1);
                const predictionHTML = `
                    <div class="prediction-item">
                        <span class="prediction-name">${plant}</span>
                        <div class="prediction-bar">
                            <div class="prediction-bar-fill" style="width: ${percentage}%"></div>
                        </div>
                        <span class="percent">${percentage}%</span>
                    </div>
                `;
                predictionsList.innerHTML += predictionHTML;
            });

        // Show results section
        resultsSection.style.display = 'block';
        errorSection.style.display = 'none';
        
        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    function displayError(message) {
        document.getElementById('errorMessage').textContent = message;
        errorSection.style.display = 'block';
        resultsSection.style.display = 'none';
        previewSection.style.display = 'block';
        
        errorSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
});

function changeImage() {
    document.getElementById('fileInput').click();
}

function resetForm() {
    document.getElementById('uploadForm').reset();
    document.getElementById('previewSection').style.display = 'none';
    document.getElementById('resultsSection').style.display = 'none';
    document.getElementById('errorSection').style.display = 'none';
    document.getElementById('loadingSpinner').style.display = 'none';
}
