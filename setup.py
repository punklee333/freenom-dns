# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='freenom_dns',
    version='1.0.0',
    url='https://github.com/PunkLee2py/freenom-dns',
    author='Punk Lee',
    author_email='punklee333@gmail.com',
    description='An unofficial python implementation for managing freenom_dns.com dns records.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    license='MIT',
    install_requires=['requests', 'lxml', 'retrying']
)
