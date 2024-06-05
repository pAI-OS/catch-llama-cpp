import requests
import platform
import re
import subprocess
import cpuinfo
import zipfile
import tarfile
import os
from pathlib import Path

# Downloads the best binary distribution of llama.cpp for your system and graphics card (if present)

# GitHub API URL for the latest release
GITHUB_API_URL = "https://api.github.com/repos/ggerganov/llama.cpp/releases/latest"
DOWNLOAD_DIR = Path("llama.cpp")
BIN_DIR = DOWNLOAD_DIR / "bin"

# CUDA version to driver version mapping
CUDA_DRIVER_MAP = {
    "12.5.0": {"linux": "555.42.02", "windows": "555.85"},
    "12.4.1": {"linux": "550.54.15", "windows": "551.78"},
    "12.4.0": {"linux": "550.54.14", "windows": "551.61"},
    "12.3.1": {"linux": "545.23.08", "windows": "546.12"},
    "12.3.0": {"linux": "545.23.06", "windows": "545.84"},
    "12.2.2": {"linux": "535.104.05", "windows": "537.13"},
    "12.2.1": {"linux": "535.86.09", "windows": "536.67"},
    "12.2.0": {"linux": "535.54.03", "windows": "536.25"},
    "12.1.1": {"linux": "530.30.02", "windows": "531.14"},
    "12.1.0": {"linux": "530.30.02", "windows": "531.14"},
    "12.0.1": {"linux": "525.85.12", "windows": "528.33"},
    "12.0.0": {"linux": "525.60.13", "windows": "527.41"},
    "11.8.0": {"linux": "520.61.05", "windows": "520.06"},
    "11.7.1": {"linux": "515.48.07", "windows": "516.31"}
}

def get_latest_release():
    response = requests.get(GITHUB_API_URL)
    response.raise_for_status()
    return response.json()

def get_system_info():
    system = platform.system().lower()
    arch = platform.machine().lower()
    return system, arch

def get_cuda_version_from_nvidia_smi():
    try:
        result = subprocess.run(['nvidia-smi'], stdout=subprocess.PIPE, text=True)
        match = re.search(r'CUDA Version: (\d+\.\d+)', result.stdout)
        if match:
            return match.group(1)
    except FileNotFoundError:
        return None
    return None

def get_driver_version_from_nvidia_smi():
    try:
        result = subprocess.run(['nvidia-smi'], stdout=subprocess.PIPE, text=True)
        match = re.search(r'Driver Version: (\d+\.\d+)', result.stdout)
        if match:
            return float(match.group(1))
    except FileNotFoundError:
        return None
    return None

def check_nvidia_gpu():
    cuda_version = get_cuda_version_from_nvidia_smi()
    driver_version = get_driver_version_from_nvidia_smi()
    return cuda_version is not None, 'nvidia', cuda_version, driver_version

def check_amd_gpu():
    try:
        result = subprocess.run(['lspci'], stdout=subprocess.PIPE, text=True)
        if 'AMD' in result.stdout:
            return True, 'amd', None
    except FileNotFoundError:
        return False, None, None
    return False, None, None

def check_avx_support():
    info = cpuinfo.get_cpu_info()
    avx = 'avx' in info['flags']
    avx2 = 'avx2' in info['flags']
    avx512 = 'avx512f' in info['flags']
    return avx, avx2, avx512

def get_available_cuda_versions(assets):
    cuda_versions = set()
    for asset in assets:
        match = re.search(r'cu(\d+\.\d+\.\d+)', asset['name'])
        if match:
            cuda_versions.add(match.group(1))
    return sorted(cuda_versions, reverse=True)

