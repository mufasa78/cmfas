/**
 * Prescription.js - Handles prescription-related functionality
 */

/**
 * Initializes the prescription form with auto-complete functionality
 */
function initPrescriptionForm() {
    // Get the materials select element
    const materialsSelect = document.getElementById('materials');
    if (!materialsSelect) return;
    
    // Initialize Select2 for materials with search and multiple selection
    $(materialsSelect).select2({
        placeholder: 'Select medicinal materials',
        allowClear: true,
        multiple: true,
        width: '100%',
        theme: 'bootstrap4'
    });
    
    // Initialize Select2 for efficacy categories with tags
    $('#efficacy_categories').select2({
        placeholder: 'Enter efficacy categories',
        tags: true,
        tokenSeparators: [','],
        width: '100%',
        theme: 'bootstrap4'
    });
}

/**
 * Initializes the search form
 */
function initSearchForm() {
    // Get the material select element
    const materialSelect = document.getElementById('material');
    if (!materialSelect) return;
    
    // Initialize Select2 for material with search
    $(materialSelect).select2({
        placeholder: 'Select a medicinal material',
        allowClear: true,
        width: '100%',
        theme: 'bootstrap4'
    });
    
    // Initialize Select2 for category
    $('#category').select2({
        placeholder: 'Select an efficacy category',
        allowClear: true,
        width: '100%',
        theme: 'bootstrap4'
    });
}

/**
 * Loads prescription details via AJAX
 * @param {number} prescriptionId - ID of the prescription to load
 */
function loadPrescriptionDetails(prescriptionId) {
    // Show loading indicator
    const detailsContainer = document.getElementById('prescription-details');
    if (!detailsContainer) return;
    
    detailsContainer.innerHTML = `
        <div class="text-center">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
    `;
    
    // Fetch prescription details
    fetch(`/api/prescription/${prescriptionId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(prescription => {
            // Generate HTML for materials
            const materialsHtml = prescription.materials.map(material => `
                <div class="col-md-6 mb-2">
                    <div class="card bg-dark text-white">
                        <div class="card-body">
                            <h5 class="card-title">${material.name}</h5>
                            <div class="card-text">
                                <small class="text-muted">
                                    Property: ${material.property || 'N/A'} | 
                                    Flavor: ${material.flavor || 'N/A'} | 
                                    Meridian: ${material.meridian || 'N/A'}
                                </small>
                            </div>
                        </div>
                    </div>
                </div>
            `).join('');
            
            // Generate HTML for efficacy categories
            const categoriesHtml = prescription.efficacy_categories.map(category => 
                `<span class="badge bg-info me-1">${category.name}</span>`
            ).join('');
            
            // Update details container
            detailsContainer.innerHTML = `
                <div class="row mb-4">
                    <div class="col-md-12">
                        <h3>${prescription.name}</h3>
                        <p>${prescription.description || 'No description available.'}</p>
                        <div class="mb-3">
                            <strong>Efficacy:</strong> ${prescription.efficacy || 'N/A'}
                        </div>
                        <div class="mb-3">
                            <strong>Categories:</strong> 
                            ${categoriesHtml || '<span class="text-muted">None specified</span>'}
                        </div>
                    </div>
                </div>
                
                <h4>Medicinal Materials</h4>
                <div class="row">
                    ${materialsHtml || '<div class="col-12"><p class="text-muted">No materials found for this prescription.</p></div>'}
                </div>
            `;
            
            // Scroll to details
            detailsContainer.scrollIntoView({ behavior: 'smooth' });
        })
        .catch(error => {
            console.error('Error fetching prescription details:', error);
            detailsContainer.innerHTML = `
                <div class="alert alert-danger" role="alert">
                    Failed to load prescription details. Please try again.
                </div>
            `;
        });
}

/**
 * Initializes the formula optimization form
 */
function initFormulaForm() {
    // Get the base materials select element
    const baseMaterialsSelect = document.getElementById('base_materials');
    if (!baseMaterialsSelect) return;
    
    // Initialize Select2 for base materials with search and multiple selection
    $(baseMaterialsSelect).select2({
        placeholder: 'Select base materials (optional)',
        allowClear: true,
        multiple: true,
        width: '100%',
        theme: 'bootstrap4'
    });
}

/**
 * Handles file upload validation for data import
 */
function validateFileUpload() {
    const fileInput = document.getElementById('file');
    const importType = document.getElementById('import_type');
    const submitBtn = document.getElementById('upload_btn');
    
    if (!fileInput || !importType || !submitBtn) return;
    
    // Enable/disable submit button based on form validity
    function updateSubmitButton() {
        if (fileInput.files.length > 0 && importType.value) {
            submitBtn.disabled = false;
        } else {
            submitBtn.disabled = true;
        }
    }
    
    fileInput.addEventListener('change', updateSubmitButton);
    importType.addEventListener('change', updateSubmitButton);
    
    // Initial check
    updateSubmitButton();
}

// Initialize all prescription-related functionality when document is ready
document.addEventListener('DOMContentLoaded', function() {
    initPrescriptionForm();
    initSearchForm();
    initFormulaForm();
    validateFileUpload();
    
    // Check if we need to load prescription details
    const prescriptionId = new URLSearchParams(window.location.search).get('view_prescription');
    if (prescriptionId) {
        loadPrescriptionDetails(prescriptionId);
    }
});
