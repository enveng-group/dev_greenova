// This script checks HTMX/JS logic for dynamic updates in the Greenova project.

// Function to validate HTMX attributes on elements
function validateHTMXAttributes() {
    const elements = document.querySelectorAll('[hx-get], [hx-post], [hx-target]');

    elements.forEach((element) => {
        if (!element.hasAttribute('hx-target')) {
            console.warn('Missing hx-target attribute:', element);
        }

        if (element.hasAttribute('hx-get') && !element.getAttribute('hx-get')) {
            console.warn('Empty hx-get attribute:', element);
        }

        if (element.hasAttribute('hx-vals')) {
            try {
                JSON.parse(element.getAttribute('hx-vals'));
            } catch (e) {
                console.error('Invalid JSON in hx-vals attribute:', element);
            }
        }
    });
}

// Function to confirm response fragments include filtered/sorted results
function validateResponseFragments(response) {
    const parser = new DOMParser();
    const doc = parser.parseFromString(response, 'text/html');

    const filteredResults = doc.querySelectorAll('.filtered-result');
    if (filteredResults.length === 0) {
        console.error('No filtered/sorted results found in the response fragment.');
    } else {
        console.log('Filtered/sorted results validated successfully.');
    }
}

// Example usage
// Call validateHTMXAttributes on page load or after dynamic updates
validateHTMXAttributes();

// Simulate a response fragment validation (replace with actual AJAX response)
const exampleResponse = '<div class="filtered-result">Example Result</div>';
validateResponseFragments(exampleResponse);
