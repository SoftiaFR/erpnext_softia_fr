function initializeLogoReplacement() {
    const customLogo = '/assets/erpnext_softia_fr/images/ERPNext_By_Softia_logo.png';
    
    function replaceLogos() {
        // Use more specific selectors
        const selectors = [
            '.navbar-brand img',
            '.login-content .app-logo img', 
            '.sidebar-brand img',
            '.page-head .logo img'
        ];
        
        selectors.forEach(selector => {
            const elements = document.querySelectorAll(selector);
            elements.forEach(element => {
                element.src = customLogo;
                element.style.maxHeight = '80px';
                element.style.width = 'auto';
                element.style.objectFit = 'contain';
            });
        });
    }
    
    // Try immediately
    replaceLogos();
    
    // Set up observers and retries
    setupLogoMonitoring(replaceLogos);
    
    // Update PDF logo when Frappe is ready
    waitForFrappe().then(() => {
        updatePdfLogo(customLogo);
    });
}

function setupLogoMonitoring(replaceFunction) {
    // MutationObserver for dynamic content
    const observer = new MutationObserver(function(mutations) {
        let shouldReplace = false;
        mutations.forEach(mutation => {
            if (mutation.addedNodes.length) {
                shouldReplace = true;
            }
        });
        if (shouldReplace) {
            replaceFunction();
        }
    });
    
    observer.observe(document.body, { childList: true, subtree: true });
    
    // Periodic checks for first 10 seconds
    const interval = setInterval(replaceFunction, 1000);
    setTimeout(() => clearInterval(interval), 10000);
}

function waitForFrappe() {
    return new Promise((resolve) => {
        function checkFrappe() {
            if (typeof frappe !== 'undefined' && frappe.db && frappe.call) {
                resolve();
            } else {
                setTimeout(checkFrappe, 100);
            }
        }
        checkFrappe();
    });
}

function updatePdfLogo(customLogo) {
    frappe.db.get_value('Print Settings', 'Print Settings', 'logo')
    .then(r => {
        if (r.message && !r.message.logo) {
            return frappe.call({
                method: 'frappe.client.set_value',
                args: {
                    doctype: 'Print Settings',
                    name: 'Print Settings',
                    fieldname: 'logo',
                    value: customLogo
                }
            });
        }
    })
    .catch(err => {
        console.warn('Could not update PDF logo:', err);
    });
}

// Start everything when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeLogoReplacement);
} else {
    initializeLogoReplacement();
}