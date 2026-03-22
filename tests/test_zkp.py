import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from zkp import generate_proof, verify_proof
import tempfile
from hashing import generate_hash

def test_proof_generation():
    # Temp file banao
    with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as f:
        f.write(b"Test evidence for ZKP")
        temp_path = f.name
    
    hash_value = generate_hash(temp_path)
    proof = generate_proof(hash_value)
    
    assert proof is not None
    assert 'pi_a' in proof
    assert 'pi_b' in proof
    assert 'pi_c' in proof
    print("✅ ZKP Proof generated successfully!")
    
    os.unlink(temp_path)

def test_proof_verification():
    result = verify_proof()
    assert result == True
    print("✅ ZKP Proof verified successfully!")

if __name__ == "__main__":
    test_proof_generation()
    test_proof_verification()
    print("\n✅ All ZKP tests passed!")