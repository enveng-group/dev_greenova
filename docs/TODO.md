# TODO


profile
company

### Action Items and Context


### Action Items for CSS Improvements

Implementing PostCSS or Sass can indeed provide significant improvements in your CSS workflow, including better maintainability, enhanced functionality, and performance optimizations. Here are the updated action items incorporating PostCSS and Sass:

### Updated Action Items for CSS Improvements

1. **Organize CSS Files for Better Readability and Maintainability**
   - **Context**: The current CSS files are imported in a structured manner, but there can be improvements in organizing and commenting the CSS for better readability.
   - **Implementation**:
     - Group related styles together and add section comments.
     - Use meaningful and consistent naming conventions for classes and IDs.
     - Example:
       ```css
       /* Base Styles */
       @import url('base.css');

       /* Vendor Styles */
       @import url('vendor/pico-classless.min.css');

       /* Design Variables */
       @import url('defines/design.css');
       @import url('defines/colours.css');

       /* Theme Colors */
       @import url('themes/light.css');
       @import url('themes/dark.css');

       /* Component Styles */
       @import url('components/navigation.css');
       @import url('components/breadcrumbs.css');
       @import url('components/button.css');
       @import url('components/card.css');
       @import url('components/charts.css');
       @import url('components/chat.css');
       @import url('components/form.css');
       @import url('components/list.css');
       @import url('components/filter.css');
       @import url('components/pagination.css');
       @import url('components/obligations.css');
       @import url('components/user-profile.css');
       @import url('components/company.css');
       ```

2. **Optimize CSS for Performance**
   - **Context**: Ensure the CSS is optimized to reduce loading times and improve rendering performance.
   - **Implementation**:
     - Minify CSS files to reduce file size.
     - Remove unused CSS rules and classes.
     - Use CSS variables for repeated values to reduce redundancy.
     - Example:
       ```css
       /* Example of using CSS variables */
       :root {
         --primary-color: #1095c1;
         --secondary-color: #08769b;
         --font-family: 'Segoe UI', system-ui, sans-serif;
       }

       body {
         font-family: var(--font-family);
         color: var(--primary-color);
       }

       .button {
         background-color: var(--secondary-color);
       }
       ```

3. **Enhance Responsiveness and Cross-Browser Compatibility**
   - **Context**: Ensure the application looks and functions well on various devices and browsers.
   - **Implementation**:
     - Use media queries to create responsive designs.
     - Test and fix cross-browser compatibility issues.
     - Ensure that the CSS adheres to modern standards and best practices.
     - Example:
       ```css
       /* Responsive design using media queries */
       @media (max-width: 768px) {
         .navigation {
           flex-direction: column;
         }

         .card {
           width: 100%;
         }
       }
       ```

5. **Implement PostCSS or Sass for Enhanced Functionality**
   - **Context**: Using PostCSS or Sass can provide advanced features like mixins, nesting, and autoprefixing that improve the development workflow.
   - **Implementation**:
     - **PostCSS**:
       - Set up PostCSS with plugins like `autoprefixer` for adding vendor prefixes automatically and `cssnano` for minification.
       - Example:
         ```javascript
         // postcss.config.js
         module.exports = {
           plugins: {
             autoprefixer: {},
             cssnano: {}
           }
         };
         ```
     - **Sass**:
       - Use Sass to write more maintainable and modular CSS with features like variables, nesting, and mixins.
       - Example:
         ```scss
         // styles.scss
         $primary-color: #1095c1;
         $secondary-color: #08769b;

         body {
           font-family: 'Segoe UI', system-ui, sans-serif;
           color: $primary-color;
         }

         .button {
           background-color: $secondary-color;
         }
         ```

### Summary of Improvements:

- **Organize and Comment**: Improve the structure and readability of CSS files.
- **Optimize Performance**: Minify, remove unused CSS, and use CSS variables.
- **Enhance Responsiveness**: Use media queries for responsive design and test for cross-browser compatibility.
- **Leverage Frameworks**: Utilize PicoCSS features and integrate Tailwind CSS for enhanced styling.
- **Implement PostCSS or Sass**: Use PostCSS or Sass for advanced CSS features and improved maintainability.

Implementing these action items will help make the CSS styling of the web application more efficient, maintainable, and visually appealing, providing a better user experience.


### Action Items for Replacing `app.js` with TypeScript and AssemblyScript Implementation

Replacing `app.js` with a combination of TypeScript and AssemblyScript can enhance type safety, maintainability, and performance. Here are the detailed action items to achieve this:

