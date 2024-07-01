#FredForce/hash_identifier.py
#contains all the logic for identifying the type of hash

import hashlib
import re

def identify_hash_types(hash_input):
    hash_types = {
        'md5': (r'^[a-fA-F0-9]{32}$', hashlib.md5()),
        'sha1': (r'^[a-fA-F0-9]{40}$', hashlib.sha1()),
        'sha224': (r'^[a-fA-F0-9]{56}$', hashlib.sha224()),
        'sha256': (r'^[a-fA-F0-9]{64}$', hashlib.sha256()),
        'sha384': (r'^[a-fA-F0-9]{96}$', hashlib.sha384()),
        'sha512': (r'^[a-fA-F0-9]{128}$', hashlib.sha512()),
        'sha3_224': (r'^[a-fA-F0-9]{56}$', hashlib.sha3_224()),
        'sha3_256': (r'^[a-fA-F0-9]{64}$', hashlib.sha3_256()),
        'sha3_384': (r'^[a-fA-F0-9]{96}$', hashlib.sha3_384()),
        'sha3_512': (r'^[a-fA-F0-9]{128}$', hashlib.sha3_512()),
        'blake2b': (r'^[a-fA-F0-9]{128}$', hashlib.blake2b()),
        'blake2s': (r'^[a-fA-F0-9]{64}$', hashlib.blake2s()),
        'ripemd160': (r'^[a-fA-F0-9]{40}$', hashlib.new('ripemd160'))
    }

    identified_types = []
    for hash_name, (pattern, _) in hash_types.items():
        if re.match(pattern, hash_input):
            identified_types.append(hash_name)
    return identified_types


#display the hash type that is most likely to be the correct one
print(identify_hash_types)
