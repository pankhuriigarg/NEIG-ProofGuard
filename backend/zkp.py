import subprocess
import json
import os

ZKP_DIR = os.path.join(os.path.dirname(__file__), '..', 'zkp')

def generate_proof(hash_value):
    # Input file banao
    input_data = {
        "hash": str(int(hash_value[:8], 16)),
        "expectedHash": str(int(hash_value[:8], 16))
    }
    
    input_path = os.path.join(ZKP_DIR, 'input.json')
    with open(input_path, 'w') as f:
        json.dump(input_data, f)
    
    # Witness generate karo
    witness_cmd = [
        'node',
        os.path.join(ZKP_DIR, 'hash_check_js', 'generate_witness.js'),
        os.path.join(ZKP_DIR, 'hash_check_js', 'hash_check.wasm'),
        input_path,
        os.path.join(ZKP_DIR, 'witness.wtns')
    ]
    subprocess.run(witness_cmd, check=True, cwd=ZKP_DIR)
    
    # Proof generate karo
    proof_cmd = [
        'snarkjs.cmd', 'groth16', 'prove',
        os.path.join(ZKP_DIR, 'circuit_final.zkey'),
        os.path.join(ZKP_DIR, 'witness.wtns'),
        os.path.join(ZKP_DIR, 'proof.json'),
        os.path.join(ZKP_DIR, 'public.json')
    ]
    subprocess.run(proof_cmd, check=True, cwd=ZKP_DIR)
    
    # Proof read karo
    with open(os.path.join(ZKP_DIR, 'proof.json'), 'r') as f:
        proof = json.load(f)
    
    return proof

def verify_proof():
    verify_cmd = [
        'snarkjs.cmd', 'groth16', 'verify',
        os.path.join(ZKP_DIR, 'verification_key.json'),
        os.path.join(ZKP_DIR, 'public.json'),
        os.path.join(ZKP_DIR, 'proof.json')
    ]
    
    result = subprocess.run(
        verify_cmd, 
        capture_output=True, 
        text=True, 
        cwd=ZKP_DIR
    )
    
    return "OK" in result.stdout