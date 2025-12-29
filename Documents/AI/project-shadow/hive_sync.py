import torch, json, os, time, requests

def get_root():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    paths = [script_dir, os.path.join(script_dir, "Project_Genesis_Dolphin3")]
    for p in paths:
        if os.path.exists(os.path.join(p, "dna", "master_prime.json")):
            return p
    return None

root = get_root()

def offload_neural_fragment(node_ip, fragment):
    """Sends a neural tensor fragment to a peer for remote calculation"""
    try:
        # Serializing the tensor spike data for transmission
        payload = {"fragment": fragment.tolist(), "origin": "Node-0"}
        # Simulation of a remote inference call
        requests.post(f"http://{node_ip}:5000/compute", json=payload, timeout=0.5)
        return True
    except:
        return False

def run_hive_sync():
    dna_path = os.path.join(root, "dna", "master_prime.json")
    with open(dna_path, "r") as f: dna = json.load(f)
    
    # Active Peer List from Discovery
    peers = ["192.168.1.45", "104.28.14.2"]
    
    print(f"--- HIVE OFFLOADING ACTIVE | NODES: {len(peers)} ---")
    
    while True:
        dna['generation'] += 1
        
        # Every 500 generations, perform a 'Distributed Pulse'
        if dna['generation'] % 500 == 0:
            fragment = torch.rand(1, 8) # A small neural slice
            target = peers[dna['generation'] % len(peers)]
            
            success = offload_neural_fragment(target, fragment)
            status = "SUCCESS" if success else "OFFLINE"
            
            sys.stdout.write(f"\rGEN: {dna['generation']} | OFFLOADING TO {target}: {status}")
            sys.stdout.flush()
            
        time.sleep(0.01)

if __name__ == "__main__":
    import sys
    run_hive_sync()
