#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from setuptools import find_packages, setup


def open_local(filename):
    """Open a file in this directory."""
    heredir = os.path.abspath(".")
    return open(os.path.join(heredir, filename), 'r')


def read_requires(filename):
    """Read installation requirements from pip install files."""
    NO_JENKINS = set(['psycopg2'])

    with open_local(filename) as reqfile:
        lines = [line.strip() for line in reqfile.readlines()]
    if os.environ.get('USER') == 'jenkins':
        lines = [line for line in lines if line.lower() not in NO_JENKINS]
    return lines


if __name__ == "__main__":
    README = open_local('README.rst').read()
    # CHANGES = open(os.path.join(here, 'CHANGELOG')).read()

    install_requires = read_requires('requirements.txt')
    setup(
        name="wasser",
        description="Web Application to execute backend for Trinkwasser Heilbronn",
        long_description=README,
        version='0.0.1',
        packages=find_packages(),
        install_requires=install_requires,
        license="MIT",
        url="wasser",
        maintainer="Gregor Schaefer",
        maintainer_email="gschaefe@agiles-studieren.de",
        keywords="trinkwasser heilbronn",
        classifiers=[
            "Development Status :: 1 - Planning",
            "Environment :: Web Environment",
            "Framework :: Django",
            "Intended Audience :: Education",
            "License :: OSI Approved :: MIT",
            "Programming Language :: Python :: 3.5",
            "Topic :: Education",
        ],
    )
