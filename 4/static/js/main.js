// Main JavaScript file for Gemini Project

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize notification system
    initNotifications();

    // Initialize form validation
    initFormValidation();

    // Initialize any interactive elements
    initInteractiveElements();
});

// Notification System
function initNotifications() {
    // Function to show notification
    window.showNotification = function(message, type = 'error') {
        const notificationElement = document.getElementById('notification');

        if (!notificationElement) return;

        notificationElement.textContent = message;
        notificationElement.className = 'notification';

        if (type === 'success') {
            notificationElement.classList.add('success');
        }

        notificationElement.style.display = 'block';

        // Auto-hide notification after 5 seconds
        setTimeout(() => {
            notificationElement.style.display = 'none';
        }, 5000);
    };
}

// Form Validation
function initFormValidation() {
    // Get all forms
    const forms = document.querySelectorAll('form');

    // Add validation to each form
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            // Check if form is valid
            if (!validateForm(form)) {
                event.preventDefault();
                return false;
            }
        });
    });
}

// Validate individual form
function validateForm(form) {
    let isValid = true;
    const inputs = form.querySelectorAll('input[required]');

    inputs.forEach(input => {
        if (!input.value.trim()) {
            showFieldError(input, 'This field is required');
            isValid = false;
        } else {
            clearFieldError(input);

            // Validate email format
            if (input.type === 'email' && !isValidEmail(input.value)) {
                showFieldError(input, 'Please enter a valid email address');
                isValid = false;
            }

            // Validate password length
            if (input.id === 'password' && input.value.length < 8) {
                showFieldError(input, 'Password must be at least 8 characters long');
                isValid = false;
            }

            // Validate password confirmation
            if (input.id === 'confirm-password') {
                const password = document.getElementById('new-password');
                if (password && input.value !== password.value) {
                    showFieldError(input, 'Passwords do not match');
                    isValid = false;
                }
            }
        }
    });

    return isValid;
}

// Show field error
function showFieldError(input, message) {
    // Remove any existing error
    clearFieldError(input);

    // Create error element
    const errorElement = document.createElement('div');
    errorElement.className = 'field-error';
    errorElement.textContent = message;
    errorElement.style.color = '#e74c3c';
    errorElement.style.fontSize = '0.85rem';
    errorElement.style.marginTop = '0.5rem';

    // Insert error after input
    input.parentNode.insertBefore(errorElement, input.nextSibling);

    // Add error styling to input
    input.style.borderColor = '#e74c3c';
}

// Clear field error
function clearFieldError(input) {
    const errorElement = input.parentNode.querySelector('.field-error');
    if (errorElement) {
        errorElement.remove();
    }
    input.style.borderColor = '';
}

// Check if email is valid
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Initialize interactive elements
function initInteractiveElements() {
    // Initialize any tooltips
    initTooltips();

    // Initialize any modals
    initModals();

    // Initialize any confirmations for dangerous actions
    initDangerConfirmations();
}

// Initialize tooltips
function initTooltips() {
    // Find all elements with tooltip attributes
    const tooltipElements = document.querySelectorAll('[data-tooltip]');

    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            showTooltip(this);
        });

        element.addEventListener('mouseleave', function() {
            hideTooltip(this);
        });
    });
}

// Show tooltip
function showTooltip(element) {
    const tooltipText = element.getAttribute('data-tooltip');
    if (!tooltipText) return;

    // Create tooltip element
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.textContent = tooltipText;

    // Style tooltip
    tooltip.style.position = 'absolute';
    tooltip.style.backgroundColor = '#333';
    tooltip.style.color = 'white';
    tooltip.style.padding = '0.5rem';
    tooltip.style.borderRadius = '4px';
    tooltip.style.fontSize = '0.8rem';
    tooltip.style.zIndex = '1000';
    tooltip.style.maxWidth = '200px';

    // Position tooltip
    const rect = element.getBoundingClientRect();
    tooltip.style.left = `${rect.left + window.scrollX}px`;
    tooltip.style.top = `${rect.top + window.scrollY - 30}px`;

    // Add to DOM
    document.body.appendChild(tooltip);

    // Store reference on element
    element.tooltipElement = tooltip;
}

// Hide tooltip
function hideTooltip(element) {
    if (element.tooltipElement) {
        element.tooltipElement.remove();
        element.tooltipElement = null;
    }
}

// Initialize modals
function initModals() {
    // Find all modal triggers
    const modalTriggers = document.querySelectorAll('[data-modal-trigger]');

    modalTriggers.forEach(trigger => {
        trigger.addEventListener('click', function() {
            const modalId = this.getAttribute('data-modal-trigger');
            openModal(modalId);
        });
    });

    // Find all modal close buttons
    const modalCloseButtons = document.querySelectorAll('[data-modal-close]');

    modalCloseButtons.forEach(button => {
        button.addEventListener('click', function() {
            const modal = this.closest('.modal');
            closeModal(modal.id);
        });
    });

    // Close modal on background click
    document.addEventListener('click', function(event) {
        if (event.target.classList.contains('modal')) {
            closeModal(event.target.id);
        }
    });
}

// Open modal
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (!modal) return;

    modal.style.display = 'flex';
    modal.style.position = 'fixed';
    modal.style.top = '0';
    modal.style.left = '0';
    modal.style.width = '100%';
    modal.style.height = '100%';
    modal.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
    modal.style.zIndex = '1000';
    modal.style.justifyContent = 'center';
    modal.style.alignItems = 'center';

    // Prevent body scroll
    document.body.style.overflow = 'hidden';
}

// Close modal
function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (!modal) return;

    modal.style.display = 'none';

    // Restore body scroll
    document.body.style.overflow = '';
}

// Initialize dangerous action confirmations
function initDangerConfirmations() {
    // Find all dangerous action buttons
    const dangerButtons = document.querySelectorAll('[data-danger-action]');

    dangerButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            const action = this.getAttribute('data-danger-action');
            const confirmation = this.getAttribute('data-confirmation') || 
                                `Are you sure you want to ${action}?`;

            if (!confirm(confirmation)) {
                event.preventDefault();
                return false;
            }
        });
    });
}
