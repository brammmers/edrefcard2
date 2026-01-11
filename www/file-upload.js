// EDRefCard - File Upload Enhancement
// Handles drag-and-drop file upload functionality with immediate validation and preview

document.addEventListener('DOMContentLoaded', () => {
    // Prevent default drag/drop behavior on document
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        document.body.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    // File upload functionality
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileupload');
    const previewContainer = document.getElementById('filePreview'); // Element to be added to HTML

    if (!dropZone || !fileInput) {
        console.error('File upload elements not found');
        return;
    }

    // Highlight drop zone when dragging over it
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            dropZone.classList.add('drag-over');
        });
    });

    // Remove highlight when leaving drop zone
    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            dropZone.classList.remove('drag-over');
        });
    });

    // Handle file drop
    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        const files = e.dataTransfer.files;
        handleFiles(files);
    });

    // Handle file selection via click
    fileInput.addEventListener('change', (e) => {
        handleFiles(e.target.files);
    });

    function handleFiles(files) {
        if (files.length === 0) return;

        const file = files[0];

        // 1. Validation
        if (!validateFile(file)) {
            // Clear input if invalid
            fileInput.value = '';
            // Visual error state is handled in validateFile via UI updates
            return;
        }

        // 2. Set file to input (if from drop)
        if (fileInput.files !== files) {
            fileInput.files = files; // Note: this works in modern browsers
        }

        // 3. Update UI and Preview
        updateFileLabel(file.name);
        generatePreview(file);
    }

    function validateFile(file) {
        const errors = [];

        // Check extension
        if (!file.name.toLowerCase().endsWith('.binds')) {
            errors.push('Invalid file type. Please select a .binds file.');
        }

        // Check size (500KB limit)
        if (file.size > 512000) {
            errors.push('File too large. Maximum size is 500KB.');
        }

        if (errors.length > 0) {
            showErrorUI(errors.join('<br>'));
            return false;
        }

        clearErrorUI();
        return true;
    }

    function showErrorUI(message) {
        dropZone.classList.add('error');
        const textElement = dropZone.querySelector('.file-upload-text');
        if (textElement) {
            textElement.innerHTML = `<div class="error-message">❌ ${message}</div>`;
        }
        // Hide preview if exists
        if (previewContainer) previewContainer.style.display = 'none';
    }

    function clearErrorUI() {
        dropZone.classList.remove('error');
    }

    // Update label to show selected filename
    function updateFileLabel(filename) {
        const textElement = dropZone.querySelector('.file-upload-text');
        if (textElement) {
            textElement.innerHTML = `<strong>Selected:</strong> ${filename}`;
        }
    }

    // Generate XML Preview
    function generatePreview(file) {
        const reader = new FileReader();

        reader.onload = function (e) {
            const content = e.target.result;

            // Simple regex to find Root element attributes
            // <Root PresetName="MyPreset" MajorVersion="3" MinorVersion="0">
            const presetMatch = content.match(/PresetName="([^"]+)"/);
            const majorMatch = content.match(/MajorVersion="([^"]+)"/);

            let presetName = presetMatch ? presetMatch[1] : 'Custom / Unnamed';
            let version = majorMatch ? majorMatch[1] : '?';

            showPreviewUI(presetName, version);
        };

        reader.onerror = function () {
            console.error("Error reading file");
        };

        reader.readAsText(file); // generated preview depends on text content
    }

    function showPreviewUI(presetName, version) {
        // Create or update preview element if not exists in HTML yet
        let previewEl = document.getElementById('binds-preview');

        if (!previewEl) {
            previewEl = document.createElement('div');
            previewEl.id = 'binds-preview';
            previewEl.className = 'binds-preview fade-in';
            // Insert after dropzone
            dropZone.parentNode.insertBefore(previewEl, dropZone.nextSibling);
        }

        previewEl.innerHTML = `
            <div class="preview-badge">
                <span class="preview-icon">✨</span>
                <div class="preview-info">
                    <span class="preview-title">Preset detected</span>
                    <span class="preview-value">${presetName} (v${version})</span>
                </div>
            </div>
        `;
        previewEl.style.display = 'block';
    }
});
