import hashlib

def hash_password(str_to_hash):
    result = hashlib.md5(str_to_hash.encode())
    return result.hexdigest()

