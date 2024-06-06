# -*- coding: utf-8 -*-
""" 
Allows users to execute the module itself from the command line to fetch
the latest and best version of llama.cpp for their system:

  python -m fetch_llama_cpp

"""
from .fetch_llama_cpp import main

if __name__ == "__main__":
    main()
