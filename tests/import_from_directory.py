import sys
from pathlib import Path

# Add the correct parent directory to the sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from fetch_llama_cpp import fetch

result = fetch()

print("Installed version: ", result['observed_version'])
