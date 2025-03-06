import os
import subprocess
import sys
import platform


def setup_environments(package_name, versions: list[str], mandatory_packages=[], envs_dir=None):
    # Set base directory
    if envs_dir is None:
        envs_dir = os.path.join(os.getcwd(), 'envs')

    # Determine Python executable and activation path based on OS
    is_windows = platform.system() == "Windows"
    python_cmd = sys.executable
    bin_dir = "Scripts" if is_windows else "bin"

    for version in versions:
        version_env_name = f"{package_name}_v{version.replace('.', '_')}_env"
        version_env_path = os.path.join(envs_dir, version_env_name)
        bin_path = os.path.join(version_env_path, bin_dir)
        if not os.path.exists(version_env_path):
            print(f"Creating environment at {version_env_path}...")
            subprocess.run([python_cmd, "-m", "venv", version_env_path], check=True)
        else:
            print(f"Environment at {version_env_path} already exists")

        print(f"Installing {package_name}=={version} in environment...")
        pip_cmd = os.path.join(bin_path, "pip")
        subprocess.run([pip_cmd, "install", f"{package_name} == {version}"], check=True)
        for package in mandatory_packages:
            print(f"Installing {package} in environment...")
            subprocess.run([pip_cmd, "install", package], check=True)
    
    print("Environment setup complete!")
    return [os.path.join(envs_dir, f"{package_name}_v{version.replace('.', '_')}_env") for version in versions]
