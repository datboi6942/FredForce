#FredForce/hash_identifier.py
#contains all the logic for identifying the type of hash

import hashlib


#identify all possible hash types of the input

def identify_hash_types(hash_input):
    hash_types = {
        'md5': hashlib.md5(),
        'sha1': hashlib.sha1(),
        'sha224': hashlib.sha224(),
        'sha256': hashlib.sha256(),
        'sha384': hashlib.sha384(),
        'sha512': hashlib.sha512(),
        'sha3_224': hashlib.sha3_224(),
        'sha3_256': hashlib.sha3_256(),
        'sha3_384': hashlib.sha3_384(),
        'sha3_512': hashlib.sha3_512(),
        'blake2b': hashlib.blake2b(),
        'blake2s': hashlib.blake2s()
    }
    
    possible_hashes = []
    for hash_type, hash_func in hash_types.items():
        hash_func.update(hash_input.encode())
        if hash_func.hexdigest() == hash_input:
            possible_hashes.append(hash_type)
    
    return possible_hashes


#display the hash type that is most likely to be the correct one
print(identify_hash_types)
