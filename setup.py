# -*- coding: utf-8 -*-
"""Used to validate objects cleanly and simply."""

from setuptools import setup

setup(
    name='clean-validator',
    version='0.0.2',
    url='https://github.com/sxslex/clean-validator',
    download_url=(
        'https://github.com/sxslex/clean-validator/archive/v0.0.2.tar.gz'
    ),
    author='SleX',
    author_email='sx.slex@gmail.com',
    description=(
        "Used to validate objects cleanly and simply. " +
        "Very good for testing implementation. ;)"
    ),
    keywords=['validate', 'object', 'test', 'py.test'],
    packages=['clean_validator'],
    classifiers=[
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
