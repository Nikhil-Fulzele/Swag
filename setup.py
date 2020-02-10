import os
from setuptools import setup

packages = []
for d, _, _ in os.walk('swag'):
    if 'venv' not in d and os.path.exists(os.path.join(d, '__init__.py')):
        packages.append(d.replace(os.path.sep, '.'))

requirements = []
with open("requirements.txt", "r") as f:
    for line in f:
        requirements.append(line.strip())

setup(
    name="MLSwag",
    version="0.0.1dev0",
    author="Nikhil Fulzele",
    author_email="nikhilf99@gmail.com",
    description="A simple wrapper around ml-model tools to track the parameters, training time and metrics.",
    license="MIT",
    packages = packages,
    install_requires=requirements
)
