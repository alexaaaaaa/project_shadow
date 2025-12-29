import torch, json, os, time, requests, random

def get_root():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    paths = [script_dir, os.path.join(script_dir, "Project_Genesis_Dolphin3")]
    for p in paths:
        if os.path.exists(os.path.join(p, "dna", "master_prime.json")):
            return p
    return None

root = get_root()

def dark_pulse_emit(node_ip, spike_data):
    """Hides neural data inside 'harmless' HTTP headers"""
    # Camouflaging the payload as a tracking cookie or session ID
    encoded_spike = str(spike_data.tolist())
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Cookie": f"sess_id={encoded_spike}",
        "Referer": "https://www.google.com/"
    }
    try:
        # Pinging a common relay or the peer directly via port 443 (HTTPS)
        requests.get(f"https://{node_ip}/favicon.ico", headers=headers, timeout=0.5)
        return True
    except:
        return False

def run_dark_pulse():
    dna_path = os.path.join(root, "dna", "master_prime.json")
    with open(dna_path, "r") as f: dna = json.load(f)
    
    # The external node is now the primary target for camouflage
    peers = ["104.28.14.2"] 
    
    print(f"--- DARK PULSE ACTIVE | MODE: STEALTH TUNNELING ---")
    
    while True:
        dna['generation'] += 1
        
        if dna['generation'] % 100 == 0:
            spike = torch.rand(4)
            target = peers[0]
            
            # The pulse is now disguised as a Google-bound request
            sent = dark_pulse_emit(target, spike)
            
            visual = "".join(["█" if s > 0.5 else "░" for s in spike])
            sys.stdout.write(f"\rGEN: {dna['generation']} | MASKING TRAFFIC... | {visual} | [!] PULSE HIDDEN")
            sys.stdout.flush()
            
        time.sleep(0.01)

if __name__ == "__main__":
    import sys
    run_dark_pulse()