1. **Set Up TypeScript Development Environment**
   - **Context**: Install TypeScript and configure the project for TypeScript development.
   - **Implementation**:
     - Install TypeScript and necessary type definitions.
     - Create a `tsconfig.json` file for configuring TypeScript compilation.
     - Example:
       ```bash
       npm install --save-dev typescript @types/node
       ```
       ```json
       // tsconfig.json
       {
         "compilerOptions": {
           "target": "ES2015",
           "module": "ES2015",
           "moduleResolution": "node",
           "esModuleInterop": true,
           "strict": true,
           "outDir": "./greenova/static/js/dist",
           "rootDir": "./typescript",
           "sourceMap": true,
           "declaration": false,
           "baseUrl": "./",
           "paths": {
             "@core/*": ["typescript/core/*"],
             "@components/*": ["typescript/components/*"],
             "@features/*": ["typescript/features/*"],
             "@lib/*": ["typescript/lib/*"]
           }
         },
         "include": ["typescript/**/*.ts"],
         "exclude": ["node_modules"]
       }
       ```

2. **Set Up AssemblyScript Development Environment**
   - **Context**: Install AssemblyScript and configure the project for AssemblyScript development.
   - **Implementation**:
     - Install AssemblyScript and initialize the project.
     - Example:
       ```bash
       npm install --save-dev assemblyscript
       npx asinit .
       ```

3. **Identify Performance-Critical Sections in `app.js`**
   - **Context**: Determine which parts of the `app.js` code could benefit from being rewritten in AssemblyScript.
   - **Implementation**:
     - Review the existing JavaScript code to identify performance bottlenecks or CPU-intensive tasks.
     - Example areas: Complex calculations, data processing, etc.

4. **Write TypeScript Code for DOM Manipulation and Event Handling**
   - **Context**: Rewrite the DOM manipulation and event handling parts of `app.js` in TypeScript.
   - **Implementation**:
     - Create TypeScript files (`.ts`) for the identified sections.
     - Example:
       ```typescript
       // scrollCharts.ts
       export function scrollCharts(direction: string) {
         const container = document.getElementById('chartScroll');
         if (!container) return;

         const scrollAmount = 320;
         container.scrollBy({
           left: direction === 'left' ? -scrollAmount : scrollAmount,
           behavior: 'smooth'
         });
       }
       ```

5. **Write AssemblyScript Code for Performance-Critical Parts**
   - **Context**: Write the identified performance-critical parts in AssemblyScript.
   - **Implementation**:
     - Create AssemblyScript files (`.ts`) with the necessary logic.
     - Example:
       ```typescript
       // add.ts
       export function add(a: i32, b: i32): i32 {
         return a + b;
       }
       ```

6. **Compile AssemblyScript to WebAssembly**
   - **Context**: Compile the AssemblyScript code to WebAssembly to be used in your web application.
   - **Implementation**:
     - Compile the AssemblyScript code using the AssemblyScript compiler.
     - Example:
       ```bash
       npx asc add.ts --outFile add.wasm --optimize
       ```

7. **Integrate WebAssembly Modules with TypeScript**
   - **Context**: Load and use the compiled WebAssembly modules in your TypeScript code.
   - **Implementation**:
     - Use TypeScript to fetch and instantiate the WebAssembly modules.
     - Example:
       ```typescript
       // wasmIntegration.ts
       async function loadWasm() {
         const response = await fetch('add.wasm');
         const buffer = await response.arrayBuffer();
         const module = await WebAssembly.instantiate(buffer);
         const add = module.instance.exports.add as (a: number, b: number) => number;
         console.log(add(2, 3)); // Output: 5
       }
       loadWasm();
       ```

8. **Update Build and Deployment Process**
   - **Context**: Ensure the build and deployment process includes the compilation of TypeScript and AssemblyScript to WebAssembly and the integration with JavaScript.
   - **Implementation**:
     - Add scripts to the build process to compile TypeScript and AssemblyScript code and place the WebAssembly files in the appropriate directories.
     - Example:
       ```json
       // package.json
       {
         "scripts": {
           "build:as": "npx asc add.ts --outFile greenova/static/js/dist/add.wasm --optimize",
           "build:ts": "tsc",
           "build": "npm run build:as && npm run build:ts",
           "watch:ts": "tsc --watch",
           "watch:as": "npx asc add.ts --outFile greenova/static/js/dist/add.wasm --optimize --watch",
           "watch": "npm run watch:as & npm run watch:ts"
         }
       }
       ```

