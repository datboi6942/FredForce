#contains the logic for the 3 different attack_methods which are:
#bruteforce
#dictionary attack
#hybrid attack
from itertools import product
import hashlib
import os
from dictionary_loader import load_dictionary
from session_manager import SessionManager


def dictionary_attack(hash_value, hash_type, dictionary_file):
    print("Starting dictionary attack...")
    try:
        dictionary = load_dictionary(dictionary_file)
        hash_func = getattr(hashlib, hash_type)  # Correctly get the hash function
        total_words = len(dictionary)

        for index, word in enumerate(dictionary, start=1):
            if index % 100 == 0:  # Update progress every 100 words
                print(f"\rTested {index} of {total_words} words", end='')
            if hash_func(word.strip().encode()).hexdigest() == hash_value:
                print(f"Match found: {word}")
                return word

    except FileNotFoundError:
        print("Dictionary file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return None

def bruteforce_attack(hash_value, hash_type, bruteforce_options, start_from=0, session=None):
    print(f"Debug: start_from type - {type(start_from)}, value - {start_from}")

    # Define character sets
    charsets = {
        'l': "abcdefghijklmnopqrstuvwxyz",  # Lowercase letters
        'L': "ABCDEFGHIJKLMNOPQRSTUVWXYZ",  # Uppercase letters
        'N': "0123456789",  # Numbers
        '@': "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"  # Symbols
    }
    
    # Parse bruteforce_options to extract pattern
    pattern = bruteforce_options.split(':') if bruteforce_options else []
    charset = ''.join(charsets[char] for char in pattern if char in charsets)
    if not charset:
        print("Invalid pattern. Use 'l' for lowercase letters, 'L' for uppercase letters, 'N' for numbers, '@' for symbols.")
        return None

    # Create a hash function based on the hash_type
    if hash_type in hashlib.algorithms_available:
        hash_func = getattr(hashlib, hash_type)
    else:
        print(f"Unsupported hash type: {hash_type}")
        return None

    # Generate and test combinations
    total_combinations = len(list(product(charset, repeat=len(pattern))))
    tested_combinations = start_from
    try:
        for combo in product(charset, repeat=len(pattern)):
            candidate = ''.join(combo)
            tested_combinations += 1
            if tested_combinations % 1000 == 0:  # Update progress every 1000 attempts
                session.update_progress(tested_combinations)
                print(f"\rTested {tested_combinations} of {total_combinations} combinations", end='')
            if hash_func(candidate.encode()).hexdigest() == hash_value:
                print(f"Match found: {candidate}")
                return candidate

        print("No match found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return None

def hybrid_attack(hash_value, hash_type, dictionary_file, bruteforce_options, position):
    print("Starting hybrid attack...")
    
    # First, try the dictionary attack
    result = dictionary_attack(hash_value, hash_type, dictionary_file)
    if result:
        print(f"Password found using dictionary attack: {result}")
        return result

    # If not found, proceed with brute force
    modified_wordlist = generate_modified_words_from_dictionary(dictionary_file, bruteforce_options, position)
    for index, word in enumerate(modified_wordlist):
        if index % 1000 == 0:  # Update progress every 1000 words
            print(f"Tested {index} words, current word: '{word}'...")
        if getattr(hashlib, hash_type)(word.encode()).hexdigest() == hash_value:
            print(f"Password found using brute force: {word}")
            return word

    print("No valid password found.")
    return None

def generate_modified_words_from_dictionary(dictionary_file, bruteforce_options, position):
    with open(dictionary_file, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            word = line.strip()
            charsets = {
                'l': "abcdefghijklmnopqrstuvwxyz",
                'L': "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                'N': "0123456789",
                '@': "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
            }
            pattern = ''.join(charsets[char] for char in bruteforce_options if char in charsets)
            if position == 'start':
                for pat in pattern:
                    yield f"{pat}{word}"
            elif position == 'end':
                for pat in pattern:
                    yield f"{word}{pat}"
            else:
                pos = int(position)
                for pat in pattern:
                    yield word[:pos] + pat + word[pos:]

def generate_modified_words(base_word, position, bruteforce_options):
    if position == 'start':
        return [f"{pattern}{base_word}" for pattern in bruteforce_options]
    elif position == 'end':
        return [f"{base_word}{pattern}" for pattern in bruteforce_options]
    else:
        # Insert at specific position or handle other cases
        try:
            pos = int(position)
            return [base_word[:pos] + pattern + base_word[pos:] for pattern in bruteforce_options]
        except ValueError:
            raise ValueError("Position must be 'start', 'end', or a valid integer index.")
