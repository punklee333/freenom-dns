# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

import freenom_dns

rootdir = path.abspath(path.dirname(__file__))
# Get the long description from the README file
with open(path.join(rootdir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

_version = freenom_dns.__version__
setup(
    name=f'freenom_dns_{_version}',
    version=_version,
    url='https://github.com/PunkLee2py/freenom-dns',
    author='Punk Lee',
    author_email='punklee333@gmail.com',
    description='An unofficial python implementation for managing freenom.com dns records.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    license='MIT',
    install_requires=['requests', 'lxml', 'retrying']
)