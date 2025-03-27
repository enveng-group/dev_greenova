from setuptools import find_packages, setup

# Use a context manager with explicit encoding
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='greenova',
    version='0.0.4',
    description='A Django web application',
    long_description=long_description,
    author='enveng-group',
    author_email='164126503+enveng-group@users.noreply.github.com',
    url='https://github.com/enssol/greenova',
    packages=find_packages(),
    python_requires='>=3.9.0, <3.10.0',
    install_requires=[
        'Django==4.1.13',
        'matplotlib==3.9.4',
        'django-htmx==1.22.0',
        'django-hyperscript==1.0.2',
        'django-tailwind==3.6.0',
        'django-allauth==65.4.1',
        'django-browser-reload==1.18.0',
        'django-debug-toolbar==5.0.1',
        'django-template-partials==24.4',
        'python-dotenv-vault==0.6.4',
    ],
    extras_require={
        'dev': [
            'pytest>=7.3.1',
            'pytest-django>=4.5.2',
            'pytest-cov>=4.1.0',
            'pytest-xdist>=3.3.1',
            'selenium>=4.11.2',
            'webdriver-manager>=4.0.0',
            'django-stubs>=4.2.3',
            'mypy>=1.4.1',
            'pylint>=2.17.4',
            'pylint-django>=2.5.3',
            'black>=23.3.0',
        ],
    },
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Framework :: Django',
        'Framework :: Django :: 4.1',
    ],
    project_urls={
        'Source': 'https://github.com/enssol/greenova.git',
        'Issue Tracker': 'https://github.com/enssol/greenova/issues',
    },
)
