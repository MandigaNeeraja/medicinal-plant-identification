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
        const label = fileInputWrapper.querySelector('label');
        label.style.borderColor = 'rgba(138, 43, 226, 0.8)';
        label.style.background = 'rgba(138, 43, 226, 0.05)';
        label.style.transform = 'scale(1.01)';
    }

    function unhighlight(e) {
        const label = fileInputWrapper.querySelector('label');
        label.style.borderColor = 'rgba(138, 43, 226, 0.3)';
        label.style.background = 'rgba(255, 255, 255, 0.02)';
        label.style.transform = 'scale(1)';
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

        // Display confidence with animation
        const confidence = data.confidence * 100;
        const confidenceBar = document.getElementById('confidenceBar');
        const confidencePercent = document.getElementById('confidencePercent');
        
        // Reset width first for animation
        confidenceBar.style.width = '0%';
        confidencePercent.textContent = '0%';
        
        // Animate after a short delay
        setTimeout(() => {
            confidenceBar.style.width = confidence + '%';
            confidencePercent.textContent = confidence.toFixed(1) + '%';
        }, 100);

        // Display medicinal uses as pill tags
        const usesContainer = document.getElementById('usesContainer');
        usesContainer.innerHTML = '';
        if (data.medicinal_uses && data.medicinal_uses.length > 0) {
            data.medicinal_uses.forEach(use => {
                const useTag = document.createElement('span');
                useTag.className = 'use-tag';
                useTag.textContent = use;
                usesContainer.appendChild(useTag);
            });
        }

        // Display all predictions
        const predictionsList = document.getElementById('predictionsList');
        predictionsList.innerHTML = '';
        
        Object.entries(data.all_predictions)
            .sort((a, b) => b[1] - a[1])
            .forEach(([plant, score]) => {
                const percentage = (score * 100).toFixed(1);
                const predictionItem = document.createElement('div');
                predictionItem.className = 'prediction-item';
                
                predictionItem.innerHTML = `
                    <span class="prediction-name">${plant}</span>
                    <div class="prediction-bar">
                        <div class="prediction-bar-fill" style="width: 0%"></div>
                    </div>
                    <span class="prediction-percent">${percentage}%</span>
                `;
                
                predictionsList.appendChild(predictionItem);
                
                // Animate the prediction bar
                setTimeout(() => {
                    predictionItem.querySelector('.prediction-bar-fill').style.width = percentage + '%';
                }, 200);
            });

        // Add "Know Medicinal Uses" button/link
        const knowContainer = document.getElementById('knowUsesContainer');
        knowContainer.innerHTML = '';
        const plantName = data.plant;
        if (plantName) {
            const a = document.createElement('a');
            a.href = '/plant/' + encodeURIComponent(plantName);
            a.className = 'btn btn-primary';
            a.textContent = 'Know More Medicinal Uses';
            knowContainer.appendChild(a);
        }

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
