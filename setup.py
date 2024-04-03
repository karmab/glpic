# coding=utf-8
from setuptools import setup, find_packages

import os
INSTALL = ['requests']

description = 'Glpic wrapper'
long_description = description
if os.path.exists('README.rst'):
    long_description = open('README.rst').read()

setup(
    name='glpic',
    version='99.0',
    include_package_data=True,
    packages=find_packages(),
    zip_safe=False,
    description=description,
    long_description=long_description,
    url='http://github.com/karmab/glpic',
    author='Karim Boumedhel',
    author_email='karimboumedhel@gmail.com',
    license='ASL',
    install_requires=['prettytable'],
    entry_points='''
        [console_scripts]
        glpic=glpic.cli:cli
    ''',
)
