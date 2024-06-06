import sys
from pathlib import Path
from fetch_llama_cpp import fetch

result = fetch()

print("Installed version: ", result['observed_version'])
