# latest-llama-cpp

This Python script automates the process of downloading and setting up the best binary distribution of `llama.cpp` for your system and graphics card (if present).

It fetches the latest release from GitHub, detects your system's specifications, and selects the most suitable binary for your setup.

## Features

- **Automatic Detection**: Detects your operating system, architecture, and GPU (NVIDIA or AMD).
- **CUDA Compatibility**: Checks for CUDA and driver versions to ensure compatibility.
- **AVX Support**: Checks for AVX, AVX2, and AVX512 support on your CPU.
- **Download and Extraction**: Downloads the appropriate binary and extracts it.
- **Verification**: Runs the binary with `--version` to verify the setup.

## Requirements

- Python 3.x
- `requests` library
- `cpuinfo` library
- `zipfile` and `tarfile` modules
- `subprocess` and `platform` modules

## Usage

1. **POSIX (Linux, macOS, etc.)**:
    ```bash
    % python -m venv .venv
    % source ./.venv/bin/activate
    (.venv) % pip install -r requirements.txt
    (.venv) % ./latest-llama-cpp.py
    ```

2. **Windows**:
    ```bash
    > python -m venv .venv
    > .\.venv\Scripts\avtivate.ps1
    > pip install -r requirements.txt
    > python latest-llama-cpp.py
    ```

## How It Works

1. **Fetch Latest Release**: The script fetches the latest release information from the `llama.cpp` GitHub repository.
2. **System Information**: It detects your operating system and architecture.
3. **GPU Detection**: Checks for NVIDIA or AMD GPUs and their respective CUDA and driver versions.
4. **AVX Support**: Checks if your CPU supports AVX, AVX2, or AVX512.
5. **Select Best Asset**: Based on the detected information, it selects the most suitable binary asset.
6. **Download and Extract**: Downloads the selected binary and extracts it to the specified directory.
7. **Run Verification**: Runs the binary with `--version` to ensure it was set up correctly.

## Testing

A Containerfile has been included for limited testing on Linux:

    ```
    % podman build -t latest-llama-cpp .
    % podman run -it latest-llama-cpp
```

## Notes

- Ensure you have the necessary permissions to run `nvidia-smi` and `lspci` commands.
- The script assumes a standard directory structure for the downloaded and extracted files.

## License

This project is licensed under the MIT License.

