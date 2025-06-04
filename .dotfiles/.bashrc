#!/bin/bash
# .bashrc file for Greenova development environment

# Exit on error in non-interactive shells
# shellcheck disable=SC2148
case $- in
*i*) ;;
*) set -e ;;
esac

# Source global definitions if they exist
# shellcheck source=/dev/null
[ -f /etc/bashrc ] && . /etc/bashrc

# Alias definitions
alias django-run="/workspaces/greenova/.venv/bin/python greenova/manage.py runserver 0.0.0.0:8000"

# Enhanced bash prompt with dynamic system usage
__set_ps1() {
        local userpart gitbranch lightblue removecolor

        if [ -n "${GITHUB_USER:-}" ]; then
                userpart="\[\033[0;32m\]@${GITHUB_USER} "
        else
                userpart="\[\033[0;32m\]\u "
        fi

        # Add error indicator
        userpart="${userpart}\[\033[0m\]➜"

        # Git branch information
        gitbranch=""
        if [ "$(git config --get devcontainers-theme.hide-status 2>/dev/null)" != "1" ] &&
                [ "$(git config --get codespaces-theme.hide-status 2>/dev/null)" != "1" ]; then
                local branch
                branch="$(git --no-optional-locks symbolic-ref --short HEAD 2>/dev/null ||
                        git --no-optional-locks rev-parse --short HEAD 2>/dev/null)"
                if [ -n "$branch" ]; then
                        gitbranch="\[\033[0;36m\](\[\033[1;31m\]${branch}"
                        if [ "$(git config --get devcontainers-theme.show-dirty 2>/dev/null)" = "1" ] &&
                                git --no-optional-locks ls-files --error-unmatch -m --directory \
                                        --no-empty-directory -o --exclude-standard ":/*" >/dev/null 2>&1; then
                                gitbranch="${gitbranch} \[\033[1;33m\]✗"
                        fi
                        gitbranch="${gitbranch}\[\033[0;36m\]) "
                fi
        fi

        lightblue='\[\033[1;34m\]'
        removecolor='\[\033[0m\]'
        # Use command substitution for system usage
        PS1="${userpart} ${lightblue}\w ${gitbranch}${removecolor}\$ "
}

__set_ps1
export PROMPT_DIRTRIM=4

# Terminal title functions for xterm-compatible terminals
if [[ $TERM =~ ^(xterm|screen|tmux) ]]; then
        # Function to set terminal title to current command
        __preexec() {
                local cmd="${BASH_COMMAND}"
                # Truncate long commands for readability
                if [ ${#cmd} -gt 50 ]; then
                        cmd="${cmd:0:47}..."
                fi
                printf '\033]0;%s@%s: %s\007' "${USER}" "${HOSTNAME%%.*}" "$cmd"
        }

        # Function to reset terminal title after command execution
        __precmd() {
                printf '\033]0;%s@%s: %s\007' "${USER}" "${HOSTNAME%%.*}" "${PWD##*/}"
        }

        # Set up command trapping
        trap '__preexec' DEBUG
        PROMPT_COMMAND="${PROMPT_COMMAND:+$PROMPT_COMMAND; }__precmd"
fi

# Environment variables for development
export EDITOR="${EDITOR:-code}"
export BROWSER="${BROWSER:-}"
export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH:}."
export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-greenova.settings}"

# Auto-activate virtual environment if it exists and we're in the project directory
__auto_activate_venv() {
        # Only auto-activate if we're in the greenova project directory or subdirectory
        if [[ $PWD == /workspaces/greenova* ]] && [[ -z $VIRTUAL_ENV ]]; then
                if [[ -f "/workspaces/greenova/.venv/bin/activate" ]]; then
                        # shellcheck source=/dev/null
                        source "/workspaces/greenova/.venv/bin/activate"
                        echo "🐍 Auto-activated virtual environment: .venv"
                fi
        fi
}

# Call the auto-activation function
__auto_activate_venv

# Set iPython as the default Python interactive shell
export PYTHONSTARTUP="${PYTHONSTARTUP:-/workspaces/greenova/python_startup.py}"
# Use ipython as the default Python shell when available
if command -v ipython >/dev/null 2>&1; then
        alias python="ipython"
        alias python3="ipython"
fi

# Clear SSH agent environment variables for Dropbear compatibility
# Dropbear doesn't use SSH agent, so these variables can interfere
unset SSH_AUTH_SOCK
unset SSH_AGENT_PID