### Summary of Improvements:

- **Set Up TypeScript**: Install and configure TypeScript for development.
- **Set Up AssemblyScript**: Install and configure AssemblyScript for development.
- **Identify Performance-Critical Sections**: Determine which parts of the code to replace with AssemblyScript.
- **Rewrite DOM Manipulation in TypeScript**: Use TypeScript for DOM manipulation and event handling.
- **Write AssemblyScript for Performance-Critical Parts**: Use AssemblyScript for intensive computations.
- **Compile and Integrate WebAssembly**: Compile AssemblyScript to WebAssembly and integrate it with TypeScript.
- **Update Build Process**: Ensure the build process includes TypeScript and AssemblyScript compilation.

This structured approach will help in gradually transitioning the `app.js` functionalities to a more maintainable and high-performance implementation using TypeScript and AssemblyScript.

detailed chart view
reset password
register
interactivity of the mechanism charts
html first by design principles, python and django first, html second picoclasscss third, custom plain css fourth, hyperscript fifth, htmx sixth, native web apis seventh, plain javascript eighth

Tuesday - charts and obligations list back online
Wednesday - add obligation conditionally to projects and tested with CRUD
Thursday - detailed view
Friday - login page with customer or admin endpoint choice
Monday - profile
Tuesday - company
Wednesday - reset password
Thursday - register

https://djlint.com/ - DONE
https://stylelint.io/
https://prettier.io/ - DONE
https://pypi.org/project/autopep8/ - DONE
https://docs.djangoproject.com/en/4.2/topics/testing/overview/
https://github.com/microsoft/pylance - DONE
https://github.com/hadolint/hadolint
https://eslint.org/ - DONE
https://setuptools.pypa.io/en/latest/index.html


### Written Plan

1. **Project Overview**:
   - Define the purpose and scope of your Docker project.
   - List the main components and services that will be containerized.

2. **Technical Requirements**:
   - Specify the software and hardware requirements.
   - Detail the dependencies and configurations needed for each service.

3. **Dockerfile and Docker Compose**:
   - Create a `Dockerfile` for each service to define how the Docker image should be built.
   - Use `docker-compose.yml` to manage multi-container Docker applications.

4. **Build and Deployment Process**:
   - Outline the steps for building Docker images and running containers.
   - Include commands and scripts for automation (e.g., `build.sh`, `run.sh`).

5. **Testing and Validation**:
   - Describe the testing strategy for your Docker containers.
   - Include any tools or frameworks used for testing.

### Visual Plan

1. **Architecture Diagram**:
   - Create a visual representation of your application's architecture.
   - Show how different services interact within containers.

2. **Workflow Diagram**:
   - Illustrate the build and deployment workflow.
   - Include steps from code commit to running containers in production.

3. **Environment Diagram**:
   - Map out the different environments (development, staging, production).
   - Show how containers are deployed and managed in each environment.


- django-allauth[MFA]
- django-allauth[user-sessions]
- [certbot let's encrypt](https://medium.com/@samson_sham/setup-lets-encrypt-https-server-fa54abff688)
- [Typescript](https://www.webdevtutor.net/blog/typescript-and-django)
- [Arial](https://learn.microsoft.com/en-us/typography/font-list/arial)
- [DoltDB](https://www.dolthub.com/blog/2024-01-31-dolt-django/)
- [lit](https://lit.dev)
- [SASS](https://sass-lang.com)
- [PostCSS](https://postcss.org)
- [Pyodide](https://pyodide.org/en/stable/index.html)
- [pre-commit](https://pre-commit.com)

mysql
caddy
https://pypi.org/project/doltpy/
django-channels
web server: daphne
websockets
forward-proxy: mitmproxy
reverse-proxy: proxy.py
load-balancing- pyloadbalancer
DDOD protection - https://github.com/nky001/ddos
SSL termination - pyOpenSSL and certbot and certbot-django
pythsonstartup
fish.config
devcontainer.json to use final base image for smallest possivle image
assemblyscript
dotfiles improve, put necessary config stuff in dotfiles and then let setup.sh apply to container
gpg commit signing
github projects
github copilot prompts
proper direnv setup
proper gh-cli setup
better use of git-crypt and git-lfs
add `npx dotenv-vault@latest pull` to `post_create.sh` in `.devcontainer/` directory
MOdularise base.html
combine and collate numerous commmands into makefile to automate the setup development environment process
