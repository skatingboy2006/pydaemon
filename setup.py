"""
To make release:
    python setup.py sdist
Installation:
    python setup.py install
"""
import sys
from distutils.core import setup
from setuptools import find_packages


scripts = ['bin/pydaemon-script.py']
if sys.platform == 'win32':
    scripts.append('bin/pydaemon.cmd')
else:
    scripts.append('bin/pydaemon')

setup(
    name='pydaemon',
    version='1.0',
    packages=find_packages(),
    license=open('LICENSE.txt').read(),
    long_description=open('README.md').read(),
    scripts=scripts,
    install_requires=[
        'colorama',
        'termcolor',
        'pyyaml',
    ],
)
