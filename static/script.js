// Poll the backend every 3 seconds for fire and smoke detection results
setInterval(checkFireSmokeDetection, 3000);

function checkFireSmokeDetection() {
    fetch('/check-fire-smoke')
        .then(response => response.json())
        .then(data => {
            const alertMessage = document.getElementById('alert-message');

            // Clear the message initially
            alertMessage.innerHTML = '';
            alertMessage.style.display = 'none';

            // Check for fire and smoke detection status
            if (data.fireDetected && data.smokeDetected) {
                // If both fire and smoke are detected
                alertMessage.innerHTML = '🔥 Fire and 💨 Smoke Detected!';
                alertMessage.style.color = 'red'; // Red for fire and smoke
                alertMessage.style.display = 'block';
            } else if (data.fireDetected) {
                // If only fire is detected
                alertMessage.innerHTML = '🔥 Fire Detected!';
                alertMessage.style.color = 'red'; // Red for fire
                alertMessage.style.display = 'block';
            } else if (data.smokeDetected) {
                // If only smoke is detected
                alertMessage.innerHTML = '💨 Smoke Detected!';
                alertMessage.style.color = 'gray'; // Gray for smoke
                alertMessage.style.display = 'block';
            } else {
                // If neither fire nor smoke is detected
                alertMessage.innerHTML = '';
                alertMessage.style.display = 'none';
            }
        })
        .catch(error => {
            console.error('Error checking fire and smoke detection:', error);
        });
}
