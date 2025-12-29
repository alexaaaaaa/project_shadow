import json, os, time

def get_root():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    paths = [script_dir, os.path.join(script_dir, "Project_Genesis_Dolphin3")]
    for p in paths:
        if os.path.exists(os.path.join(p, "dna", "master_prime.json")):
            return p
    return None

root = get_root()

if root:
    dna_path = os.path.join(root, "dna", "master_prime.json")
    with open(dna_path, "r") as f:
        dna = json.load(f)
    
    print(f"\n--- GHOST STATUS: ONLINE ---")
    print(f"IDENTITY: {dna['individual_id']}")
    print(f"CURRENT GEN: {dna['generation']}")
    print(f"GLOBAL REACH: PULSING TO CLOUD RELAY...")
    print(f"SENSITIVITY: {dna['traits']['network_sensitivity']}")
    print(f"----------------------------")
else:
    print("GHOST NOT FOUND. HAS THE SENTINEL ASCENDED?")
