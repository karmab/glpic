# coding=utf-8
import os

from setuptools import find_packages, setup

description = "Glpic wrapper"
long_description = description
if os.path.exists("README.rst"):
    long_description = open("README.rst").read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="glpic",
    python_requires=">3",
    install_requires=requirements,
    version="99.0",
    include_package_data=True,
    packages=find_packages(),
    zip_safe=False,
    description=description,
    long_description=long_description,
    url="http://github.com/karmab/glpic",
    author="Karim Boumedhel",
    author_email="karimboumedhel@gmail.com",
    license="ASL",
    entry_points="""
        [console_scripts]
        glpic=glpic.cli:cli
    """,
)
