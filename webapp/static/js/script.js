document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const fileInput = document.getElementById('fileInput');
    const resultsSection = document.getElementById('resultsSection');
    const errorSection = document.getElementById('errorSection');
    const loadingSpinner = document.getElementById('loadingSpinner');

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
        uploadForm.dispatchEvent(new Event('submit'));
    }

    // Form submission
    uploadForm.addEventListener('submit', function(e) {
        e.preventDefault();
        console.log("Form submitted!");

        if (!fileInput.files.length) {
            alert('Please select an image');
            return;
        }

        const file = fileInput.files[0];
        const formData = new FormData();
        formData.append('file', file);
        
        console.log("File selected:", file.name, file.type, file.size);
        
        // Show loading spinner
        loadingSpinner.style.display = 'flex';
        resultsSection.style.display = 'none';
        errorSection.style.display = 'none';

        console.log("Sending prediction request to /predict...");
        
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
        
        errorSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
});

function resetForm() {
    document.getElementById('uploadForm').reset();
    document.getElementById('resultsSection').style.display = 'none';
    document.getElementById('errorSection').style.display = 'none';
    document.getElementById('loadingSpinner').style.display = 'none';
}
