// JavaScript for Saves page

// DOM Elements
const savesTableBody = document.getElementById('savesTableBody');
const createSaveBtn = document.getElementById('createSaveBtn');
const confirmLoadBtn = document.getElementById('confirmLoadBtn');
const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');

// Global variables
let currentSaveId = null;

// Initialize on page load
document.addEventListener('DOMContentLoaded', async () => {
    // Load saves
    await loadSaves();
    
    // Set up event listeners
    if (createSaveBtn) {
        createSaveBtn.addEventListener('click', createSave);
    }
});

// Load saves from API
async function loadSaves() {
    try {
        const result = await apiRequest('/saves/');
        
        if (result.success) {
            renderSaves(result.data.saves);
        }
    } catch (error) {
        console.error('Error loading saves:', error);
    }
}

// Render saves table
function renderSaves(saves) {
    savesTableBody.innerHTML = '';
    
    if (saves.length === 0) {
        const row = document.createElement('tr');
        row.innerHTML = `<td colspan="6" class="text-center">No save files found</td>`;
        savesTableBody.appendChild(row);
        return;
    }
    
    saves.forEach(save => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${save.id}</td>
            <td>${save.name}</td>
            <td>${save.game_version}</td>
            <td>${formatDate(save.created_at)}</td>
            <td>${formatDate(save.last_updated)}</td>
            <td>
                <button class="btn btn-sm btn-success load-save" data-id="${save.id}" data-name="${save.name}" data-created="${save.created_at}">Load</button>
                <button class="btn btn-sm btn-danger delete-save" data-id="${save.id}" data-name="${save.name}">Delete</button>
            </td>
        `;
        savesTableBody.appendChild(row);
    });
    
    // Add event listeners to buttons
    document.querySelectorAll('.load-save').forEach(btn => {
        btn.addEventListener('click', () => showLoadSaveModal(btn.dataset.id, btn.dataset.name, btn.dataset.created));
    });
    
    document.querySelectorAll('.delete-save').forEach(btn => {
        btn.addEventListener('click', () => showDeleteSaveModal(btn.dataset.id, btn.dataset.name));
    });
}

// Create new save
async function createSave() {
    try {
        // Validate form
        const saveName = document.getElementById('saveName').value.trim();
        if (!saveName) {
            showAlert('Save name is required', 'danger');
            return;
        }
        
        const gameVersion = document.getElementById('gameVersion').value;
        
        // Create save data
        const saveData = {
            name: saveName,
            game_version: gameVersion
        };
        
        // Send API request
        const result = await apiRequest('/saves/', 'POST', saveData);
        
        if (result.success) {
            showAlert(`Save file "${saveName}" created successfully`, 'success');
            
            // Close modal and reload saves
            const modal = bootstrap.Modal.getInstance(document.getElementById('createSaveModal'));
            modal.hide();
            
            // Reset form
            document.getElementById('createSaveForm').reset();
            
            // Reload saves
            await loadSaves();
        }
    } catch (error) {
        console.error('Error creating save:', error);
    }
}

// Show load save confirmation modal
function showLoadSaveModal(saveId, saveName, saveCreated) {
    currentSaveId = saveId;
    
    // Update modal content
    document.getElementById('loadSaveName').textContent = saveName;
    document.getElementById('loadSaveCreated').textContent = formatDate(saveCreated);
    
    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('loadSaveModal'));
    modal.show();
    
    // Set up confirm button
    confirmLoadBtn.onclick = loadSave;
}

// Load save
async function loadSave() {
    try {
        const result = await apiRequest(`/saves/${currentSaveId}/load`, 'POST');
        
        if (result.success) {
            showAlert('Save file loaded successfully', 'success');
            
            // Close modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('loadSaveModal'));
            modal.hide();
        }
    } catch (error) {
        console.error('Error loading save:', error);
    }
}

// Show delete save confirmation modal
function showDeleteSaveModal(saveId, saveName) {
    currentSaveId = saveId;
    
    // Update modal content
    document.getElementById('deleteSaveName').textContent = saveName;
    
    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('deleteSaveModal'));
    modal.show();
    
    // Set up confirm button
    confirmDeleteBtn.onclick = deleteSave;
}

// Delete save
async function deleteSave() {
    try {
        const result = await apiRequest(`/saves/${currentSaveId}`, 'DELETE');
        
        if (result.success) {
            showAlert('Save file deleted successfully', 'success');
            
            // Close modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('deleteSaveModal'));
            modal.hide();
            
            // Reload saves
            await loadSaves();
        }
    } catch (error) {
        console.error('Error deleting save:', error);
    }
}
