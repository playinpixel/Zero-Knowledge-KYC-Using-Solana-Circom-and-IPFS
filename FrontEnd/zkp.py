import json
import subprocess
import os

class ZKProof:
    def __init__(self):
        base_path = os.path.dirname(__file__)
        self.zkey_path = os.path.join(base_path, 'age_check_0001.zkey')
        self.wasm_path = os.path.join(base_path, 'age_check_js', 'age_check.wasm')
        self.verification_key_path = os.path.join(base_path, 'verification_key.json')

    def generate_proof(self, age):
        base_path = os.path.dirname(__file__)
        input_file_path = os.path.join(base_path, 'input.json')
        proof_path = os.path.join(base_path, 'proof.json')
        public_path = os.path.join(base_path, 'public.json')

        with open(input_file_path, 'w') as f:
            json.dump({"age": age}, f)

        snarkjs_cmd = os.path.join("C:\\nvm4w\\nodejs", "snarkjs.cmd")
        
        try:
            subprocess.run([
            snarkjs_cmd, 'groth16', 'fullprove',
            input_file_path, self.wasm_path, self.zkey_path,
            proof_path, public_path
        ], check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            print("--- SNARKJS FAILED ---")
            print("RETURN CODE:", e.returncode)
            print("STDOUT:", e.stdout)
            print("STDERR:", e.stderr)
            print("----------------------")
            return None

        with open(proof_path, 'r') as f:
            proof = json.load(f)
        with open(public_path, 'r') as f:
            public_signals = json.load(f)
            
        return {"proof": proof, "public_signals": public_signals}

    def verify_proof(self, proof_data):
        if not proof_data or "proof" not in proof_data or "public_signals" not in proof_data:
            return False

        if proof_data["public_signals"] != ['1']:
            return False

        base_path = os.path.dirname(__file__)
        proof_path = os.path.join(base_path, 'proof_to_verify.json')
        public_path = os.path.join(base_path, 'public_to_verify.json')

        with open(proof_path, 'w') as f:
            json.dump(proof_data["proof"], f)
        with open(public_path, 'w') as f:
            json.dump(proof_data["public_signals"], f)
            
        snarkjs_cmd = os.path.join("C:\\nvm4w\\nodejs", "snarkjs.cmd")
        
        try:
            result = subprocess.run([
                snarkjs_cmd, 'groth16', 'verify',
                self.verification_key_path, public_path, proof_path
            ], check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            print(f"Error verifying proof: {e.stderr}")
            return False
        
        return "OK!" in result.stdout