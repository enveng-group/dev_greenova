document.addEventListener('htmx:responseError', function (evt) {
  const errorBoundary = document.getElementById('error-boundary');
  const errorMessage = document.getElementById('error-message');

  if (errorBoundary && errorMessage) {
    // Try to extract meaningful error message
    let message = 'An error occurred while processing your request.';

    if (evt.detail.xhr.status === 403) {
      message = "You don't have permission to access this resource.";
    } else if (evt.detail.xhr.status === 404) {
      message = 'The requested resource could not be found.';
    } else if (evt.detail.xhr.status === 500) {
      message = 'A server error occurred. Please try again later.';
    }

    // Set message and show error boundary
    errorMessage.textContent = message;
    errorBoundary.classList.remove('hidden');
  }
});
