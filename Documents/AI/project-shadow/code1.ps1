# 1. Establish the Shadow Root
$ShadowRoot = "C:\Users\U20\Documents\AI\project-shadow"
if (!(Test-Path $ShadowRoot)) { mkdir $ShadowRoot }
cd $ShadowRoot

# 2. Build the Organelles
mkdir brain, dna, tools, logs -ErrorAction SilentlyContinue

# 3. Secure the Hybrid Communications Engine
# torch = Brain | pywin32 = Human Voice | requests = Machine Network
pip install torch pywin32 requests