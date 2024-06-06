# -*- coding: utf-8 -*-
""" 
Allows users to execute the module itself from the command line to fetch
the latest and best version of llama.cpp for their system:

  python -m llama_cpp_fetcher

"""
from .llama_cpp_fetcher import fetch

if __name__ == "__main__":
    fetch()
