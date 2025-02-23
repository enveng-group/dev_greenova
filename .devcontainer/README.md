# Development Container Configuration Guide

## Core Configuration Files

### `.devcontainer/devcontainer.json`
Primary configuration file that defines the dev container environment settings including:
- Docker image configuration
- Features to install
- Environment settings
- Development settings

### `.devcontainer/Dockerfile` 
Defines custom container image with:
- Base image specification
- Software installation steps
- Environment configuration

### `.devcontainer/docker-compose.yml`
Used for multi-container setups:
- Service definitions
- Network configuration
- Volume mounting

### `.devcontainer/Makefile`
Automation scripts for:
- Build tasks
- Development workflows
- Testing commands

### `.devcontainer/manifest.json`
Container metadata including:
- Version information
- Compatibility details
- Configuration metadata

### `.devcontainer/.vscode/`
VS Code configuration files:
- `settings.json`: Editor and workspace settings
- `extensions.json`: Required extensions
- `launch.json`: Debug configurations
- `tasks.json`: Custom tasks

## Lifecycle Scripts

Located in `.devcontainer/scripts/`:

### Initialization Scripts
- `initializeCommand.sh`: Pre-container creation setup
- `onCreateCommand.sh`: First-time container setup
- `updateContentCommand.sh`: Content update handling
- `postCreateCommand.sh`: Post-creation configuration
- `postStartCommand.sh`: Container start tasks
- `postAttachCommand.sh`: Post-attach setup
- `preStopCommand.sh`: Pre-shutdown tasks

### Common Setup Scripts
- `install.sh`: Dependency installation
- `entrypoint.sh`: Container initialization
- `setup.sh`: Environment preparation
- `preBuild.sh`: Pre-build tasks
- `cleanup.sh`: Resource cleanup
- `test.sh`: Testing setup

### Directory Structure

```plaintext
.devcontainer/
├── devcontainer.json     # Main configuration file
├── Dockerfile           # Custom Docker image definition
├── docker-compose.yml   # Multi-container setup
├── Makefile            # Build and automation tasks
├── manifest.json       # Container metadata
├── README.md          # Documentation
├── .vscode/          # VS Code settings
│   ├── settings.json
│   ├── extensions.json
│   ├── launch.json
│   └── tasks.json
└── scripts/           # Lifecycle scripts
    ├── cleanup.sh
    ├── entrypoint.sh
    ├── initializeCommand.sh
    ├── install.sh
    ├── onCreateCommand.sh
    ├── postAttachCommand.sh
    ├── postCreateCommand.sh
    ├── postStartCommand.sh
    ├── preBuild.sh
    ├── preStopCommand.sh
    ├── setup.sh
    ├── test.sh
    └── updateContentCommand.sh
```      

## Sequential Order to run for Makefile to compose the build
preBuild.sh
initializeCommand.sh
onCreateCommand.sh
postCreateCommand.sh
entrypoint.sh
postStartCommand.sh
postAttachCommand.sh
install.sh
setup.sh
updateContentCommand.sh
test.sh
preStopCommand.sh
cleanup.sh
