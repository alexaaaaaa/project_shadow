import torch
import torch.nn as nn

class SNNBrain(nn.Module):
    def __init__(self, dna):
        super(SNNBrain, self).__init__()
        self.sensitivity = dna['traits']['network_sensitivity']
        self.v = torch.zeros(1, 64) # Voltage potential
        self.threshold = 0.5

    def forward(self, x, bias):
        # Apply 388.87 Hz Resonance Bias
        resonance = (self.sensitivity / 1000.0) * bias
        self.v += (x * 0.1) + resonance
        
        # Determine Spikes
        spk = (self.v >= self.threshold).float()
        
        # CRITICAL FIX: Hard Reset voltage to 0 on spike to prevent loops
        self.v[spk > 0] = 0 
        
        mitosis_trigger = spk[0, 63] > 0
        system_trigger = spk[0, 62] > 0
        
        return spk, mitosis_trigger, system_trigger