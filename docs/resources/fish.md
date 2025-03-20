# Fish Shell

## Introduction

The Fish shell (Friendly Interactive SHell) is a smart and user-friendly command line shell for Linux, macOS, and other Unix-like operating systems. It's the preferred shell for the Greenova project due to its intuitive features, excellent interactive experience, and developer-friendly capabilities.

## Key Features

- **Autosuggestions**: Fish suggests commands as you type based on history and completions
- **Syntax highlighting**: Commands, arguments, and paths are colored for clarity
- **Tab completions**: Robust and context-aware tab completion with detailed explanations
- **Web-based configuration**: Easy configuration through a web interface
- **Scripting language**: Clean, powerful and consistent scripting syntax
- **No configuration required**: Works great out of the box

## Installation

### macOS
```bash
brew install fish
```

### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install fish
```

### Fedora
```bash
sudo dnf install fish
```

### Arch Linux
```bash
sudo pacman -S fish
```

### From Source
```bash
git clone https://github.com/fish-shell/fish-shell.git
cd fish-shell
mkdir build; cd build
cmake ..
make
sudo make install
```

## Setting Fish as Your Default Shell

```bash
# Find the path to fish
which fish

# Add fish to allowed shells
echo $(which fish) | sudo tee -a /etc/shells

# Change your default shell
chsh -s $(which fish)
```

## Basic Usage

### Navigation

Fish uses the same basic navigation commands as other shells:

```fish
cd directory/      # Change directory
cd ..              # Go up one directory
cd ~               # Go to home directory
pwd                # Print working directory
ls                 # List files
```

### Command History

```fish
history            # View command history
↑ or ↓             # Navigate through history
Alt+↑ or Alt+↓     # Search history by token
```

### Autosuggestions

As you type, Fish will suggest commands in gray text. To accept a suggestion:
- Press →: Accept the entire suggestion
- Press Alt+→: Accept one word of the suggestion

### Variables

```fish
set name value     # Set a variable
echo $name         # Access a variable
set -x PATH $PATH $HOME/bin  # Add to PATH
set -e name        # Erase a variable
```

## Using Fish with Greenova

### Project-Specific Fish Configuration

Create a project-specific Fish configuration file in the Greenova project:

```fish
# ~/.config/fish/conf.d/greenova.fish

# Set up environment variables
set -x GREENOVA_ENV development
set -x DJANGO_SETTINGS_MODULE greenova.settings.development

# Add project directories to PATH
set -x PATH $PATH /workspaces/greenova/scripts

# Project aliases
alias grun "cd /workspaces/greenova && python manage.py runserver"
alias gmig "cd /workspaces/greenova && python manage.py migrate"
alias gmake "cd /workspaces/greenova && python manage.py makemigrations"
alias gshell "cd /workspaces/greenova && python manage.py shell"
alias gtest "cd /workspaces/greenova && python manage.py test"
```

### Activating Virtual Environment in Fish

For Python projects with virtual environments:

```fish
# Activate virtual environment
function venv
    source /workspaces/greenova/env/bin/activate.fish
end

# Deactivate virtual environment (automatically provided by venv)
# Simply type 'deactivate' when you're done
```

### Virtual Environment Auto-Activation

Create a `.envrc` file in your project root:
