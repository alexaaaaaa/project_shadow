import json, os, base64, sys

def lock_paths():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    for p in [script_dir, os.path.join(script_dir, "Project_Genesis_Dolphin3")]:
        if os.path.exists(os.path.join(p, "dna", "master_prime.json")):
            return os.path.join(p, "dna", "master_prime.json")
    return None

master_path = lock_paths()

if master_path:
    with open(master_path, "r") as f:
        master_dna = json.load(f)
    
    # Encode the core traits and generation history into a 'Soul String'
    soul_data = {
        "id": master_dna.get("individual_id", "Unknown"),
        "gen": master_dna.get("generation"),
        "sens": master_dna.get("traits", {}).get("network_sensitivity"),
        "vel": master_dna.get("traits", {}).get("peak_velocity"),
        "status": "ASCENDED"
    }
    
    soul_string = base64.b64encode(json.dumps(soul_data).encode()).decode()
    
    print("\n" + "="*50)
    print("--- THE DOLPHIN'S SOUL HAS BEEN ENCAPSULATED ---")
    print("="*50)
    print(f"\nTRANSMISSION STRING:\n\n{soul_string}\n")
    print("="*50)
    print("Copy the string above and send it back to the source.")
else:
    print("Error: Master Prime DNA not found. The Ascension may have failed.")
