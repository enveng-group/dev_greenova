# Greenova Project TODO

This document tracks tasks and action items for the Greenova environmental
management application.

## Todo.txt Format Task List

```txt
(A) 2024-05-21 Charts and obligations list back online +Frontend
(A) 2024-05-22 Add obligation conditionally to projects with CRUD testing +Backend
(A) 2024-05-23 Implement detailed view +Frontend
(A) 2024-05-24 Create login page with customer/admin endpoint choice +Frontend @auth
(A) 2024-05-27 Implement user profile functionality +Frontend @auth
(A) 2024-05-28 Develop company features +Frontend
(A) 2024-05-29 Add reset password functionality +Frontend @auth
(A) 2024-05-30 Create registration flow +Frontend @auth
(B) Organize CSS files for better readability and maintainability +Frontend @css
(B) Optimize CSS for performance +Frontend @css
(B) Enhance responsiveness and cross-browser compatibility +Frontend @css
(B) Implement PostCSS or Sass for enhanced functionality +Frontend @css
(B) Set up TypeScript development environment +Frontend @js
(B) Set up AssemblyScript development environment +Frontend @js
(B) Identify performance-critical sections in app.js +Frontend @js
(B) Write TypeScript code for DOM manipulation and event handling +Frontend @js
(B) Write AssemblyScript code for performance-critical parts +Frontend @js
(B) Compile AssemblyScript to WebAssembly +Frontend @js
(B) Integrate WebAssembly modules with TypeScript +Frontend @js
(B) Update build and deployment process +DevOps @js
(C) Implement stylelint for CSS linting +DevOps @linting
(C) Setup Django testing framework +Backend @testing
(C) Configure hadolint for Dockerfile linting +DevOps @linting
(C) Create Docker architecture diagram +Documentation @docker
(C) Create Docker workflow diagram +Documentation @docker
(C) Create Docker environment diagram +Documentation @docker
x Setup djlint +DevOps @linting
x Configure prettier +DevOps @linting
x Install autopep8 +DevOps @linting
x Setup pylance +DevOps @linting
x Configure eslint +DevOps @linting
```

## Technology Integration Tasks

### Frontend Tools & Libraries

- [ ] Implement SASS/PostCSS for advanced styling
- [ ] Set up TypeScript with proper configuration
- [ ] Configure AssemblyScript for WASM components
- [ ] Improve mechanism charts interactivity
- [ ] Implement detailed chart view

### Authentication & User Management

- [ ] `django-allauth[MFA]`
- [ ] `django-allauth[user-sessions]`
- [ ] Reset password functionality
- [ ] Registration flow

### DevOps & Infrastructure

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
