#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Wikimedia Foundation and contributors
# Copyright (c) 2017 Yuvi Panda
# License: Apache-2.0

import os
from setuptools import find_packages
from setuptools import setup

VERSION = '0.0.1'

setup(
    name='wmcs.hgg',
    version=VERSION,
    description=(
        'Helper scripts for creating and using lists of '
        'Wikimedia Cloud VPS project hosts.'
    ),
    long_description=open(
        os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: System :: Distributed Computing',
        'Topic :: System :: Systems Administration',
    ],
    packages=find_packages(),
    install_requires=[
        'PyYAML',  # MIT
    ],
    entry_points={
        'console_scripts': [
            'wmcs-hgg=wmcs.hgg.generator:main',
            'wmcs-source=wmcs.hgg.source:main',
        ],
    },
)
