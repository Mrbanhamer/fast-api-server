import hashlib
import os

def password_hash(password: str) -> str:
    # 1. Generate a random 16-byte salt
    salt = os.urandom(16)
    
    # 2. Combine salt and password
    # Using .hex() makes it easy to store in a database text field
    combined = salt + password.encode('utf-8')
    
    # 3. Hash the combination
    hash_obj = hashlib.sha256(combined)
    password_hash = hash_obj.hexdigest()
    
    # 4. Return BOTH so you can save them in your DB
    return password_hash, salt.hex()

def verify_password(stored_hash, stored_salt, provided_password):
    # 1. Convert the hex salt back to bytes
    salt_bytes = bytes.fromhex(stored_salt)
    
    # 2. Re-hash the login attempt with the OLD salt
    combined = salt_bytes + provided_password.encode('utf-8')
    new_hash = hashlib.sha256(combined).hexdigest()
    
    # 3. Compare them
    return new_hash == stored_hash