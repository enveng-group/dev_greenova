# SSH agent configuration
if not set -q SSH_AUTH_SOCK
    eval (ssh-agent -c | string split ';' | head -n 1)
end
if test -f ~/.ssh/id_gitlab
    chmod 600 ~/.ssh/id_gitlab
    ssh-add ~/.ssh/id_gitlab ^/dev/null
end

# UV/UVX completions
if type -q uv
    complete -c uv -e
    uv generate-shell-completion fish | source
end

if type -q uvx
    complete -c uvx -e
    uvx --generate-shell-completion fish | source
end

# Python development settings
set -gx PYTHONDONTWRITEBYTECODE 1
set -gx PYTHONBREAKPOINT ipdb.set_trace
set -gx VIRTUAL_ENV_DISABLE_PROMPT 1

# VS Code integration
if type -q code
    set -gx EDITOR code -w
    alias e="code ."
end

# Virtual environment handling
function __handle_virtualenv --on-variable PWD
    status --is-command-substitution; and return

    if test -e .venv/bin/activate.fish
        if not set -q VIRTUAL_ENV
            source .venv/bin/activate.fish
        end
    else if set -q VIRTUAL_ENV
        if not string match -q -- "$PWD*" (dirname "$VIRTUAL_ENV")
            deactivate
        end
    end
end

# Ensure the function runs when shell starts
__handle_virtualenv

# Custom prompt with git status and virtual env
function fish_prompt
    set -l last_status $status

    # Show Python virtual env
    if set -q VIRTUAL_ENV
        echo -n (set_color blue)"("(basename $VIRTUAL_ENV)") "(set_color normal)
    end

    # Current directory
    echo -n (set_color green)(prompt_pwd)(set_color normal)

    # Git status if available
    if type -q git
        and test -d .git
        or git rev-parse --git-dir >/dev/null 2>&1
        set -l git_branch (git symbolic-ref --short HEAD 2>/dev/null)
        if test $status = 0
            echo -n (set_color yellow)" ($git_branch)"
            set -l git_status (git status --porcelain)
            if test -n "$git_status"
                echo -n (set_color red)"*"
            end
        end
    end

    # Prompt character
    if test $last_status = 0
        echo -n (set_color normal)" λ "
    else
        echo -n (set_color red)" λ "
    end
end

# Add local bin to PATH
if test -d $HOME/.local/bin
    set -gx PATH $HOME/.local/bin $PATH
end