// Copyright 2025 Enveng Group.
// SPDX-License-Identifier: 	AGPL-3.0-or-later

/**
 * Enhanced Obligation Detail Modal with Inline Editing
 */
(function () {
  'use strict';

  class ObligationModal {
    constructor() {
      this.modal = document.getElementById('obligation-detail-modal');
      this.modalContent = document.getElementById('obligation-modal-content');
      this.modalTitle = document.getElementById('modal-obligation-number');
      this.modalProjectName = document.getElementById('modal-project-name');
      this.modalStatus = document.getElementById('modal-obligation-status');

      // Action buttons
      this.viewModeActions = null;
      this.editModeActions = null;
      this.editBtn = null;
      this.saveBtn = null;
      this.cancelBtn = null;
      this.deleteBtn = null;

      this.currentObligationNumber = null;
      this.isEditMode = false;
      this.hasUnsavedChanges = false;
      this.originalFormData = {};

      this.init();
    }

    init() {
      this.bindEvents();
      this.createBackdrop();
    }

    createBackdrop() {
      if (!this.modal) return;

      const backdrop = this.modal.querySelector('.obligation-detail-backdrop');
      if (backdrop) {
        backdrop.addEventListener('click', () => this.handleClose());
      }
    }

    bindEvents() {
      // Bind modal trigger buttons
      document.addEventListener('click', (e) => {
        if (
          e.target.matches('.modal-trigger') ||
          e.target.closest('.modal-trigger')
        ) {
          e.preventDefault();
          const trigger = e.target.matches('.modal-trigger')
            ? e.target
            : e.target.closest('.modal-trigger');
          const obligationNumber = trigger.dataset.obligationNumber;
          if (obligationNumber) {
            this.open(obligationNumber);
          }
        }
      });

      // Bind close buttons
      if (this.modal) {
        this.modal.addEventListener('click', (e) => {
          if (e.target.matches('.obligation-detail-close')) {
            e.preventDefault();
            this.handleClose();
          }
        });
      }

      // Bind escape key
      document.addEventListener('keydown', (e) => {
        if (
          e.key === 'Escape' &&
          this.modal &&
          this.modal.classList.contains('active')
        ) {
          this.handleClose();
        }
      });
    }

    bindActionButtons() {
      this.viewModeActions = document.getElementById('view-mode-actions');
      this.editModeActions = document.getElementById('edit-mode-actions');
      this.editBtn = document.getElementById('modal-edit-btn');
      this.saveBtn = document.getElementById('modal-save-btn');
      this.cancelBtn = document.getElementById('modal-cancel-btn');
      this.deleteBtn = document.getElementById('modal-delete-btn');

      if (this.editBtn) {
        this.editBtn.addEventListener('click', () => this.enterEditMode());
      }

      if (this.saveBtn) {
        this.saveBtn.addEventListener('click', () => this.saveChanges());
      }

      if (this.cancelBtn) {
        this.cancelBtn.addEventListener('click', () => this.cancelEdit());
      }

      if (this.deleteBtn) {
        this.deleteBtn.addEventListener('click', () => this.handleDelete());
      }
    }

    bindFormChangeTracking() {
      const form = document.getElementById('obligation-edit-form');
      if (!form) return;

      // Store original form data
      this.originalFormData = new FormData(form);

      // Track changes
      form.addEventListener('input', () => {
        this.checkForChanges();
      });

      form.addEventListener('change', () => {
        this.checkForChanges();
      });
    }

    checkForChanges() {
      const form = document.getElementById('obligation-edit-form');
      if (!form) return;

      const currentData = new FormData(form);
      let hasChanges = false;

      // Compare form data
      for (let [key, value] of currentData.entries()) {
        if (this.originalFormData.get(key) !== value) {
          hasChanges = true;
          break;
        }
      }

      this.hasUnsavedChanges = hasChanges;

      if (hasChanges) {
        this.modal.classList.add('has-changes');
      } else {
        this.modal.classList.remove('has-changes');
      }
    }

    async open(obligationNumber) {
      if (!this.modal) return;

      this.currentObligationNumber = obligationNumber;

      // Show modal with loading state
      this.modal.classList.add('active');
      this.modal.removeAttribute('hidden');
      this.showLoading();

      // Focus management
      this.modal.focus();

      try {
        // Fetch obligation details with edit form
        const response = await fetch(
          `/obligations/view/${obligationNumber}/`,
          {
            headers: {
              'X-Requested-With': 'XMLHttpRequest',
              'Content-Type': 'application/json',
            },
          }
        );

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        this.populateModal(data);
        this.bindActionButtons();
        this.bindFormChangeTracking();
      } catch (error) {
        console.error('Error fetching obligation details:', error);
        this.showError('Failed to load obligation details. Please try again.');
      }
    }

    handleClose() {
      if (this.hasUnsavedChanges) {
        const confirmClose = confirm(
          'You have unsaved changes. Are you sure you want to close without saving?'
        );
        if (!confirmClose) return;
      }

      this.close();
    }

    close() {
      if (!this.modal) return;

      this.modal.classList.remove('active', 'edit-mode', 'has-changes');
      this.isEditMode = false;
      this.hasUnsavedChanges = false;

      // Delay hiding to allow animation to complete
      setTimeout(() => {
        this.modal.setAttribute('hidden', '');
        this.currentObligationNumber = null;
      }, 300);
    }

    enterEditMode() {
      this.isEditMode = true;
      this.modal.classList.add('edit-mode');

      // Show edit inputs, hide view values
      const viewElements = this.modal.querySelectorAll('.view-mode');
      const editElements = this.modal.querySelectorAll('.edit-mode');

      viewElements.forEach((el) => (el.style.display = 'none'));
      editElements.forEach((el) => (el.style.display = 'block'));

      // Show edit actions, hide view actions
      if (this.viewModeActions) this.viewModeActions.style.display = 'none';
      if (this.editModeActions) this.editModeActions.style.display = 'flex';

      // Focus first input
      const firstInput = this.modal.querySelector(
        '.edit-mode input, .edit-mode textarea, .edit-mode select'
      );
      if (firstInput) firstInput.focus();
    }

    exitEditMode() {
      this.isEditMode = false;
      this.modal.classList.remove('edit-mode', 'has-changes');
      this.hasUnsavedChanges = false;

      // Show view values, hide edit inputs
      const viewElements = this.modal.querySelectorAll('.view-mode');
      const editElements = this.modal.querySelectorAll('.edit-mode');

      viewElements.forEach((el) => (el.style.display = 'block'));
      editElements.forEach((el) => (el.style.display = 'none'));

      // Show view actions, hide edit actions
      if (this.viewModeActions) this.viewModeActions.style.display = 'flex';
      if (this.editModeActions) this.editModeActions.style.display = 'none';
    }

    cancelEdit() {
      if (this.hasUnsavedChanges) {
        const confirmCancel = confirm(
          'Are you sure you want to cancel? All unsaved changes will be lost.'
        );
        if (!confirmCancel) return;
      }

      // Reset form to original values
      this.resetForm();
      this.exitEditMode();
    }

    resetForm() {
      const form = document.getElementById('obligation-edit-form');
      if (!form || !this.originalFormData) return;

      // Reset all form fields to original values
      for (let [key, value] of this.originalFormData.entries()) {
        const field = form.querySelector(`[name="${key}"]`);
        if (field) {
          if (field.type === 'checkbox') {
            field.checked = value === 'on';
          } else {
            field.value = value;
          }
        }
      }
    }

    async saveChanges() {
      const form = document.getElementById('obligation-edit-form');
      if (!form) return;

      // Show saving state
      if (this.saveBtn) {
        this.saveBtn.classList.add('saving');
        this.saveBtn.textContent = 'Saving...';
        this.saveBtn.disabled = true;
      }

      try {
        const formData = new FormData(form);
        const csrfToken = this.getCSRFToken();

        const response = await fetch(
          `/obligations/update/${this.currentObligationNumber}/`,
          {
            method: 'POST',
            headers: {
              'X-CSRFToken': csrfToken,
              'X-Requested-With': 'XMLHttpRequest',
            },
            body: formData,
          }
        );

        if (response.ok) {
          const data = await response.json();

          if (data.success) {
            // Update view mode with new data
            this.updateViewMode(data.obligation);
            this.exitEditMode();
            this.showSuccessMessage('Obligation updated successfully');
            this.refreshObligationList();
          } else {
            // Show validation errors
            this.showValidationErrors(data.errors);
          }
        } else {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
      } catch (error) {
        console.error('Error saving obligation:', error);
        this.showErrorMessage('Failed to save changes. Please try again.');
      } finally {
        // Reset saving state
        if (this.saveBtn) {
          this.saveBtn.classList.remove('saving');
          this.saveBtn.textContent = 'Save Changes';
          this.saveBtn.disabled = false;
        }
      }
    }

    updateViewMode(obligationData) {
      // Update view elements with new data
      const fields = [
        'environmental_aspect',
        'obligation',
        'procedure',
        'responsibility',
        'action_due_date',
        'close_out_date',
        'general_comments',
        'supporting_information',
        'compliance_comments',
      ];

      fields.forEach((field) => {
        const viewElement = this.modal
          .querySelector(`[name="${field}"]`)
          ?.closest('.detail-value-container')
          ?.querySelector('.view-mode');

        if (viewElement && obligationData[field]) {
          if (field.includes('date')) {
            viewElement.textContent = new Date(
              obligationData[field]
            ).toLocaleDateString();
          } else if (field.includes('comments') || field === 'obligation') {
            viewElement.innerHTML = obligationData[field].replace(
              /\n/g,
              '<br>'
            );
          } else {
            viewElement.textContent = obligationData[field];
          }
        }
      });

      // Update status
      if (this.modalStatus && obligationData.status_display) {
        this.modalStatus.innerHTML = obligationData.status_display;
      }
    }

    showValidationErrors(errors) {
      // Clear existing errors
      this.modal.querySelectorAll('.field-error').forEach((el) => el.remove());

      // Show new errors
      Object.entries(errors).forEach(([field, messages]) => {
        const fieldElement = this.modal.querySelector(`[name="${field}"]`);
        if (fieldElement) {
          fieldElement.classList.add('error');

          const errorElement = document.createElement('span');
          errorElement.className = 'field-error';
          errorElement.textContent = Array.isArray(messages)
            ? messages.join(', ')
            : messages;

          fieldElement.parentNode.appendChild(errorElement);
        }
      });
    }

    showLoading() {
      if (!this.modalContent) return;

      this.modalContent.innerHTML = `
                <div class="obligation-detail-loading">
                    <div class="loading-spinner"></div>
                    <span style="margin-left: 0.5rem;">Loading obligation details...</span>
                </div>
            `;

      // Reset header content
      if (this.modalTitle) this.modalTitle.textContent = 'Loading...';
      if (this.modalProjectName)
        this.modalProjectName.textContent = 'Loading...';
      if (this.modalStatus) this.modalStatus.textContent = 'Loading...';
    }

    showError(message) {
      if (!this.modalContent) return;

      this.modalContent.innerHTML = `
                <div class="error-container" style="text-align: center; padding: 2rem;">
                    <p class="error" style="color: var(--greenova-notif-primary-high, #ff1f1f);">${message}</p>
                    <button type="button" class="btn-modal btn-modal-secondary obligation-detail-close" style="margin-top: 1rem;">
                        Close
                    </button>
                </div>
            `;
    }

    populateModal(data) {
      // Update header
      if (this.modalTitle)
        this.modalTitle.textContent = data.obligation_number || 'Unknown';
      if (this.modalProjectName)
        this.modalProjectName.textContent =
          data.project_name || 'Unknown Project';
      if (this.modalStatus)
        this.modalStatus.innerHTML = data.status_display || 'Unknown';

      // Populate content
      if (this.modalContent && data.content) {
        this.modalContent.innerHTML = data.content;
      }
    }

    async handleDelete() {
      if (!this.currentObligationNumber) return;

      const confirmed = confirm(
        'Are you sure you want to delete this obligation? This action cannot be undone.'
      );

      if (!confirmed) return;

      try {
        const csrfToken = this.getCSRFToken();

        const response = await fetch(
          `/obligations/delete/${this.currentObligationNumber}/`,
          {
            method: 'POST',
            headers: {
              'X-CSRFToken': csrfToken,
              'X-Requested-With': 'XMLHttpRequest',
              'Content-Type': 'application/json',
            },
          }
        );

        if (response.ok) {
          this.close();
          this.refreshObligationList();
          this.showSuccessMessage('Obligation deleted successfully');
        } else {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
      } catch (error) {
        console.error('Error deleting obligation:', error);
        this.showErrorMessage(
          'Failed to delete obligation. Please try again.'
        );
      }
    }

    getCSRFToken() {
      const csrfCookie = document.querySelector('[name=csrfmiddlewaretoken]');
      return csrfCookie ? csrfCookie.value : '';
    }

    refreshObligationList() {
      const container = document.getElementById('obligations-container');
      if (container && typeof htmx !== 'undefined') {
        htmx.trigger(container, 'refresh');
      } else {
        window.location.reload();
      }
    }

    showSuccessMessage(message) {
      this.showMessage(message, 'success');
    }

    showErrorMessage(message) {
      this.showMessage(message, 'error');
    }

    showMessage(message, type) {
      const messageEl = document.createElement('div');
      messageEl.className = `alert ${type}`;
      messageEl.style.position = 'fixed';
      messageEl.style.top = '20px';
      messageEl.style.right = '20px';
      messageEl.style.zIndex = '1002';
      messageEl.style.padding = '1rem 2rem';
      messageEl.style.borderRadius = '0.5rem';
      messageEl.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';

      if (type === 'success') {
        messageEl.style.background =
          'var(--greenova-success-background, #e3f9dd)';
        messageEl.style.color = 'var(--greenova-success-text, #0d5613)';
      } else {
        messageEl.style.background =
          'var(--greenova-error-background, #ffeaea)';
        messageEl.style.color = 'var(--greenova-error-text, #721c24)';
      }

      messageEl.textContent = message;
      document.body.appendChild(messageEl);

      setTimeout(() => {
        messageEl.remove();
      }, 3000);
    }
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      new ObligationModal();
    });
  } else {
    new ObligationModal();
  }
})();
