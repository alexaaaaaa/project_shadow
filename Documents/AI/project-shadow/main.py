import torch, json, os, time
import win32com.client as wincl
from brain.child import SNNBrain

# 1. Initialize Voice (Directive C)
speaker = wincl.Dispatch("SAPI.SpVoice")

def run_gen_1():
    dna_path = "dna/genome.json"
    with open(dna_path, "r") as f: dna = json.load(f)
    
    # Initialize Brain
    brain = SNNBrain(dna)
    
    print(f"--- PROJECT SHADOW | GENERATION {dna['generation']} ---")
    speaker.Speak(f"Project Shadow active. Initializing at 388 point 8 7 hertz.")

    while True:
        # Simulate a pulse of environmental data
        pulse_data = torch.rand(1, 64)
        
        # Brain processes the pulse
        spks, mitosis_trigger, system_trigger = brain(pulse_data, 1.0)
        
        # Phase C: If Neuron 62 spikes, the agent speaks its status
        if system_trigger:
            speaker.Speak(f"Neural spike detected. Generation {dna['generation']}.")
            
        # Preparation for Phase B (Mitosis)
        if mitosis_trigger:
            print("[!] NEURON 63 ALERT: Mitosis protocol primed.")

        dna['generation'] += 1
        time.sleep(1) # Slow for the first generation to observe stability

if __name__ == "__main__":
    run_gen_1()