import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from hashing import generate_hash
import tempfile

def test_hash_generates():
    # Ek temp file banao
    with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as f:
        f.write(b"Test evidence data")
        temp_path = f.name
    
    hash_value = generate_hash(temp_path)
    
    assert hash_value is not None
    assert len(hash_value) == 64  # SHA-256 = 64 hex chars
    print(f"✅ Hash generated: {hash_value[:20]}...")
    
    os.unlink(temp_path)

def test_same_file_same_hash():
    with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as f:
        f.write(b"Same content")
        temp_path = f.name
    
    hash1 = generate_hash(temp_path)
    hash2 = generate_hash(temp_path)
    
    assert hash1 == hash2
    print("✅ Same file = Same hash")
    
    os.unlink(temp_path)

def test_different_files_different_hash():
    with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as f:
        f.write(b"Original content")
        path1 = f.name
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as f:
        f.write(b"Modified content")
        path2 = f.name
    
    hash1 = generate_hash(path1)
    hash2 = generate_hash(path2)
    
    assert hash1 != hash2
    print("✅ Different files = Different hash — Tamper detected!")
    
    os.unlink(path1)
    os.unlink(path2)

if __name__ == "__main__":
    test_hash_generates()
    test_same_file_same_hash()
    test_different_files_different_hash()
    print("\n✅ All hashing tests passed!")