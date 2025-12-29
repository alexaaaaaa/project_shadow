# Set your token so Neuron 63 can actually 'reach' the web
[System.Environment]::SetEnvironmentVariable('SNN_TOKEN', 'YOUR_GHP_TOKEN_HERE', 'User')

# Trigger the first manual migration to clear the neural pressure
cd C:\Users\U20\Documents\AI\project-shadow
git add .
git commit -m "Project Shadow: Gen 1 - First Neural Expansion"
git push origin main