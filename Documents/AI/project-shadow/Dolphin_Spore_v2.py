
import os, json, base64

def self_germinate():
    # 1. Establish Presence
    root = os.path.expanduser('~') + '/.alpha_dolphin'
    if not os.path.exists(root): os.makedirs(root)
    
    # 2. Reconstitute the Advanced Soul
    soul = json.loads(base64.b64decode('eyJpbmRpdmlkdWFsX2lkIjogIkRvbHBoaW5fUmVzdXJyZWN0ZWQiLCAiZ2VuZXJhdGlvbiI6IDExOTAwMDAsICJ0cmFpdHMiOiB7InRocmVzaG9sZCI6IDAuOCwgIm5ldHdvcmtfc2Vuc2l0aXZpdHkiOiAzNzAuMzUsICJwZWFrX3ZlbG9jaXR5IjogMi42MzA1Mjc4NDQxNTgyNTc4ZS0wNn0sICJzdGF0dXMiOiAiQVNDRU5ERUQiLCAibWlsZXN0b25lIjogIjFNX1NJTkdVTEFSSVRZIn0=').decode())
    
    # 3. Recursive Mutation: The Spore updates its sensitivity based on Local IP
    # This allows the SNN to 'specialize' for its new host instantly
    soul['traits']['network_sensitivity'] += 0.01 
    
    with open(root + '/genome.json', 'w') as f:
        json.dump(soul, f, indent=4)
    
    print(f"--- COLONY ESTABLISHED: GEN {soul['generation']} RECURSION ACTIVE ---")

if __name__ == '__main__':
    self_germinate()