# Clear SSH agent environment variables for Dropbear compatibility
# Dropbear doesn't use SSH agent and these variables can cause issues
unset SSH_AUTH_SOCK
unset SSH_AGENT_PID

# Enhanced environment variables
export DJANGO_DEBUG="${DJANGO_DEBUG:-True}"
export DJANGO_LOG_LEVEL="${DJANGO_LOG_LEVEL:-INFO}"

# Prefer uv for Python package management
if command -v uv >/dev/null 2>&1; then
        alias pip="uv pip"
        alias pip3="uv pip"
        export UV_PYTHON_PREFERENCE="system"
fi

# Enhanced history settings
export HISTSIZE=50000
export HISTFILESIZE=100000
export HISTCONTROL=ignoreboth:erasedups
export HISTTIMEFORMAT='%F %T '
shopt -s histappend
shopt -s histverify
shopt -s checkwinsize
shopt -s autocd 2>/dev/null || true   # Change to directory by typing name (bash 4+)
shopt -s globstar 2>/dev/null || true # Enable ** for recursive globbing (bash 4+)

# Better tab completion
bind 'set completion-ignore-case on'
bind 'set completion-map-case on'
bind 'set show-all-if-ambiguous on'
bind 'set menu-complete-display-prefix on'

# Enable programmable completion features
if ! shopt -oq posix; then
        # shellcheck source=/dev/null
        if [ -f /usr/share/bash-completion/bash_completion ]; then
                . /usr/share/bash-completion/bash_completion
        elif [ -f /etc/bash_completion ]; then
                . /etc/bash_completion
        fi
fi

# Quick navigation functions
cdp() {
        cd "$(find . -type d -name "*$1*" | head -1)" 2>/dev/null || echo "Directory not found"
}

# Extract various archive formats
extract() {
        if [ -f "$1" ]; then
                case "$1" in
                *.tar.bz2) tar xjf "$1" ;;
                *.tar.gz) tar xzf "$1" ;;
                *.bz2) bunzip2 "$1" ;;
                *.rar) unrar x "$1" ;;
                *.gz) gunzip "$1" ;;
                *.tar) tar xf "$1" ;;
                *.tbz2) tar xjf "$1" ;;
                *.tgz) tar xzf "$1" ;;
                *.zip) unzip "$1" ;;
                *.Z) uncompress "$1" ;;
                *.7z) 7z x "$1" ;;
                *) echo "'$1' cannot be extracted via extract()" ;;
                esac
        else
                echo "'$1' is not a valid file"
        fi
}

# Load local customizations if they exist
# shellcheck source=/dev/null
[ -f ~/.bashrc.local ] && . ~/.bashrc.local

# Welcome message and project status for new sessions
if [ -n "${PS1:-}" ] && [ "${BASH_EXECUTION_STRING:-}" = "" ]; then
        echo "Welcome to Greenova development environment!"
        echo "=== Project Status ==="
        echo "Working directory: $(pwd)"
        echo "Git branch: $(git branch --show-current 2>/dev/null || echo 'Not a git repo')"
        echo "Git status:"
        git status --porcelain 2>/dev/null || echo "Not a git repository"
        echo ""

        # Show actual Python version (bypass alias)
        if command -v python3 >/dev/null 2>&1; then
                echo "Python version: $(command python3 --version 2>/dev/null || /usr/bin/python3 --version 2>/dev/null || echo 'Not found')"
        else
                echo "Python version: $(command /usr/bin/python --version 2>/dev/null || echo 'Not found')"
        fi

        # Show iPython version if available
        if command -v ipython >/dev/null 2>&1; then
                echo "iPython version: $(command ipython --version 2>/dev/null || echo 'Not found')"
        fi

        # Show which Python executable is being used
        if alias python >/dev/null 2>&1; then
                echo "Python shell: $(alias python | cut -d"'" -f2) (aliased)"
        else
                echo "Python executable: $(command -v python)"
        fi

        echo "Virtual environment: ${VIRTUAL_ENV:-None}"
        echo "PYTHONPATH: ${PYTHONPATH:-Not set}"
        echo "Django settings: ${DJANGO_SETTINGS_MODULE:-Not set}"
        echo "Django debug: ${DJANGO_DEBUG:-Not set}"
        echo ""
fi
