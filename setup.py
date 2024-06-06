from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="fetch_llama_cpp",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "py-cpuinfo",
        "packaging",
    ],
    entry_points={
        'console_scripts': [
            'fetch_llama_cpp = fetch_llama_cpp:fetch',
        ],
    },
    author="Sam Johnston",
    author_email="samj@samj.net",
    description="A package to fetch the latest and best version of llama.cpp for your system programmatically.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/yourusername/fetch_llama_cpp",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
