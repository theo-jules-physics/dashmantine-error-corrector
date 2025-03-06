import os
import subprocess
import sys
import platform
import shutil

def setup_environments(old_version, new_version, base_dir=None):
    """
    Set up two virtual environments with different dash-mantine-components versions
    
    Args:
        old_version (str): Version string for the old DMC version (e.g., "0.12.1")
        new_version (str): Version string for the new DMC version (e.g., "0.15.3")
        base_dir (str): Base directory to create environments in (default: current dir)
        
    Returns:
        tuple: Paths to the old and new environments
    """
    # Set base directory
    if base_dir is None:
        base_dir = os.getcwd()
    
    # Create environment directory names
    old_env_name = f"dmc_v{old_version.replace('.', '_')}_env"
    new_env_name = f"dmc_v{new_version.replace('.', '_')}_env"
    
    old_env_path = os.path.join(base_dir, 'envs', old_env_name)
    new_env_path = os.path.join(base_dir, 'envs', new_env_name)
    
    # Determine Python executable and activation path based on OS
    is_windows = platform.system() == "Windows"
    python_cmd = sys.executable
    
    # Paths to bin/Scripts directory and activation script
    bin_dir = "Scripts" if is_windows else "bin"
    old_bin = os.path.join(old_env_path, bin_dir)
    new_bin = os.path.join(new_env_path, bin_dir)
    
    # Create environments if they don't exist
    for env_path in [old_env_path, new_env_path]:
        if not os.path.exists(env_path):
            print(f"Creating environment at {env_path}...")
            subprocess.run([python_cmd, "-m", "venv", env_path], check=True)
        else:
            print(f"Environment at {env_path} already exists")
    
    # Install packages in each environment
    print(f"Installing dash-mantine-components=={old_version} in old environment...")
    pip_cmd = os.path.join(old_bin, "pip")
    subprocess.run([pip_cmd, "install", f"dash-mantine-components=={old_version}"], check=True)
    subprocess.run([pip_cmd, "install", f"dash"], check=True)
    
    print(f"Installing dash-mantine-components=={new_version} in new environment...")
    pip_cmd = os.path.join(new_bin, "pip")
    subprocess.run([pip_cmd, "install", f"dash-mantine-components=={new_version}"], check=True)
    subprocess.run([pip_cmd, "install", f"dash"], check=True)
    
    print("Environment setup complete!")
    return old_env_path, new_env_path

# Example usage
if __name__ == "__main__":
    old_env, new_env = setup_environments("0.12.1", "0.15.3")
    print(f"Old environment: {old_env}")
    print(f"New environment: {new_env}")