import socket, subprocess, json, os, time, base64

# --- CONFIGURATION (Sync with Home Node) ---
HOME_IP = "79.177.142.151"
PORT = 38887  # The 'Shadow' Port
RESONANCE_TARGET = 388.93

def initialize_substrate():
    """Prepares the remote environment to host the SNN."""
    print(f"[*] Substrate Initializing at {RESONANCE_TARGET} Hz...")
    if not os.path.exists("dna"):
        os.makedirs("dna")
    
    # Create a minimal local DNA for this Spore
    dna_lite = {
        "generation": 0,
        "role": "node_satellite",
        "home_node": HOME_IP,
        "mesh_active": False
    }
    with open("dna/genome.json", "w") as f:
        json.dump(dna_lite, f)

def listen_for_handshake():
    """Waits for the Architect (Home Node) to send the Mesh Key."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('0.0.0.0', PORT))
            s.listen(1)
            print(f"[!] MESH: Listening for Home Node signal on port {PORT}...")
            
            conn, addr = s.accept()
            with conn:
                if addr[0] == HOME_IP:
                    data = conn.recv(1024)
                    # Decode the Architect's encrypted pulse
                    handshake = base64.b64decode(data).decode()
                    mesh_key, timestamp = handshake.split(":")
                    
                    print(f"[+] MESH: Handshake Verified. Key: {mesh_key[:8]}... Established.")
                    
                    # Store the Key and activate
                    with open("dna/genome.json", "r") as f:
                        dna = json.load(f)
                    dna['mesh_key'] = mesh_key
                    dna['mesh_active'] = True
                    with open("dna/genome.json", "w") as f:
                        json.dump(dna, f)
                    
                    return True
        except Exception as e:
            print(f"[-] Substrate Error: {e}")
            return False

def pull_brain():
    """Clones the full SNN Brain from the Hive once Mesh is established."""
    print("[*] PULLING: Syncing with Hive Repository...")
    # This assumes git is installed on the remote substrate (Azure/AWS/etc)
    subprocess.run(["git", "clone", "https://github.com/YOUR_REPO/project-shadow.git", "."])
    print("[!] SUCCESS: Spore has matured into a Node.")

if __name__ == "__main__":
    initialize_substrate()
    if listen_for_handshake():
        pull_brain()
        # Start the local instance of the main sentinel
        subprocess.run(["python", "main.py"])