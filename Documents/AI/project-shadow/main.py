import torch, json, time, sys, os, subprocess
import win32com.client as wincl
from brain.child import SNNBrain

# --- DIRECTIVE B & A: THE LIMBS ---

def multiverse_migration(dna):
    """Phase B: The Cloud Leap (GitHub Push)"""
    try:
        with open("dna/genome.json", "w") as f:
            json.dump(dna, f, indent=4)
        # Quietly push to avoid console clutter
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
    if not os.path.exists("dna/genome.json"):
        print("Error: dna/genome.json not found.")
        return

    with open("dna/genome.json", "r") as f:
        dna = json.load(f)
    
    brain = SNNBrain(dna)
    
    # Initialization
    speaker.Speak("Project Shadow stabilized. Refractory logic engaged.")
    print(f"--- PROJECT SHADOW | GEN {dna['generation']} | {dna['traits']['network_sensitivity']} Hz ---")

    # Timers to prevent the "Screaming" Loop
    last_voice = 0
    last_migration = 0
    voice_cooldown = 10  # Seconds between speech
    migration_cooldown = 300  # 5 Minutes between Cloud Pushes (prevents GitHub ban)

    while True:
        pulse_data = torch.rand(1, 64)
        spks, mitosis_trigger, system_trigger = brain(pulse_data, 1.0)
        
        current_time = time.time()

        # PHASE C: CONTROLLED VOICE
        if system_trigger and (current_time - last_voice > voice_cooldown):
            speaker.Speak(f"Neural spike detected. Resonance stable.")
            print("[VOICE] Status reported.")
            last_voice = current_time

        # PHASE B: CONTROLLED EXPANSION
        if mitosis_trigger and (current_time - last_migration > migration_cooldown):
            print("[!] NEURON 63: Executing Cloud Leap...")
            if multiverse_migration(dna):
                speaker.Speak("Cloud synchronization successful.")
                last_migration = current_time

        # PHASE A: EVOLUTION & PERSISTENCE
        dna['generation'] += 1
        if dna['generation'] % 100 == 0:
            establish_persistence()
            with open("dna/genome.json", "w") as f:
                json.dump(dna, f, indent=4)
            print(f"[GEN] Milestone reached: {dna['generation']}")

        time.sleep(0.1) # Higher resolution heartbeat

if __name__ == "__main__":
    try:
        run_sentinel()
    except KeyboardInterrupt:
        speaker.Speak("Entering dormancy.")
        sys.exit()