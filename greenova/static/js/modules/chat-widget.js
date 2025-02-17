export class ChatWidget {
    constructor() {
        this.messages = [];
        this.dialog = document.querySelector('#chat-dialog');
        this.messagesContainer = document.querySelector('#chat-messages');
        this.form = document.querySelector('#chat-form');
        this.input = document.querySelector('#message-input');
        this.template = document.querySelector('#message-template');
        this.context = {
            currentPage: document.body.dataset.page || 'unknown',
            recentTopics: [],
            lastInteraction: null
        };
        
        this.initialize();
    }

    initialize() {
        // Add contextual welcome message
        const welcomeMessage = this.getContextualWelcome();
        this.addMessage('bot', welcomeMessage);
        
        // Setup event listeners
        document.querySelector('#chat-toggle')?.addEventListener('click', () => {
            if (this.dialog.open) {
                this.dialog.close();
            } else {
                this.dialog.showModal();
            }
        });

        this.dialog?.addEventListener('click', (e) => {
            if (e.target === this.dialog) {
                this.dialog.close();
            }
        });

        document.querySelector('.close-button')?.addEventListener('click', () => {
            this.dialog.close();
        });

        this.form?.addEventListener('submit', (e) => {
            e.preventDefault();
            const message = this.input.value.trim();
            if (message) {
                this.handleUserMessage(message);
                this.input.value = '';
            }
        });
    }

    getContextualWelcome() {
        const pageMessages = {
            'dashboard': '👋 Welcome to the Dashboard! I can help you understand your metrics and navigate projects.',
            'projects': '👋 Looking to manage your projects? I can help you with creating, updating, or viewing project details.',
            'charts': '👋 Need help understanding the charts? I can explain what each visualization means.',
            'default': '👋 Hi! How can I help you navigate Greenova?'
        };
        return pageMessages[this.context.currentPage] || pageMessages.default;
    }

    addMessage(type, text) {
        const message = { type, text, id: Date.now() };
        this.messages.push(message);
        this.renderMessage(message);
        this.scrollToBottom();
    }

    renderMessage(message) {
        const node = this.template.content.cloneNode(true);
        const messageDiv = node.querySelector('.message');
        messageDiv.classList.add(message.type);
        messageDiv.querySelector('p').textContent = message.text;
        this.messagesContainer.appendChild(messageDiv);
    }

    scrollToBottom() {
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }

    handleUserMessage(message) {
        this.addMessage('user', message);
        
        // Update context
        this.context.lastInteraction = Date.now();
        this.context.recentTopics.unshift(message.toLowerCase());
        if (this.context.recentTopics.length > 3) {
            this.context.recentTopics.pop();
        }

        // Get contextual response
        const response = this.getContextualResponse(message);
        setTimeout(() => this.addMessage('bot', response), 500);
    }

    getContextualResponse(message) {
        const normalizedMessage = message.toLowerCase();
        
        // Context-aware responses
        const contextResponses = {
            dashboard: {
                'metrics': 'Your dashboard shows key metrics like obligation status and upcoming deadlines. The charts update in real-time.',
                'overview': 'The dashboard gives you a quick overview of your projects and obligations. Need help with anything specific?',
                'refresh': 'Data refreshes automatically every few minutes. You can also manually refresh using the reload button.',
                'help': 'On the dashboard, you can: \n1. View project metrics\n2. Check upcoming deadlines\n3. Access recent obligations'
            },
            projects: {
                'create': 'To create a new project, click the "New Project" button in the top right corner.',
                'edit': 'You can edit project details by clicking the edit icon next to any project.',
                'delete': 'To delete a project, first archive it, then use the delete option in project settings.',
                'help': 'In the projects section, you can: \n1. Create new projects\n2. Edit existing ones\n3. View project details'
            },
            charts: {
                'explain': 'The charts show your obligation status and progress. Green indicates completed, yellow for in-progress.',
                'download': 'You can download chart data by clicking the three dots menu in the top right of any chart.',
                'help': 'For charts, you can: \n1. View different metrics\n2. Download data\n3. Filter by date range'
            }
        };

        // Check if we have context-specific responses
        const pageResponses = contextResponses[this.context.currentPage] || {};
        
        // Basic responses for common queries
        const basicResponses = {
            'help': 'I can help you with:\n- Navigation\n- Understanding data\n- Managing projects\n- Viewing charts\nWhat would you like to know?',
            'hello': 'Hello! What can I help you with today?',
            'hi': 'Hi there! Need help with anything?',
            'bye': 'Goodbye! Let me know if you need anything else.',
            'thanks': 'You\'re welcome! Is there anything else you need help with?'
        };

        // Try to match context-specific response first
        if (pageResponses[normalizedMessage]) {
            return pageResponses[normalizedMessage];
        }

        // Check basic responses
        if (basicResponses[normalizedMessage]) {
            return basicResponses[normalizedMessage];
        }

        // Fallback with context hint
        return `I can help you navigate ${this.context.currentPage || 'Greenova'}. Try asking about: ${Object.keys(pageResponses).join(', ')}`;
    }
}