gh auth login
(.venv) vscode ➜ /workspaces/greenova (staging) $ gh auth login
? Where do you use GitHub? GitHub.com
? What is your preferred protocol for Git operations on this host? SSH
? Upload your SSH public key to your GitHub account? /home/vscode/.ssh/id_ed25519.pub
? Title for your SSH key: GitHub CLI
? How would you like to authenticate GitHub CLI? Login with a web browser

! First copy your one-time code: 62B2-56B5
Press Enter to open <https://github.com/login/device> in your browser...
✓ Authentication complete.

- gh config set -h github.com git_protocol ssh
  ✓ Configured git protocol
  ! Authentication credentials saved in plain text
  ✓ SSH key already existed on your GitHub account: /home/vscode/.ssh/id_ed25519.pub
  ✓ Logged in as enveng-group
  gh extension install github/gh-copilot
  ✓ Installed extension github/gh-copilot
