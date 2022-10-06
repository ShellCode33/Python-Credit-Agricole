#!/usr/bin/python3
# coding: utf-8

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='credit-agricole',
    version='0.1.1',
    description='Python library that allows you to retrieve bank details from the Credit Agricole website',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords="credit agricole bank account card loan insurance",
    license="MIT",
    author='ShellCode',
    author_email='shellcode33@protonmail.ch',
    url='https://github.com/ShellCode33/Python-Credit-Agricole',
    packages=find_packages(),
    python_requires='>=3.6',

    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        'License :: OSI Approved :: MIT License',
        "Operating System :: POSIX :: Linux",
    ],

    install_requires=[
        "requests"
    ],

    entry_points={
        "console_scripts": [
            "creditagricole = creditagricole.cli:main",
        ]
    }
)
