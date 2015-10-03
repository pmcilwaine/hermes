# /usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

root_dir = os.path.dirname(__file__)

if root_dir != "":
    os.chdir(root_dir)


def read(filename):
    buf = []
    with open(filename, 'r') as r:
        buf.append(r.read())
    return '\n'.join(buf)

install_requires = []
with open('requirements.txt') as f:
    for line in f:
        install_requires.append(line)

setup(
    name='hermes_cms',
    version='0.9.0',
    description='Hermes CMS',
    long_description=read('README.md'),
    author='Paul Mcilwaine',
    url='https://github.com/pmcilwaine/hermes',
    packages=find_packages(exclude='tests'),
    entry_points={
        'console_scripts': [
            'hermes_service = hermes_cms.service.cmdline.runner:main'
        ]
    },
    include_package_data=True,
    install_requires=install_requires
)
