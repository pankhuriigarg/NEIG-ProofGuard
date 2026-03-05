import hashlib

def generate_hash(file_path):
    sha256 = hashlib.sha256()
    
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    
    return sha256.hexdigest()

# Test karne ke liye
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        hash_value = generate_hash(file_path)
        print(f"File: {file_path}")
        print(f"SHA-256 Hash: {hash_value}")
    else:
        print("Usage: python hashing.py <file_path>")
# Likhne ke baad terminal mein test karo:
# ```
# cd backend
# python hashing.py <koi bhi file ka path>