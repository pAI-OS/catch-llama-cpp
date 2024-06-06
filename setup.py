#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="fetch_llama_cpp",
    version="0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'fetch_llama_cpp = fetch_llama_cpp:fetch',
        ],
    },
)
