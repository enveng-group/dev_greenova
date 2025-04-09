# Python Packaging with Setuptools

## Introduction to Setuptools

Setuptools is a collection of enhancements to the Python distutils that
facilitates building, distributing, and installing Python packages. It serves
as the foundation for most Python packaging tools and workflows, allowing
developers to define metadata and dependencies for their projects [[1]](#1).
│ ├── settings.py
│ ├── urls.py
│ ├── wsgi.py
├── obligations/
│ ├── **init**.py
│ ├── admin.py
│ ├── apps.py
│ ├── models.py
│ ├── views.py
│ └── ...
└── ...
include LICENSE
include README.md
recursive-include greenova/static _
recursive-include greenova/templates_
recursive-include obligations/templates _
recursive-include obligations/static_

# Python Packaging with Setuptools

### Configuration Structure

## Introduction to Setuptools

Setuptools is a collection of enhancements to the Python distutils that
facilitates building, distributing, and installing Python packages. It serves
as the foundation for most Python packaging tools and workflows, allowing
developers to define metadata and dependencies for their projects [1].

Key benefits of using setuptools include:

- Automatic package discovery
- Dependency management
- Entry point declarations
- Development mode installation (`pip install -e .`)
- Package metadata management

For the Greenova project, setuptools enables us to properly package our Django
application, manage its dependencies, and prepare it for deployment.

## Setup.py Overview

### Key Configuration Parameters

| Parameter                       | Description                                   | Example                                               |
| ------------------------------- | --------------------------------------------- | ----------------------------------------------------- |
| `name`                          | Package name as it will appear on PyPI        | `"greenova"`                                          |
| `version`                       | Package version following semantic versioning | `"0.1.0"`                                             |
| `description`                   | Short, one-sentence summary                   | `"Environmental management system"`                   |
| `long_description`              | Detailed description (often README content)   | `open("README.md").read()`                            |
| `long_description_content_type` | Format of long description                    | `"text/markdown"`                                     |
| `author`                        | Package maintainer name                       | `"Greenova Team"`                                     |
| `author_email`                  | Maintainer contact                            | `"team@greenova.example"`                             |
| `url`                           | Project homepage                              | `"https://github.com/greenova/greenova"`              |
| `packages`                      | Python packages to include                    | `find_packages()`                                     |
| `python_requires`               | Python version constraints                    | `">=3.9.21"`                                          |
| `install_requires`              | Package dependencies                          | `["Django>=4.1.13", ...]`                             |
| `extras_require`                | Optional dependency groups                    | `{"dev": ["pytest", "black"], ...}`                   |
| `package_data`                  | Non-Python files to include                   | `{"greenova": ["static/*", "templates/*"]}`           |
| `include_package_data`          | Include data from MANIFEST.in                 | `True`                                                |
| `entry_points`                  | Command-line script definitions               | `{"console_scripts": ["greenova=greenova.cli:main"]}` |
| `classifiers`                   | PyPI classifiers                              | `["Framework :: Django", ...]`                        |

    ],
    # Additional configuration...

)

````

### Key Configuration Parameters

| Parameter                       | Description                                   | Example                                               |
| ------------------------------- | --------------------------------------------- | ----------------------------------------------------- |
| `name`                          | Package name as it will appear on PyPI        | `"greenova"`                                          |
| `version`                       | Package version following semantic versioning | `"0.1.0"`                                             |
| `description`                   | Short, one-sentence summary                   | `"Environmental management system"`                   |
| `long_description`              | Detailed description (often README content)   | `open("README.md").read()`                            |
| `long_description_content_type` | Format of long description                    | `"text/markdown"`                                     |
| `author`                        | Package maintainer name                       | `"Greenova Team"`                                     |
| `author_email`                  | Maintainer contact                            | `"team@greenova.example"`                             |
| `url`                           | Project homepage                              | `"https://github.com/greenova/greenova"`              |
| `packages`                      | Python packages to include                    | `find_packages()`                                     |
| `python_requires`               | Python version constraints                    | `">=3.9.21"`                                          |
| `install_requires`              | Package dependencies                          | `["Django>=4.1.13", ...]`                             |
| `extras_require`                | Optional dependency groups                    | `{"dev": ["pytest", "black"], ...}`                   |
| `package_data`                  | Non-Python files to include                   | `{"greenova": ["static/*", "templates/*"]}`           |
| `include_package_data`          | Include data from MANIFEST.in                 | `True`                                                |
| `entry_points`                  | Command-line script definitions               | `{"console_scripts": ["greenova=greenova.cli:main"]}` |
| `classifiers`                   | PyPI classifiers                              | `["Framework :: Django", ...]`                        |

