# Python Packaging with Setuptools

## Introduction to Setuptools

Setuptools is a collection of enhancements to the Python distutils that
facilitates building, distributing, and installing Python packages. It serves
as the foundation for most Python packaging tools and workflows, allowing
developers to define metadata and dependencies for their projects.

### Key Benefits

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
| `python_requires`               | Python version constraints                    | `">=3.12.9"`                                          |
| `install_requires`              | Package dependencies                          | `["Django>=5.2", ...]`                                |
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
    python_requires=">=3.12.9",
    install_requires=[
        "Django==5.2",
        "matplotlib==3.9.4",
        "django-htmx==1.22.0",
        "django-hyperscript==1.0.2",
        "django-tailwind==4.0.1",
        "django-allauth==65.4.1",
        "django-browser-reload==1.18.0",
        "django-debug-toolbar==5.1.0",
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
```

## References

[1] Python Packaging Authority, "Packaging and distributing projects," Python
Packaging User Guide, 2023. [Online]. Available:
<https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/>
[Accessed: Mar. 27, 2025].
