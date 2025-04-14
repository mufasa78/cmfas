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
        placeholder: getTranslation('select_medicinal_materials'),
        allowClear: true,
        multiple: true,
        width: '100%',
        theme: 'bootstrap-5'
    });

    // Initialize Select2 for efficacy categories with tags
    $('#efficacy_categories').select2({
        placeholder: getTranslation('enter_efficacy_categories'),
        tags: true,
        tokenSeparators: [','],
        width: '100%',
        theme: 'bootstrap-5'
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
        placeholder: getTranslation('select_a_medicinal_material'),
        allowClear: true,
        width: '100%',
        theme: 'bootstrap-5'
    });

    // Initialize Select2 for category
    $('#category').select2({
        placeholder: getTranslation('select_an_efficacy_category'),
        allowClear: true,
        width: '100%',
        theme: 'bootstrap-5'
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
                <span class="visually-hidden">${getTranslation('loading')}</span>
            </div>
        </div>
    `;

    // Fetch prescription details
    fetch(`/api/prescription/${prescriptionId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(getTranslation('network_error'));
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
                                    ${getTranslation('property_label')}: ${material.property || getTranslation('not_available')} |
                                    ${getTranslation('flavor_label')}: ${material.flavor || getTranslation('not_available')} |
                                    ${getTranslation('meridian_label')}: ${material.meridian || getTranslation('not_available')}
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
                        <p>${prescription.description || getTranslation('no_description')}</p>
                        <div class="mb-3">
                            <strong>${getTranslation('efficacy_label')}:</strong> ${prescription.efficacy || getTranslation('not_available')}
                        </div>
                        <div class="mb-3">
                            <strong>${getTranslation('categories_label')}:</strong>
                            ${categoriesHtml || `<span class="text-muted">${getTranslation('none_specified')}</span>`}
                        </div>
                    </div>
                </div>

                <h4>${getTranslation('medicinal_materials_heading')}</h4>
                <div class="row">
                    ${materialsHtml || `<div class="col-12"><p class="text-muted">${getTranslation('no_materials')}</p></div>`}
                </div>
            `;

            // Scroll to details
            detailsContainer.scrollIntoView({ behavior: 'smooth' });
        })
        .catch(error => {
            console.error('Error fetching prescription details:', error);
            detailsContainer.innerHTML = `
                <div class="alert alert-danger" role="alert">
                    ${getTranslation('load_error')}
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
        placeholder: getTranslation('select_base_materials'),
        allowClear: true,
        multiple: true,
        width: '100%',
        theme: 'bootstrap-5'
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
