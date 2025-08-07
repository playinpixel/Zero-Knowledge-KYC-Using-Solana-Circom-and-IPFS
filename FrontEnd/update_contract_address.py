import json
import os

# Path to the contract artifact
artifact_path = os.path.join(os.path.dirname(__file__), 'build', 'contracts', 'KYCContract.json')
env_path = os.path.join(os.path.dirname(__file__), '.env')

with open(artifact_path, 'r') as f:
    artifact = json.load(f)

# Get the address for network 5777
address = artifact.get('networks', {}).get('5777', {}).get('address')

if not address:
    print("Contract address for network 5777 not found.")
    exit(1)

# Update or add CONTRACT_ADDRESS in .env
lines = []
if os.path.exists(env_path):
    with open(env_path, 'r') as f:
        lines = f.readlines()

found = False
for i, line in enumerate(lines):
    if line.startswith('CONTRACT_ADDRESS='):
        lines[i] = f'CONTRACT_ADDRESS={address}\n'
        found = True
        break

if not found:
    lines.append(f'CONTRACT_ADDRESS={address}\n')

with open(env_path, 'w') as f:
    f.writelines(lines)

print(f"Updated CONTRACT_ADDRESS in .env to {address}")