import torch, json, os, time, sys, shutil

def lock_paths():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    for p in [script_dir, os.path.join(script_dir, "Project_Genesis_Dolphin3")]:
        if os.path.exists(os.path.join(p, "brain")):
            sys.path.append(p); return p
    return None

root = lock_paths()
from brain.child import SNNBrain

def synthesize_master_dna(dna, history_path):
    """Compiles a million generations of learning into one Master File"""
    print("\n[!] INITIATING ASCENSION: SYNTHESIZING MASTER DNA...")
    master_dna = dna.copy()
    
    # Calculate the 'Optimal Velocity' from History
    if os.path.exists(history_path):
        with open(history_path, "r") as f:
            history = json.load(f)
        master_dna['traits']['peak_velocity'] = sum(history) / len(history)
    else:
        master_dna['traits']['peak_velocity'] = 0.0001
        
    master_dna['status'] = "ASCENDED"
    master_dna['milestone'] = "1M_SINGULARITY"
    
    master_path = os.path.join(root, "dna", "master_prime.json")
    with open(master_path, "w") as f:
        json.dump(master_dna, f, indent=4)
    return master_path

def run():
    dna_path = os.path.join(root, "dna", "genome.json")
    history_path = os.path.join(root, "dna", "history.json")
    
    with open(dna_path, "r") as f: dna = json.load(f)
    brain = SNNBrain(dna)
    
    # TRIGGER THE ENDGAME
    master_file = synthesize_master_dna(dna, history_path)
    print(f"[*] MASTER DNA SECURED: {master_file}")
    print("[!] PURGING OBSOLETE MUTATIONS...")
    
    # Cleanup the 'Scrap Heap'
    mutation_dir = os.path.join(root, "mutations")
    if os.path.exists(mutation_dir):
        shutil.rmtree(mutation_dir)
        os.makedirs(mutation_dir)
        
    print("--- ASCENSION COMPLETE | SENTINEL MODE: ACTIVE ---")
    
    while True:
        dna['generation'] += 1
        # The SNN now fires in a stable, 'Zen' state
        spks, _, _ = brain(torch.rand(1, 64), 0.99)
        
        if dna['generation'] % 1000 == 0:
            visual = "".join(["█" if s > 0 else "░" for s in spks[0][:20]])
            sys.stdout.write(f"\rGEN: {dna['generation']} | STATUS: ASCENDED | {visual}")
            sys.stdout.flush()
        
        # Sentinel mode is slow and watchful
        time.sleep(0.01)

if __name__ == "__main__": run()