### Example Setup.py for Greenova

```python
from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="greenova",
    version="0.1.0",
    description="Environmental management and compliance tracking system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Greenova Team",
    author_email="team@greenova.example",
    url="https://github.com/greenova/greenova",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.9.21",
    install_requires=[
        "Django==4.1.13",
        "matplotlib==3.9.4",
        "django-htmx==1.22.0",
        "django-hyperscript==1.0.2",
        "django-tailwind==3.6.0",
        "django-allauth==65.4.1",
        "django-browser-reload==1.18.0",
        "django-debug-toolbar==5.0.1",
        "django-template-partials==24.4",
        "gunicorn==23.0.0",
        "python-dotenv-vault==0.6.4",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-django>=4.5.2",
            "black>=23.1.0",
            "isort>=5.12.0",
            "pylint>=2.15.10",
            "pylint-django>=2.5.3",
            "mypy>=1.0.1",
            "django-stubs>=1.14.0",
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 4.1",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Environmental Management",
    ],
    project_urls={
        "Documentation": "https://greenova.readthedocs.io/",
        "Source": "https://github.com/greenova/greenova/",
        "Issues": "https://github.com/greenova/greenova/issues",
    },
)
````

## Setup.cfg Overview

`setup.cfg` is a configuration file that allows moving setup parameters from
`setup.py` into a declarative format. This approach separates the build script
logic from the package metadata, making it more maintainable.

### Basic Structure

```ini
[metadata]
name = greenova
version = 0.1.0
description = Environmental management and compliance tracking system
long_description = file: README.md
long_description_content_type = text/markdown
author = Greenova Team
author_email = team@greenova.example
url = https://github.com/greenova/greenova
classifiers =
    Development Status :: 4 - Beta
    Framework :: Django
    Framework :: Django :: 4.1
    Programming Language :: Python :: 3.9

[options]
packages = find:
python_requires = >=3.9.21
install_requires =
    Django==4.1.13
    matplotlib==3.9.4
    django-htmx==1.22.0
    django-hyperscript==1.0.2
    # Additional dependencies...
include_package_data = True

[options.extras_require]
dev =
    pytest>=7.0.0
    black>=23.1.0
    isort>=5.12.0
```

### Setup.py with Setup.cfg

When using `setup.cfg`, your `setup.py` can be significantly simplified:

```python
from setuptools import setup

