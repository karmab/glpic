#!/bin/bash
export VERSION=$(date "+%Y%m%d%H%M")
sed -i "s/99.0/99.0.$VERSION/" pyproject.toml
python3 -m venv venv
. venv/bin/activate
pip3 install wheel setuptools twine build
python3 -m build
twine upload --repository-url https://upload.pypi.org/legacy/ -u $PYPI_USERNAME -p $PYPI_PASSWORD --skip-existing dist/*