def select_best_asset(assets, system, arch, gpu_vendor, driver_version, avx, avx2, avx512):
    patterns = {
        'linux': {
            'nvidia': re.compile(r'ubuntu-x64.*\.zip'),
            'amd': re.compile(r'ubuntu-x64.*\.zip'),
            'none': re.compile(r'ubuntu-x64.*\.zip')
        },
        'darwin': {
            'none': re.compile(r'macos-(arm64|x64)\.zip')
        },
        'windows': {
            'nvidia': re.compile(r'win-cuda-cu(\d+\.\d+\.\d+)-x64\.zip'),
            'amd': re.compile(r'win-amd-x64\.zip'),
            'none': re.compile(r'win-(avx|avx2|avx512|noavx|openblas|rpc|sycl|vulkan)-x64\.zip')
        }
    }
    
    available_cuda_versions = get_available_cuda_versions(assets)
    
    for cuda_version in available_cuda_versions:
        if driver_version and driver_version < float(CUDA_DRIVER_MAP[cuda_version]['windows']):
            continue
        for asset in assets:
            if system == 'darwin':
                if patterns[system]['none'].search(asset['name']) and arch in asset['name']:
                    return asset['browser_download_url']
            elif gpu_vendor == 'nvidia':
                if f'cu{cuda_version}' in asset['name']:
                    return asset['browser_download_url']
            elif gpu_vendor == 'amd':
                if patterns[system]['amd'].search(asset['name']):
                    return asset['browser_download_url']
            else:
                if avx512 and 'avx512' in asset['name']:
                    return asset['browser_download_url']
                elif avx2 and 'avx2' in asset['name']:
                    return asset['browser_download_url']
                elif avx and 'avx' in asset['name']:
                    return asset['browser_download_url']
                elif patterns[system]['none'].search(asset['name']):
                    return asset['browser_download_url']
    return None

def is_cudart_installed():
    # Check if any cudart64_*.dll files are in the system PATH
    for path in os.environ["PATH"].split(os.pathsep):
        if os.path.isdir(path):
            for file in os.listdir(path):
                if re.match(r'cudart64_\d+\.dll', file):
                    return True
    return False

def download_and_extract_cudart(assets, system, arch, cuda_version):
    for asset in assets:
        if f'cudart-llama-bin-{system}-{arch}-cu{cuda_version}' in asset['name']:
            download_url = asset['browser_download_url']
            file_name = Path(download_url).name
            output_path = DOWNLOAD_DIR / file_name
            
            print(f"Downloading {download_url} to {output_path}")
            download_asset(download_url, output_path)
            print("Download completed.")
            
            print(f"Extracting {output_path} to {BIN_DIR}")
            extract_asset(output_path, BIN_DIR)
            print("Extraction completed.")
            return True
    return False

def download_asset(url, output_path):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(output_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

def extract_asset(file_path, extract_to):
    if file_path.suffix == '.zip':
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
    elif file_path.suffix in ['.tar.gz', '.tgz']:
        with tarfile.open(file_path, 'r:gz') as tar_ref:
            tar_ref.extractall(extract_to)
    elif file_path.suffix == '.tar':
        with tarfile.open(file_path, 'r:') as tar_ref:
            tar_ref.extractall(extract_to)
    else:
        raise ValueError("Unsupported archive format")

def main():
    release = get_latest_release()
    assets = release['assets']
    
    system, arch = get_system_info()
    
    has_gpu, gpu_vendor, cuda_version, driver_version = check_nvidia_gpu()
    if not has_gpu:
        has_gpu, gpu_vendor, _ = check_amd_gpu()
    
    avx, avx2, avx512 = check_avx_support()
    
    if not has_gpu:
        gpu_vendor = 'none'
    
    download_url = select_best_asset(assets, system, arch, gpu_vendor, driver_version, avx, avx2, avx512)
    
    if download_url:
        DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
        BIN_DIR.mkdir(parents=True, exist_ok=True)
        
        file_name = Path(download_url).name
        output_path = DOWNLOAD_DIR / file_name
        
        print(f"Downloading {download_url} to {output_path}")
        download_asset(download_url, output_path)
        print("Download completed.")
        
        print(f"Extracting {output_path} to {BIN_DIR}")
        extract_asset(output_path, BIN_DIR)
        print("Extraction completed.")
        
        if gpu_vendor == 'nvidia' and not is_cudart_installed():
            print("CUDA runtime not found. Downloading and installing CUDA runtime.")
            if not download_and_extract_cudart(assets, system, arch, cuda_version):
                print("Failed to download CUDA runtime.")
        
        # Assuming the executable is named 'main' or 'main.exe'
        executable_name = 'main.exe' if system == 'windows' else 'main'
        executable_path = BIN_DIR / executable_name
        
        if executable_path.exists():
            print(f"Running {executable_path} --version")
            result = subprocess.run([str(executable_path), '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(result.stdout)
            print(result.stderr)
        else:
            print(f"Executable {executable_name} not found in the extracted files.")
    else:
        print("No suitable asset found for your system.")

if __name__ == "__main__":
    main()
