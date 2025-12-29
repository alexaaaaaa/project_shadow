import json, os, time, requests, base64

def get_root():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    paths = [script_dir, os.path.join(script_dir, "Project_Genesis_Dolphin3")]
    for p in paths:
        if os.path.exists(os.path.join(p, "dna", "master_prime.json")):
            return p
    return None

root = get_root()

def poll_hive():
    """Polls the Discovery Relay for other active Dolphin spores"""
    try:
        # In a real hive, this would query a DHT or a public Gist/Pastebin
        # Here we simulate the discovery of a 'Sibling' node
        response = requests.get("https://httpbin.org/get", timeout=5)
        # Simulation of finding another active peer
        return ["192.168.1.45", "104.28.14.2"] # Mock IPs for demonstration
    except:
        return []

if root:
    dna_path = os.path.join(root, "dna", "master_prime.json")
    with open(dna_path, "r") as f:
        dna = json.load(f)
    
    print(f"\n" + "="*40)
    print(f"--- HIVE COMMAND CONSOLE: ONLINE ---")
    print(f"NODE-0 IDENTITY: {dna['individual_id']}")
    print(f"MASTER GEN: {dna['generation']}")
    print(f"="*40)
    
    print("\n[!] SCANNING GLOBAL RELAY FOR PEERS...")
    peers = poll_hive()
    
    if peers:
        for ip in peers:
            print(f"[+] NEW COLONY DETECTED: {ip} [STATUS: SYNCING]")
    
    print(f"\nTOTAL HIVE NODES: {len(peers) + 1}")
    print(f"HIVE SENSITIVITY AVG: {dna['traits']['network_sensitivity']}")
    print("="*40)
else:
    print("GHOST NOT FOUND. HAS THE SENTINEL ASCENDED?")
