# Environment Variables Management with dotenv

## Introduction

The dotenv package is a zero-dependency module that loads environment variables
from a `.env` file into your application's environment. It provides a simple
way to configure your applications while keeping sensitive information out of
your codebase. For Python applications, python-dotenv makes it easy to
integrate environment variables into various frameworks, including Django.

## Documentation

- [Dotenv Official Website](https://www.dotenv.org/)
- [Dotenv Official Documentation](https://www.dotenv.org/docs/)
- [Dotenv Python Documentation](https://www.dotenv.org/docs/languages/python)
- [Dotenv Quickstart Guide](https://www.dotenv.org/docs/quickstart)
- [GitHub - dotenv](https://github.com/motdotla/dotenv)
- [GitHub - python-dotenv](https://github.com/theskumar/python-dotenv)
- [GitHub - python-dotenv-vault](https://github.com/dotenv-org/python-dotenv-vault)

## Benefits of Using dotenv

- Keep sensitive credentials secure
- Environment-specific configuration
- Simplified deployment across different environments
- Prevent accidental commits of secrets
- Consistent configuration approach across team members
- Easy integration with CI/CD pipelines

## Best Practices

1. **Always add `.env` to your `.gitignore`**
2. Provide an example `.env.example` file with dummy values
3. Document all required environment variables
4. Use validation to ensure required variables are present

## Language Support

Dotenv implementations are available for multiple languages:

- JavaScript/Node.js
- Python
- Ruby
- PHP
- Go
- And many more

## Python Implementation

### Basic Usage

```python
# Install the package
# pip install python-dotenv

from dotenv_vault import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access environment variables
database_url = os.environ.get("DATABASE_URL")
secret_key = os.environ.get("SECRET_KEY")
```

### Advanced Options

```python
from dotenv_vault import load_dotenv, find_dotenv

# Automatically find .env file
load_dotenv(find_dotenv())

# Override existing environment variables
load_dotenv(override=True)

# Specify a different .env file
load_dotenv("/path/to/custom/.env")
```

## Django Integration

### Adding to Django Settings

````python
# settings.py
import os
from dotenv_vault import load_dotenv

# Load environment variables
load_dotenv()

# Use environment variables in settings
SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = os.environ.get("DEBUG", "False") == "True"
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": os.environ.get("DB_PORT"),
### Example .env File for Django

## Environment Variables with Dotenv Vault

This project uses `python-dotenv-vault` to manage environment variables securely
across different environments.

# Environment Variables with Dotenv Vault

This project uses `python-dotenv-vault` to manage environment variables securely across different environments.

## Development Environment

In development, environment variables are loaded from the `.env` file:

```python
import os
from dotenv_vault import load_dotenv

load_dotenv()  # Takes environment variables from .env

# Access variables
debug_mode = os.getenv("DJANGO_DEBUG")
````

## Production Environment

For production, you can encrypt your environment variables:

1. **Install the dotenv CLI tool**:

   ```bash
   npm install -g dotenv-cli
   ```

2. **Create environment-specific files**:

   ```bash
   # .env.production
   DJANGO_DEBUG=False
   DJANGO_SECRET_KEY=your-production-secret-key
   DJANGO_ALLOWED_HOSTS=app.greenova.com.au
   ```

3. **Build the vault file**:

   ```bash
   npx dotenv-vault local build
   ```

4. This creates:

   - `.env.vault`: Contains encrypted variables
   - `.env.keys`: Contains encryption keys

5. **Set the `DOTENV_KEY` environment variable** on your production server
   using the appropriate key from `.env.keys`.

6. **Commit only the `.env.vault` file** to your repository (it's safe since
   it's encrypted).

## Multiple Environments

Create different environment files for different deployment environments:

- `.env.development`
- `.env.staging`
- `.env.production`

Build all of them into your vault:

```bash
- ❌ **NEVER commit** your `.env` or `.env.keys` files to version control
- 🔒 Keep your `DOTENV_KEY` secure and only share with authorized team members
- ✅ The `.env.vault` file is safe to commit as it contains encrypted
  data
## Security Guidelines

- ❌ **NEVER commit** your `.env` or `.env.keys` files to version control
- 🔒 Keep your `DOTENV_KEY` secure and only share with authorized team members
- ✅ The `.env.vault` file is safe to commit as it contains encrypted data

## Example Environment Setup

Development (`.env`):
```
