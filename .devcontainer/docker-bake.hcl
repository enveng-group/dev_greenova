group "default" {
  targets = ["greenova"]
}

// Common variables
variable "PYTHON_VERSION" {
  default = "3.12.9"
}

variable "NODE_VERSION" {
  default = "20.19.1"
}

variable "NPM_VERSION" {
  default = "11.3.0"
}

variable "DJANGO_SETTINGS_MODULE" {
  default = "greenova.settings"
}

variable "PYTHONSTARTUP" {
  default = "/workspaces/greenova/pythonstartup"
}

variable "PYTHONIOENCODING" {
  default = "utf-8"
}

variable "PYTHONUNBUFFERED" {
  default = "1"
}

variable "PYTHONDONTWRITEBYTECODE" {
  default = "1"
}

variable "PYTHONWARNINGS" {
  default = "ignore"
}

variable "PYTHONHASHSEED" {
  default = "0"
}

variable "PYTHONPATH" {
  default = "/workspaces/greenova:/workspaces/greenova/greenova"
}

variable "NPM_BIN_PATH" {
  default = "/home/vscode/.nvm/versions/node/v20.19.1/bin/npm"
}

variable "NVM_DIR" {
  default = "/usr/local/share/nvm"
}

variable "NODE_PATH" {
  default = "/usr/local/share/nvm/versions/node/v20.19.1/lib/node_modules"
}

variable "COMPOSE_BAKE" {
  default = "true"
}

variable "PIP_NO_CACHE_DIR" {
  default = "1"
}

variable "PIP_CACHE_DIR" {
  default = "/root/.cache/pip"
}

variable "PIP_REQUIRE_VIRTUALENV" {
  default = "true"
}

variable "PATH" {
  default = "/usr/local/share/nvm/versions/node/v20.19.1/bin:/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games:/workspaces/greenova/.venv/bin"
}

// Single target for simplicity
target "greenova" {
  context = "."
  dockerfile = ".devcontainer/Dockerfile"
  cache-from = ["type=local,src=.cache/buildx"]
  cache-to = ["type=local,dest=.cache/buildx,mode=max"]
  tags = ["greenova:latest"]
  args = {
    PYTHON_VERSION = "${PYTHON_VERSION}"
    NODE_VERSION = "${NODE_VERSION}"
    NPM_VERSION = "${NPM_VERSION}"
    DJANGO_SETTINGS_MODULE = "${DJANGO_SETTINGS_MODULE}"
    PYTHONSTARTUP = "${PYTHONSTARTUP}"
    PYTHONIOENCODING = "${PYTHONIOENCODING}"
    PYTHONUNBUFFERED = "${PYTHONUNBUFFERED}"
    PYTHONDONTWRITEBYTECODE = "${PYTHONDONTWRITEBYTECODE}"
    PYTHONWARNINGS = "${PYTHONWARNINGS}"
    PYTHONHASHSEED = "${PYTHONHASHSEED}"
    PYTHONPATH = "${PYTHONPATH}"
    NPM_BIN_PATH = "${NPM_BIN_PATH}"
    NVM_DIR = "${NVM_DIR}"
    NODE_PATH = "${NODE_PATH}"
    COMPOSE_BAKE = "${COMPOSE_BAKE}"
    PIP_NO_CACHE_DIR = "${PIP_NO_CACHE_DIR}"
    PIP_CACHE_DIR = "${PIP_CACHE_DIR}"
    PIP_REQUIRE_VIRTUALENV = "${PIP_REQUIRE_VIRTUALENV}"
    PATH = "${PATH}"
  }
}
