document.addEventListener('DOMContentLoaded', function() {
    // Get form element
    const calculatorForm = document.getElementById('calculatorForm');
    
    // Add event listener for form submission
    calculatorForm.addEventListener('submit', function(event) {
        event.preventDefault();
        calculateDistance();
    });
    
    // Add event listeners for preset buttons
    const presetButtons = document.querySelectorAll('.preset-btn');
    presetButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Get coordinates from data attributes
            const lat1 = this.getAttribute('data-lat1');
            const lon1 = this.getAttribute('data-lon1');
            const lat2 = this.getAttribute('data-lat2');
            const lon2 = this.getAttribute('data-lon2');
            
            // Fill the form inputs
            document.getElementById('lat1').value = lat1;
            document.getElementById('lon1').value = lon1;
            document.getElementById('lat2').value = lat2;
            document.getElementById('lon2').value = lon2;
        });
    });
    
    // Function to handle distance calculation
    function calculateDistance() {
        // Get form data
        const formData = new FormData(calculatorForm);
        
        // Hide previous error message if any
        hideError();
        
        // Send AJAX request to the server
        fetch('/calculate', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displayResults(data);
                updateRecentCalculations(data);
            } else {
                showError(data.error);
            }
        })
        .catch(error => {
            showError('An error occurred while processing your request.');
            console.error('Error:', error);
        });
    }
    
    // Function to display calculation results
    function displayResults(data) {
        // Show results card
        document.getElementById('resultsCard').classList.remove('d-none');
        
        // Update result fields
        document.getElementById('point1Result').textContent = data.point1;
        document.getElementById('point2Result').textContent = data.point2;
        document.getElementById('distanceResult').textContent = `${data.distance_km} km`;
        document.getElementById('alternateDistance').textContent = `(${data.distance_mi} miles)`;
        
        // Scroll to results
        document.getElementById('resultsCard').scrollIntoView({ behavior: 'smooth' });
    }
    
    // Function to update recent calculations list
    function updateRecentCalculations(data) {
        const recentCalculationsElement = document.getElementById('recentCalculations');
        
        // Clear current content
        recentCalculationsElement.innerHTML = '';
        
        // Create a list group
        const listGroup = document.createElement('ul');
        listGroup.className = 'list-group list-group-flush';
        
        // Create a list item for the new calculation
        const listItem = document.createElement('li');
        listItem.className = 'list-group-item bg-transparent';
        
        // Fill list item with calculation data
        listItem.innerHTML = `
            <h5 class="mb-1">${data.distance_km} km</h5>
            <p class="mb-0 small">
                From ${data.point1} to ${data.point2}
            </p>
        `;
        
        // Add to the list
        listGroup.appendChild(listItem);
        
        // Add the list to the container
        recentCalculationsElement.appendChild(listGroup);
    }
    
    // Function to show error message
    function showError(message) {
        const errorAlert = document.getElementById('errorAlert');
        const errorMessage = document.getElementById('errorMessage');
        
        errorMessage.textContent = message;
        errorAlert.classList.remove('d-none');
        
        // Hide results if any
        document.getElementById('resultsCard').classList.add('d-none');
        
        // Scroll to error
        errorAlert.scrollIntoView({ behavior: 'smooth' });
    }
    
    // Function to hide error message
    function hideError() {
        document.getElementById('errorAlert').classList.add('d-none');
    }
});
