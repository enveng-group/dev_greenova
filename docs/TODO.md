# Greenova Project TODO

This document tracks tasks and action items for the Greenova environmental
management application.

## Completed Tasks

The following tasks have been completed and moved to `done.txt`:

- Charts and obligations list back online
- Add obligation conditionally to projects with CRUD testing
- Implement detailed view
- Create login page with customer/admin endpoint choice
- Implement user profile functionality
- Develop company features
- Implement stylelint for CSS linting

## Technology Integration Tasks

### Frontend Tools & Libraries

- [ ] Organize CSS files for better readability and maintainability
- [ ] Optimize CSS for performance
- [ ] Enhance responsiveness and cross-browser compatibility
- [ ] Implement PostCSS or Sass for advanced styling
- [ ] Set up TypeScript development environment
- [ ] Set up AssemblyScript development environment
- [ ] Identify performance-critical sections in app.js
- [ ] Write TypeScript code for DOM manipulation and event handling
- [ ] Write AssemblyScript code for performance-critical parts
- [ ] Compile AssemblyScript to WebAssembly
- [ ] Integrate WebAssembly modules with TypeScript
- [ ] Improve mechanism charts interactivity
- [ ] Implement detailed chart view

### Authentication & User Management

- [ ] Add reset password functionality
- [ ] Create registration flow
- [ ] `django-allauth[MFA]`
- [ ] `django-allauth[user-sessions]`

### DevOps & Infrastructure

- [ ] Integrate commitlint into devtool stack
- [ ] Integrate Dive for optimizing Docker/OCI image size
- [ ] Introduce cloudflared for tunnel
- [ ] certbot let's encrypt SSL setup
- [ ] Configure MySQL or PostgreSQL in devcontainer
- [ ] Set up Caddy with devcontainer feature
- [ ] Configure cloudflared devcontainer feature
- [ ] Evaluate DoltDB integration
- [ ] Set up django-channels
- [ ] Configure daphne as web server
- [ ] Implement websockets
- [ ] Configure proper direnv setup
- [ ] Set up gh-cli properly

### Code Quality & CI/CD

- [ ] Configure pre-commit hooks
- [ ] Set up GPG commit signing
- [ ] Better integration of git-crypt and git-lfs
- [ ] Create Makefile for common development tasks
- [ ] Add `npx dotenv-vault@latest pull` to post_create.sh

### Documentation & Architecture

- [ ] Modularize base.html template
- [ ] Document HTML-first design principles
- [ ] Create architecture diagrams for Docker setup

### Migrate Templates from DTL to Jinja2

- [ ] Authentication
- [ ] Chatbot
- [ ] Company
- [ ] Core
- [x] Dashboard
- [x] Feedback
- [ ] Landing
- [ ] Mechanisms
- [ ] Obligations
- [x] Procedures
- [ ] Projects
- [ ] Responsibility
- [ ] Templates
- [ ] Users

## References

- [djlint](https://djlint.com/)
- [stylelint](https://stylelint.io/)
- [prettier](https://prettier.io/)
- [autopep8](https://pypi.org/project/autopep8/)
- [Django Testing](https://docs.djangoproject.com/en/4.2/topics/testing/overview/)
- [pylance](https://github.com/microsoft/pylance)
- [hadolint](https://github.com/hadolint/hadolint)
- [eslint](https://eslint.org/)
- [setuptools](https://setuptools.pypa.io/en/latest/index.html)
- [pre-commit](https://pre-commit.com)
- [pre-commit hooks](https://pre-commit.com/hooks.html)
