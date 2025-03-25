# setup.py introduction

This 'setup.py' file used to package and install the ** Greenova Django web 
application **

# Key Fields

- **name** : The name of the pakage.
- **Version** : The current version.
- **desription** : A short project summary.
- **long_description** : Detaild README content.
- **author** / **author_email** :  Maintainer information.
- **url** : Project homepage.
- **packages=find_packages()** : Auto detect Python packages.
- **python_requires** :python version requirement.
- **install_requires** : Require third-party libralies.
- **include_package_data=True** :
- **classifiers** : Metadata for PyPI and tooling.
- **project_urls** : Additional links.

# Install require dependencies

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

# What I learned

1. I learned how to whrite 'setup.py' to package a Python project, including filling
in metadata, dependency information, and version requirements.
2. I learned the role of install_requires, which ensure that the project automatically
pulls in all require third-party libralies when installing.

# References

https://github.com/axju/django-setup-demo, 
https://write.agrevolution.in/packaging-a-django-project-using-setuptools-c1d7d565779e, https://lincolnloop.com/insights/using-setuppy-your-django-project/,
https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/, https://setuptools.pypa.io/en/latest/userguide/declarative_config.html, 
https://adamj.eu/tech/2023/03/02/django-profile-and-improve-import-time/, 
https://www.bitecode.dev/p/happiness-is-a-good-pythonstartup, 
https://docs.python.org/3/using/cmdline.html
