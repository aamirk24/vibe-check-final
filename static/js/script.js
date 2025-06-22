document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('webcam');
    const canvas = document.getElementById('canvas');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const resultsDiv = document.getElementById('results');
    const moodSpan = document.getElementById('mood');
    const playlistContainer = document.getElementById('playlist-container');
    const loadingDiv = document.getElementById('loading');
    const errorDiv = document.getElementById('error');
    const errorMessage = document.getElementById('error-message');
    const feedbackBtn = document.getElementById('feedbackBtn');
    const moodFeedbackSelect = document.getElementById('mood-feedback');
    
    const confidenceContainer = document.getElementById('confidence-container');
    const confidenceBarFill = document.getElementById('confidence-bar-fill');
    const confidenceValue = document.getElementById('confidence-value');

    let lastPredictionId = null; 
    let capturedImageData = null;

    // Access webcam
    if (navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true, audio: false })
            .then(stream => { 
                video.srcObject = stream;
                // Set canvas dimensions once video is loaded
                video.onloadedmetadata = () => {
                    canvas.width = video.videoWidth;
                    canvas.height = video.videoHeight;
                };
             })
            .catch(err => {
                console.error("Error accessing webcam: ", err);
                showError("Could not access your webcam. Please enable it in your browser settings.");
            });
    }

    function showError(message) {
        errorMessage.textContent = message;
        errorDiv.classList.remove('hidden');
        loadingDiv.classList.add('hidden');
        resultsDiv.classList.add('hidden');
    }

    analyzeBtn.addEventListener('click', async () => {
        resultsDiv.classList.add('hidden');
        errorDiv.classList.add('hidden');
        loadingDiv.classList.remove('hidden');

        // Capture a frame from the video
        const context = canvas.getContext('2d');
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        capturedImageData = canvas.toDataURL('image/jpeg');

        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ image: capturedImageData }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Failed to analyze image');
            }

            const data = await response.json();
            
            lastPredictionId = data.prediction_id;
            displayResults(data.mood, data.confidence, data.playlist);

        } catch (error) {
            console.error('Error:', error);
            showError(`Analysis failed: ${error.message}`);
        } finally {
            loadingDiv.classList.add('hidden');
        }
    });

    function displayResults(mood, confidence, playlistUrl) {
        // Update mood text
        moodSpan.textContent = mood;

        // Update confidence bar
        const confidencePercentage = (confidence * 100).toFixed(1);
        confidenceBarFill.style.width = `${confidencePercentage}%`;
        confidenceValue.textContent = `${confidencePercentage}%`;
        
        // Update Spotify playlist
        playlistContainer.innerHTML = `<iframe style="border-radius:12px" src="${playlistUrl}" width="100%" height="352" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>`;
        
        // Show the entire results container
        resultsDiv.classList.remove('hidden');
    }

    feedbackBtn.addEventListener('click', async () => {
        const selectedMood = moodFeedbackSelect.value;
        
        if (!lastPredictionId) {
            alert("Please analyze an image first before submitting feedback.");
            return;
        }

        try {
            await fetch('/feedback', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    prediction_id: lastPredictionId, 
                    mood: selectedMood 
                }),
            });
            alert("Thank you for your feedback! It has been logged.");
        } catch (error) {
            console.error('Error submitting feedback:', error);
            alert("Could not submit feedback.");
        }
    });
});