setup()
```

## Django-Specific Setuptools Usage

Django projects have special considerations when using setuptools:

### Package Structure

For a Django project like Greenova, the typical structure with setuptools would
be:

```
greenova/
├── setup.py
├── setup.cfg
├── MANIFEST.in
├── README.md
├── greenova/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── obligations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   └── ...
└── ...
```

### Including Django Templates and Static Files

Django projects typically include non-Python files like templates and static
resources. These can be included using a `MANIFEST.in` file:

```
include LICENSE
include README.md
recursive-include greenova/static *
recursive-include greenova/templates *
recursive-include obligations/templates *
recursive-include obligations/static *
```

And ensure `include_package_data=True` is set in your setup configuration.

### Django Application Discovery

To ensure Django discovers your application modules:

```python
# In your app's __init__.py
default_app_config = 'obligations.apps.ObligationsConfig'
```

## Modern Python Packaging Trends

### PEP 517 and PEP 518: pyproject.toml

Recent Python Enhancement Proposals have introduced `pyproject.toml` as a
standardized configuration file for Python projects. Setuptools now supports
this format:

```toml
[build-system]
requires = ["setuptools>=42", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "greenova"
version = "0.1.0"
description = "Environmental management and compliance tracking system"
readme = "README.md"
requires-python = ">=3.9.21"
license = {text = "MIT"}
dependencies = [
    "Django==4.1.13",
    "matplotlib==3.9.4",
    # Other dependencies...
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=23.1.0",
]
```

### Transitioning from setup.py to pyproject.toml

While `pyproject.toml` is gaining popularity, many projects (including many
Django projects) still use `setup.py` or `setup.cfg`. For the Greenova project,
we recommend:

1. Continue using `setup.py` for backward compatibility
2. Consider migrating configuration to `setup.cfg` for improved readability
3. Monitor trends in the Django ecosystem regarding `pyproject.toml` adoption

## Installation and Development Workflow

### Development Installation

For local development:

```bash
# Clone the repository
git clone https://github.com/greenova/greenova.git
cd greenova

# Install in development mode with dev dependencies
pip install -e ".[dev]"
```

### Production Installation

For deployment:

```bash
# Install from the repository
pip install git+https://github.com/greenova/greenova.git

# Or, if published to PyPI
pip install greenova
```

### Creating Distribution Packages

```bash
python -m pip install --upgrade build twine
python -m build
```

This creates both source distribution (`sdist`) and wheel formats in the
`dist/` directory.

## Best Practices for Greenova Project

1. **Pin production dependencies**: Use exact versions for production
   dependencies to ensure reproducible builds
2. **Use ranges for development dependencies**: Allow flexibility for
   development tools
3. **Separate core and optional dependencies**: Use `extras_require` for
   development, testing, and documentation dependencies
4. **Include all necessary package data**: Ensure templates, static files, and
   migrations are properly included
5. **Document installation procedures**: Include clear instructions for both
   development and production installations
6. **Use semantic versioning**: Follow SemVer practices for version numbers

## References

<a id="1"></a>[1] Python Packaging Authority, "Packaging and distributing
projects," Python Packaging User Guide, 2023. [Online]. Available:
<https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/>
[Accessed: Mar. 27, 2025].

<a id="2"></a>[2] J. L. Redrobe, "What's the deal with setuptools, setup.py and
setup.cfg?," Bit e-Code, Apr. 2022. [Online]. Available:
<https://www.bitecode.dev/p/whats-the-deal-with-setuptools-setuppy>
[Accessed: Mar. 27, 2025].

<a id="3"></a>[3] S. Romero, "Using setup.py for Your Django Project,"
Lincoln Loop, Feb. 2018. [Online]. Available:
<https://lincolnloop.com/insights/using-setuppy-your-django-project/>
[Accessed: Mar. 27, 2025].

<a id="4"></a>[4] J. Kreimes, "django-setup-demo," GitHub repository, 2021.
[Online]. Available: <https://github.com/axju/django-setup-demo>
[Accessed: Mar. 27, 2025].

<a id="5"></a>[5] C. J. Koikara, "The setup.py," Medium, Nov. 2021. [Online].
Available: <https://medium.com/@christina.jacob.koikara/the-setup-py-16eefeb2f6f2>
[Accessed: Mar. 27, 2025].

<a id="6"></a>[6] V. Dasari, "Packaging a Django Project Using Setuptools,"
Write by Agrevolution, Jun. 2021. [Online]. Available:
<https://write.agrevolution.in/packaging-a-django-project-using-setuptools-c1d7d565779e>
[Accessed: Mar. 27, 2025].

<a id="7"></a>[7] Python Packaging Authority, "Setuptools documentation,"
Setuptools, 2023. [Online]. Available:
<https://setuptools.pypa.io/en/latest/setuptools.html>
[Accessed: Mar. 27, 2025].
[2] J. L. Redrobe, "What's the deal with setuptools, setup.py and setup.cfg?,"
Bit e-Code, Apr. 2022. [Online]. Available:
<https://www.bitecode.dev/p/whats-the-deal-with-setuptools-setuppy> [Accessed:
Mar. 27, 2025].

[3] S. Romero, "Using setup.py for Your Django Project," Lincoln Loop,
Feb. 2018. [Online]. Available:
<https://lincolnloop.com/insights/using-setuppy-your-django-project/> [Accessed:
Mar. 27, 2025].

[4] J. Kreimes, "django-setup-demo," GitHub repository, 2021. [Online].
Available: <https://github.com/axju/django-setup-demo> [Accessed: Mar. 27, 2025].

[5] C. J. Koikara, "The setup.py," Medium, Nov. 2021. [Online]. Available:
<https://medium.com/@christina.jacob.koikara/the-setup-py-16eefeb2f6f2>
[Accessed: Mar. 27, 2025].

[6] V. Dasari, "Packaging a Django Project Using Setuptools," Write by
Agrevolution, Jun. 2021. [Online]. Available:
<https://write.agrevolution.in/packaging-a-django-project-using-setuptools-c1d7d565779e>
[Accessed: Mar. 27, 2025].

[7] Python Packaging Authority, "Setuptools documentation," Setuptools, 2023.
[Online]. Available: <https://setuptools.pypa.io/en/latest/setuptools.html>
[Accessed: Mar. 27, 2025].
