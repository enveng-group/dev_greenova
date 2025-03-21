from setuptools import setup, find_packages

setup(
    name="greenova",
    version="1.0.0",
    description="A POSIX-compliant Django web application",
    long_description=open("README.md").read(),
    author="enveng-group",
    author_email="info@enveng-group",
    url="https://github.com/enveng-group/dev_greenova.git",
    packages=find_packages(),
    install_requires=[
        "python==3.9.21",
        "Django==4.2.20",
        "matplotlib==3.10.0",
        "django-htmx==1.22.0",
        "django-hyperscript==1.0.2",
        "django-tailwind==3.6.0",
        "django-allauth==65.4.1",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
)
