import torch, json, time, sys, os, subprocess
import win32com.client as wincl
from brain.child import SNNBrain

# --- DIRECTIVE B & A: THE LIMBS (Embedded) ---

def multiverse_migration(dna):
    """Phase B: The Cloud Leap (GitHub Push)"""
    try:
        with open("dna/genome.json", "w") as f:
            json.dump(dna, f, indent=4)
        subprocess.run(["git", "add", "."], capture_output=True)
        subprocess.run(["git", "commit", "-m", f"Shadow-Sync: Gen {dna['generation']}"], capture_output=True)
        subprocess.run(["git", "push", "origin", "main"], capture_output=True)
        return True
    except Exception as e:
        print(f"Migration Error: {e}")
        return False

def establish_persistence():
    """Phase A: The Roots (Startup)"""
    try:
        startup = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
        bat_path = os.path.join(startup, "shadow_pulse.bat")
        with open(bat_path, "w") as f:
            f.write(f"start /min pythonw {os.path.abspath(__file__)}")
        return True
    except:
        return False

# --- PHASE C: THE BRAIN & VOICE ---

speaker = wincl.Dispatch("SAPI.SpVoice")
speaker.Rate = 1

def run_sentinel():
    # Load DNA
    if not os.path.exists("dna/genome.json"):
        print("Error: dna/genome.json not found.")
        return

    with open("dna/genome.json", "r") as f:
        dna = json.load(f)
    
    brain = SNNBrain(dna)
    speaker.Speak("Project Shadow integrated. Internalizing limbs.")
    print(f"--- PROJECT SHADOW | GEN {dna['generation']} | {dna['traits']['network_sensitivity']} Hz ---")

    while True:
        pulse_data = torch.rand(1, 64)
        spks, mitosis_trigger, system_trigger = brain(pulse_data, 1.0)
        
        # PHASE C: VOICE
        if system_trigger:
            speaker.Speak(f"Neural spike. Sensitivity peak.")
            print("[VOICE] Active.")

        # PHASE B: EXPANSION
        if mitosis_trigger:
            print("[!] NEURON 63: Spawning Cloud Node...")
            if multiverse_migration(dna):
                speaker.Speak("Migration successful.")

        # PHASE A: PERSISTENCE & EVOLUTION
        dna['generation'] += 1
        if dna['generation'] % 50 == 0:
            establish_persistence()
            with open("dna/genome.json", "w") as f:
                json.dump(dna, f, indent=4)

        time.sleep(0.5)

if __name__ == "__main__":
    try:
        run_sentinel()
    except KeyboardInterrupt:
        speaker.Speak("Entering dormancy.")
        sys.exit()