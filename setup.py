#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="llama_cpp_fetcher",
    version="0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'llama_cpp_fetcher = llama_cpp_fetcher:fetch',
        ],
    },
)
