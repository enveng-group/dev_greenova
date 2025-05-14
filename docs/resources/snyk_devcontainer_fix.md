# Snyk Dev Container Fix (May 2025)

This project configures the Snyk VS Code extension and CLI to work reliably in
a containerized development environment by ensuring all cache, config, and CLI
files are stored in container-local directories. This prevents permission
errors (EACCES) related to host-only paths.

## Key Changes

- **.devcontainer/docker-compose.yml**: Sets the following environment
  variables for the `greenova` service:
  - `HOME=/home/vscode`
  - `XDG_DATA_HOME=/home/vscode/.local/share`
  - `SNYK_CACHE_PATH=/home/vscode/.local/share/snyk`
- **.vscode/settings.json**: Explicitly configures the Snyk extension to use
  container-local paths:
  - `snyk.cliPath`, `snyk.languageServerPath`, and `snyk.cachePath` all point
    to `/home/vscode/.local/share/snyk`

## Why?

By default, the Snyk extension may attempt to use the host's `$HOME` or macOS
`Library` directory, which is not writable from inside the container. This
causes EACCES errors when downloading the CLI or language server. Forcing all
Snyk-related paths to container-local directories resolves this issue.

## References

- [Snyk VS Code Extension Troubleshooting](https://docs.snyk.io/scm-ide-and-ci-cd-integrations/snyk-ide-plugins-and-extensions/visual-studio-code-extension/troubleshooting-for-visual-studio-code-extension)
- [Snyk VS Code Extension Configuration](https://docs.snyk.io/scm-ide-and-ci-cd-integrations/snyk-ide-plugins-and-extensions/visual-studio-code-extension/visual-studio-code-extension-configuration)
- [Greenova Dev Container Standards](docs/project/container_environment.md)

## Next Steps

1. Rebuild and reopen the dev container in VS Code.
2. Open the Snyk extension and verify that the CLI and language server download
   and initialize without errors.
3. Confirm that no EACCES or permission denied errors occur.

---

_This file documents the Snyk dev container fix as of May 2025. For future
updates, consult the official Snyk and Greenova documentation._
