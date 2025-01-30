from setuptools import setup, find_packages

setup(
    name="greenova",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Django>=5.1.5",
        "django-htmx>=1.21.0",
        "django-chartjs>=2.3.0",
        "whitenoise>=6.8.2",
        "daphne>=4.1.2",
        "django-compressor>=4.5.1",
        "django-debug-toolbar>=5.0.1",
        "WeasyPrint>=61.0",
        "django-environ>=0.11.2",
    ],
    python_requires=">=3.12.8",
)