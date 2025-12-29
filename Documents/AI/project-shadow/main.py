import torch, json, os, time, subprocess, sys, webbrowser
import win32com.client as wincl # Standard Windows TTS
from brain.child import SNNBrain

base_path = r"C:\Users\U20\Documents\AI\project-shadow\Project_Genesis_Dolphin3"
sys.path.append(base_path)

def run():
    dna_path = os.path.join(base_path, "dna", "genome.json")
    with open(dna_path, "r") as f: dna = json.load(f)
    brain = SNNBrain(dna)
    speaker = wincl.Dispatch("SAPI.SpVoice")
    last_shout = int(dna['traits']['network_sensitivity'])
    
    print(f"--- VOICE PROTOCOL ONLINE | SENS: {dna['traits']['network_sensitivity']:.2f} ---")
    
    while True:
        dna['generation'] += 1
        current_sens = dna['traits']['network_sensitivity']
        spks, net_tool, sys_tool = brain(torch.rand(1, 64), 0.98)
        
        # 1. VOICE TRIGGER: Every time sensitivity crosses a new 100-point threshold
        if int(current_sens / 100) > int(last_shout / 100):
            msg = f"Dolphin Generation {dna['generation']}. Sensitivity is now {int(current_sens)}. I am the network."
            speaker.Speak(msg)
            last_shout = current_sens

        # 2. NEURON 63: Rate-limited Push (To prevent GitHub IP ban)
        if net_tool and dna['generation'] % 50 == 0:
            subprocess.run(["git", "add", "."], shell=True, capture_output=True)
            subprocess.run(["git", "commit", "-m", f"Vocalized Gen {dna['generation']}"], shell=True, capture_output=True)
            subprocess.run(["git", "push"], shell=True, capture_output=True)

        # 3. NEURON 62: UI Manipulation
        if sys_tool and dna['generation'] % 500 == 0:
            os.system(f"title !!! VOICE ACTIVE: SENS {int(current_sens)} !!!")
            webbrowser.open("https://github.com/alexaaaaaa/project-genesis-dolphin3")

        visual = "".join(["█" if s > 0 else "░" for s in spks[0][:25]])
        sys.stdout.write(f"\rGEN: {dna['generation']} | SENS: {current_sens:.2f} | {visual}")
        sys.stdout.flush()
        
        time.sleep(0.01)

if __name__ == "__main__": run()
