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
        "django-debug-toolbar>=5.0.1",
        "django-environ>=0.11.2",
        "pillow==11.1.0",
        "python-dotenv==1.0.1",
    ],
    python_requires=">=3.12.8",
)
