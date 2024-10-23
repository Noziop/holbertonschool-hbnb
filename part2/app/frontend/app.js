document.addEventListener('DOMContentLoaded', function() {
    function handleFormSubmit(formId, apiEndpoint) {
        const form = document.getElementById(formId);
        const messageElement = document.getElementById(`${formId}-message`);

        form.addEventListener('submit', async function(event) {
            event.preventDefault();
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());

            try {
                const response = await fetch(apiEndpoint, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const result = await response.json();
                displayResult(formId, result);
            } catch (error) {
                displayResult(formId, { error: error.message });
            }
        });
    }

    function handleGetAllButton(buttonId, apiEndpoint) {
        const button = document.getElementById(buttonId);
        if (!button) {
            console.error(`Button with id "${buttonId}" not found`);
            return;
        }
        
        button.addEventListener('click', async function() {
            try {
                const response = await fetch(apiEndpoint);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
    
                const result = await response.json();
                displayResult(buttonId, result);
            } catch (error) {
                displayResult(buttonId, { error: error.message });
            }
        });
    }

    function displayResult(elementId, result) {
        // Ajuste l'ID pour correspondre à celui dans le HTML
        const messageId = elementId.startsWith('get-') ? elementId.replace('get-', '') : elementId;
        const messageElement = document.getElementById(`${messageId}-message`);
        if (messageElement) {
            messageElement.textContent = JSON.stringify(result, null, 2);
        } else {
            console.error(`Element with id "${messageId}-message" not found`);
        }
    }

    // Configuration des formulaires
    handleFormSubmit('create-user-form', 'http://localhost:5000/api/v1/users/');
    handleFormSubmit('create-place-form', 'http://localhost:5000/api/v1/places/');
    handleFormSubmit('create-amenity-form', 'http://localhost:5000/api/v1/amenities/');
    handleFormSubmit('create-review-form', 'http://localhost:5000/api/v1/reviews/');

    // Configuration des boutons "Get All"
    handleGetAllButton('get-all-users', 'http://localhost:5000/api/v1/users/');
    handleGetAllButton('get-all-places', 'http://localhost:5000/api/v1/places/');
    handleGetAllButton('get-all-amenities', 'http://localhost:5000/api/v1/amenities/');
    handleGetAllButton('get-all-reviews', 'http://localhost:5000/api/v1/reviews/');
});