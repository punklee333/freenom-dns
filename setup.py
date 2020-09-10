# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import freenom_dns

name = freenom_dns.__name__
version = freenom_dns.__version__
with open("README.md", "r") as f:
    long_description = f.read()
install_requires = ["requests>=2.24.0", "retrying>=1.3.3", "lxml>=4.5.2"]

setup(name=name,
      version=version,
      author='Punk Lee',
      author_email='punklee333@gmail.com',
      description='An unofficial python implementation for managing freenom.com dns records.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/PunkLee2py/freenom-dns',
      license='MIT',
      python_requires='>=3.6',
      packages=find_packages(),
      install_requires=install_requires)
