/**
 * SQL Injection Demo - Main JavaScript
 * This file contains common functionality for the SQL Injection demonstration
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Highlight code blocks
    const preElements = document.querySelectorAll('pre');
    preElements.forEach(pre => {
        pre.classList.add('bg-dark', 'text-light', 'p-3', 'rounded');
    });
    
    // Function to escape HTML entities
    window.escapeHtml = function(unsafe) {
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    };
    
    // Visual feedback for copy buttons
    document.body.addEventListener('click', function(e) {
        const copyButton = e.target.closest('.copy-example');
        if (copyButton) {
            const originalText = copyButton.textContent.trim();
            copyButton.textContent = 'Copied!';
            copyButton.classList.add('btn-success');
            copyButton.classList.remove('btn-outline-secondary');
            
            setTimeout(() => {
                copyButton.textContent = originalText;
                copyButton.classList.remove('btn-success');
                copyButton.classList.add('btn-outline-secondary');
            }, 1500);
        }
    });
    
    // Handle form submission with Enter key
    const formInputs = document.querySelectorAll('form input');
    formInputs.forEach(input => {
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                const form = this.closest('form');
                const submitBtn = form.querySelector('button[type="submit"]');
                if (submitBtn) {
                    submitBtn.click();
                }
            }
        });
    });
});
