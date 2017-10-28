"""
To make release:
    python setup.py sdist
Installation:
    python setup.py install
"""

from distutils.core import setup
from setuptools import find_packages

setup(
    name='pydaemon',
    version='1.0',
    packages=find_packages(),
    license=open('LICENSE.txt').read(),
    long_description=open('README.md').read(),
    scripts=['bin/pydaemon'],
    install_requires=[
        'colorama',
        'termcolor',
        'pyyaml',
    ],
)
