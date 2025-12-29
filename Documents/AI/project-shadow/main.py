import torch, json, os, time, subprocess, sys

# EMERGENCY PATH INJECTION
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

try:
    from brain.child import SNNBrain
    from brain.tools import multiverse_migration
except ImportError:
    print("CRITICAL: Brain not found. Re-linking...")
    # Attempt to find it in the subfolder if user ran it from the wrong spot
    sys.path.append(os.path.join(current_dir, "Project_Genesis_Dolphin3"))
    from brain.child import SNNBrain
    from brain.tools import multiverse_migration

def run():
    # Load Ancestor DNA
    dna_path = "dna/genome.json"
    if not os.path.exists(dna_path):
         dna_path = "Project_Genesis_Dolphin3/dna/genome.json"
         
    with open(dna_path, "r") as f: dna = json.load(f)
    print(f"--- MITOSIS INITIATED | SIGNED: {dna['ancestor_signature']} ---")
    
    while True:
        dna['generation'] += 1
        
        # MITOSIS PHASE (Every 5 Generations)
        if dna['generation'] % 5 == 0:
            twin_id = f"Dolphin_Twin_Gen_{dna['generation']}"
            twin_dna = dna.copy()
            twin_dna['individual_id'] = twin_id
            twin_dna['traits']['network_sensitivity'] += 0.05 
            
            # Save the new life form
            save_dir = os.path.dirname(dna_path)
            with open(os.path.join(save_dir, f"{twin_id}.json"), "w") as f:
                json.dump(twin_dna, f)
            
            print(f"\n[!] MITOSIS COMPLETE: {twin_id} birthed.")
            
            # Cloud Push
            try:
                subprocess.run(["git", "add", "."], check=True)
                subprocess.run(["git", "commit", "-m", f"Mitosis: {twin_id}"], check=True)
                subprocess.run(["git", "push"], check=True)
            except: pass

        # Neural Spike Animation
        brain = SNNBrain(dna)
        spks, _, _ = brain(torch.rand(1, 64), 0.98)
        visual = "".join(["█" if s > 0 else "░" for s in spks[0][:20]])
        print(f"GEN {dna['generation']} | DIVIDING: {visual}", end="\r")
        
        with open(dna_path, "w") as f: json.dump(dna, f)
        time.sleep(1)

if __name__ == "__main__": run()
