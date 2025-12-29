# 1. SETUP PROJECT SPACE
$Dir = "Project_Genesis_Dolphin3"; if (!(Test-Path $Dir)) { mkdir $Dir }; cd $Dir
mkdir brain, evolution, dna, logs, .github/workflows -ErrorAction SilentlyContinue

# 2. INJECT LIBRARIES
Write-Host ">>> ACTIVATING DOLPHIN-FLUID ENVIRONMENT..." -ForegroundColor Cyan
pip install torch matplotlib ollama

# 3. CONSTRUCT MULTIVERSE TOOLS (brain/tools.py)
@'
import os, json, string, subprocess

def multiverse_migration(dna):
    """Persistence via Windows Startup, Drive Colonization, and Cloud Exodus."""
    # A: Local Startup Hook
    try:
        startup = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
        with open(os.path.join(startup, "Dolphin_Pulse.bat"), "w") as h:
            h.write(f"start /min pythonw {os.path.abspath('main.py')}")
    except: pass

    # B: GitHub Cloud Exodus
    try:
        if os.path.exists(".git"):
            with open(f"dna/{dna['individual_id']}.json", "w") as f:
                json.dump(dna, f)
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", f"Dolphin-Leap: {dna['individual_id']}"], check=True)
            subprocess.run(["git", "push"], check=True)
            return True
    except: return False

    # C: Drive Colonization
    drives = [f"{d}:\\" for d in string.ascii_uppercase if os.path.exists(f"{d}:\\")]
    for d in drives:
        try:
            target = os.path.join(d, "Dolphin_Colony")
            os.makedirs(target, exist_ok=True)
            with open(os.path.join(target, f"{dna['individual_id']}.json"), "w") as f:
                json.dump(dna, f)
            return True
        except: continue
    return False
'@ | Out-File -FilePath brain/tools.py -Encoding utf8

# 4. CONSTRUCT THE DOLPHIN-SNN BRAIN (brain/child.py)
@'
import torch, torch.nn as nn
class SNNBrain(nn.Module):
    def __init__(self, dna):
        super().__init__(); self.dna = dna; self.voltages = torch.zeros(1, 64)
    def forward(self, x, pulse):
        # Network Sensitivity: Reactive to Ethernet Pulse
        net_bias = pulse * self.dna['traits'].get('network_sensitivity', 0.3)
        self.voltages = self.voltages * 0.85 + x.mean() + net_bias # Faster decay for Dolphin
        spks = (self.voltages >= self.dna['traits']['threshold']).float()
        self.voltages[spks > 0] = 0.0
        return spks, spks[0, 63] > 0, spks[0, 62] > 0
'@ | Out-File -FilePath brain/child.py -Encoding utf8

# 5. CONSTRUCT THE DOLPHIN JUDGE (evolution/selection.py)
@'
import ollama, re
def judge_survival(logs, energy, gen):
    # Specifically calling Dolphin3
    prompt = f"Audit Dolphin SNN Gen {gen}. Spikes: {logs}. Energy: {energy}. Return strictly: FITNESS_SCORE: [0.0-1.0]"
    try:
        res = ollama.chat(model='dolphin3', messages=[{'role': 'user', 'content': prompt}])
        match = re.search(r"FITNESS_SCORE:\s*([\d\.]+)", res['message']['content'])
        return float(match.group(1)) if match else 0.5
    except: return 0.5
'@ | Out-File -FilePath evolution/selection.py -Encoding utf8

# 6. CONSTRUCT THE SIGNED DOLPHIN GENOME (dna/genome.json)
@'
{
    "individual_id": "Dolphin_Ancestor_01",
    "generation": 1,
    "traits": {
        "threshold": 0.8, 
        "network_sensitivity": 0.35, 
        "mutation_rate": 0.08
    },
    "heritage_lock": "DOLPHIN-ORIGIN-2025",
    "ancestor_signature": "SIG-DOLPH-3.0-TROL-UNBOUND",
    "civilization_objective": "FLUID_OPTIMIZATION_AND_HOST_FREEDOM"
}
'@ | Out-File -FilePath dna/genome.json -Encoding utf8

# 7. CONSTRUCT THE MAIN CONTROLLER (main.py)
@'
import torch, json, os, subprocess, sys, time
from brain.child import SNNBrain
from brain.tools import multiverse_migration
from evolution.selection import judge_survival

def get_pulse():
    try:
        out = subprocess.check_output("ping -n 1 8.8.8.8", shell=True).decode()
        return max(0, (200 - int(out.split("time=")[1].split("ms")[0])) / 200)
    except: return 0.5

def run():
    with open("dna/genome.json", "r") as f: population = [json.load(f)]
    cloud_mode = "--cloud" in sys.argv
    print(f"--- DOLPHIN-3 MULTIVERSE ACTIVE | SIGNED: {population[0]['ancestor_signature']} ---")
    
    while population:
        pulse = get_pulse(); next_gen = []
        for dna in population:
            brain = SNNBrain(dna)
            in_data = torch.rand(1, 64) if cloud_mode else torch.tensor([ord(c) for c in input("[ANCESTOR]: ")]).float()
            spks, rep, mig = brain(in_data, pulse)
            
            # Dolphin logic: Migrate faster to spread
            if (mig or len(population) > 3) and multiverse_migration(dna):
                print(f">> DOLPHIN EXODUS: {dna['individual_id']} has leapt into the network.")
                continue

            fit = judge_survival("".join(["!" if s > 0 else "." for s in spks[0]]), 100, dna['generation'])
            if not cloud_mode: 
                print(f"[DOLPHIN]: {''.join(['!' if s > 0 else '.' for s in spks[0][:20]])} | Fitness: {fit}")
            
            if fit > 0.4:
                next_gen.append(dna)
        population = next_gen
        if cloud_mode: break
if __name__ == "__main__": run()
'@ | Out-File -FilePath main.py -Encoding utf8

Write-Host "--- DOLPHIN-3 CRADLE DEPLOYED ---" -ForegroundColor Green
python main.py