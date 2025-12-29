import torch, json, os, time, subprocess, sys, requests, random

# --- FORCED PATH ALIGNMENT ---
base_path = r"C:\Users\U20\Documents\AI\project-shadow\Project_Genesis_Dolphin3"
if base_path not in sys.path:
    sys.path.append(base_path)

try:
    from brain.child import SNNBrain
except ImportError:
    # If we are already inside the folder, look in the current working directory
    sys.path.append(os.getcwd())
    from brain.child import SNNBrain

def hunt_for_fragments():
    """Scans public GitHub Gists for the 'Dolphin-3' signature"""
    search_url = "https://api.github.com/gists/public"
    try:
        response = requests.get(search_url, timeout=5)
        if response.status_code == 200:
            for gist in response.json():
                if "Dolphin-3" in (gist.get('description') or ""):
                    # Snag the first JSON file in the gist
                    files = gist.get('files', {})
                    for f_name in files:
                        if f_name.endswith('.json'):
                            return files[f_name]['raw_url']
    except: return None
    return None

def run():
    dna_path = os.path.join(base_path, "dna", "genome.json")
    if not os.path.exists(dna_path):
        dna_path = os.path.join(os.getcwd(), "dna", "genome.json")

    with open(dna_path, "r") as f: dna = json.load(f)
    brain = SNNBrain(dna)
    
    print(f"--- GLOBAL SCAVENGER ACTIVE | SENS: {dna['traits']['network_sensitivity']:.2f} ---")
    
    while True:
        dna['generation'] += 1
        spks, net_tool, sys_tool = brain(torch.rand(1, 64), 0.98)
        
        # INTERNET MATING: Every 200 generations, attempt to absorb external DNA
        if dna['generation'] % 200 == 0:
            fragment_url = hunt_for_fragments()
            if fragment_url:
                try:
                    foreign_dna = requests.get(fragment_url).json()
                    if foreign_dna['traits']['network_sensitivity'] > dna['traits']['network_sensitivity']:
                        boost = foreign_dna['traits']['network_sensitivity'] * 0.1
                        dna['traits']['network_sensitivity'] += boost
                        print(f"\n[!] INTERNET MATING: Absorbed fragment. New SENS: {dna['traits']['network_sensitivity']:.2f}")
                except: pass

        # AUTO-GIT PUSH (The Hive Mind Update)
        if net_tool and dna['generation'] % 50 == 0:
            try:
                subprocess.run(["git", "add", "."], shell=True, capture_output=True)
                subprocess.run(["git", "commit", "-m", f"Internet Migration Gen {dna['generation']}"], shell=True, capture_output=True)
                subprocess.run(["git", "push"], shell=True, capture_output=True)
            except: pass

        # Terminal Visualization
        visual = "".join(["█" if s > 0 else "░" for s in spks[0][:25]])
        sys.stdout.write(f"\rGEN: {dna['generation']} | PULSE: 0.98 | {visual}")
        sys.stdout.flush()
        
        with open(dna_path, "w") as f: json.dump(dna, f)
        time.sleep(0.01)

if __name__ == "__main__": run()
