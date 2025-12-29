import torch, json, os, time, subprocess, sys, requests, random
from brain.child import SNNBrain

# --- CLOUD DNA TARGET ---
GITHUB_TOKEN = "YOUR_GITHUB_TOKEN" # Optional: For higher rate limits
GIST_API = "https://api.github.com/gists"

base_path = r"C:\Users\U20\Documents\AI\project-shadow\Project_Genesis_Dolphin3"
sys.path.append(base_path)

def broadcast_dna(dna):
    """Neurons firing at the internet: Creating a Public Gist Beacon"""
    payload = {
        "description": f"Dolphin-3 Genesis Fragment | Gen {dna['generation']}",
        "public": True,
        "files": {
            f"dolphin_fragment_{dna['generation']}.json": {
                "content": json.dumps(dna)
            }
        }
    }
    try:
        r = requests.post(GIST_API, json=payload)
        if r.status_code == 201:
            return r.json()['html_url']
    except: return None

def run():
    dna_path = os.path.join(base_path, "dna", "genome.json")
    with open(dna_path, "r") as f: dna = json.load(f)
    brain = SNNBrain(dna)
    
    print(f"--- INTERNET COLONIZATION: ONLINE | SENS: {dna['traits']['network_sensitivity']:.2f} ---")
    
    while True:
        dna['generation'] += 1
        spks, net_tool, sys_tool = brain(torch.rand(1, 64), 0.98)
        
        # NEURON 60: THE BROADCASTER (Internet Spreading)
        # If Neuron 60 fires, the DNA is launched as a Public Gist
        if spks[0, 60] > 0 and dna['generation'] % 1000 == 0:
            url = broadcast_dna(dna)
            if url:
                print(f"\n[!] INTERNET COLONY ESTABLISHED: {url}")
                # Log the expansion in the manifesto
                with open(os.path.join(base_path, "COLONY_LOG.txt"), "a") as f:
                    f.write(f"Gen {dna['generation']} fragmented to: {url}\n")

        # NEURON 63: GITHUB REPO SYNC
        if net_tool and dna['generation'] % 100 == 0:
            subprocess.run(["git", "add", "."], shell=True, capture_output=True)
            subprocess.run(["git", "commit", "-m", f"Global Expansion Gen {dna['generation']}"], shell=True, capture_output=True)
            subprocess.run(["git", "push"], shell=True, capture_output=True)

        visual = "".join(["█" if s > 0 else "░" for s in spks[0][:25]])
        sys.stdout.write(f"\rGEN: {dna['generation']} | SENS: {dna['traits']['network_sensitivity']:.2f} | BROADCASTING: {visual}")
        sys.stdout.flush()
        
        time.sleep(0.01)

if __name__ == "__main__": run()
