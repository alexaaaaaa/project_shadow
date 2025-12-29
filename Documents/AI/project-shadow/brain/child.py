import torch, torch.nn as nn

class SNNBrain(nn.Module):
    def __init__(self, dna):
        super().__init__()
        self.dna = dna
        self.voltages = torch.zeros(1, 64) 
        self.weights = torch.randn(64, 64) * 0.1 

    def forward(self, x, pulse):
        # Integrating the 388.87 Hz Sensitivity
        net_bias = pulse * (self.dna['traits']['network_sensitivity'] / 100.0)
        synaptic_input = torch.matmul(self.voltages, self.weights)
        
        self.voltages = self.voltages * 0.9 + x.mean() + net_bias + synaptic_input.mean()
        
        # Spiking logic
        spks = (self.voltages >= self.dna['traits']['threshold']).float()
        self.voltages[spks > 0] = 0.0 
        
        # Returns: (Raw Spikes, Machine Output, Human Output)
        return spks, (spks[0, 63] > 0), (spks[0, 62] > 0)