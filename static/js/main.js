// Main JavaScript file for Pokemon Player State Tracker

// API base URL
const API_BASE_URL = 'http://localhost:8000';

// Utility functions
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString();
}

function showAlert(message, type = 'success') {
    const alertContainer = document.getElementById('alertContainer');
    if (!alertContainer) {
        const container = document.createElement('div');
        container.id = 'alertContainer';
        container.style.position = 'fixed';
        container.style.top = '20px';
        container.style.right = '20px';
        container.style.zIndex = '9999';
        document.body.appendChild(container);
    }
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    document.getElementById('alertContainer').appendChild(alert);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        alert.classList.remove('show');
        setTimeout(() => alert.remove(), 300);
    }, 5000);
}

// API request helper
async function apiRequest(endpoint, method = 'GET', data = null) {
    const url = `${API_BASE_URL}${endpoint}`;
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json',
        },
    };
    
    if (data && (method === 'POST' || method === 'PUT')) {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(url, options);
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.message || 'API request failed');
        }
        
        return result;
    } catch (error) {
        console.error('API request error:', error);
        showAlert(error.message || 'An error occurred while communicating with the server', 'danger');
        throw error;
    }
}

// Check if API server is running
async function checkApiStatus() {
    try {
        const result = await apiRequest('/');
        console.log('API Status:', result);
        return result.success;
    } catch (error) {
        console.error('API Status Check Failed:', error);
        showAlert('Cannot connect to the API server. Please make sure it is running.', 'danger');
        return false;
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', async () => {
    // Check API status
    await checkApiStatus();
});
