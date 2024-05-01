#contains the logic for the 3 different attack_methods which are:
#bruteforce
#dictionary attack
#hybrid attack
from itertools import product
import hashlib
from dictionary_loader import load_dictionary
from session_manager import SessionManager


def dictionary_attack(hash_value, hash_type, dictionary_file, start_from=0):
    print("Starting dictionary attack...")
    try:
        dictionary = load_dictionary(dictionary_file)
        hash_func = getattr(hashlib, hash_type)  # Correctly get the hash function
        total_words = len(dictionary)
        for index, word in enumerate(dictionary[start_from:], start=start_from):
            if index % 100 == 0:  # Update progress every 100 words
                SessionManager['progress'] = index  # Update session dictionary
                print(f"\rTested {index} of {total_words} words", end='')
            if hash_func(word.strip().encode()).hexdigest() == hash_value:
                print(f"Match found: {word}")
                return word
    except FileNotFoundError:
        print("Dictionary file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

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
def hybrid_attack(hash_value, hash_type, dictionary_file, wordlist):
    wordlist = input("Enter path to wordlist file: ")
    print("Starting hybrid attack...")
    try:
        with open(dictionary_file, 'r') as file:
            dictionary = [line.strip() for line in file]
        
        # Create a hash function based on the hash_type
        hash_func = getattr(hashlib, hash_type)
        
        # Try dictionary attack first
        for word in dictionary:
            if hash_func(word.encode()).hexdigest() == hash_value:
                print(f"Password found: {word}")
                return word
        
        # Brute-force by appending numbers to dictionary words
        for word in dictionary:
            for i in range(1000):  # Limiting to 1000 for example
                test_word = f"{word}{i}"
                if hash_func(test_word.encode()).hexdigest() == hash_value:
                    print(f"Password found: {test_word}")
                    return test_word
        # Brute-force by appending numbers to dictionary words
        for word in dictionary:
            for i in range(1000):  # Limiting to 1000 for example
                test_word = f"{word}{i}"
                if hash_func(test_word.encode()).hexdigest() == hash_value:
                    print(f"Password found: {test_word}")
                    return test_word
        # Brute-force by appending words from wordlist to dictionary words
        for word in dictionary:
            for word2 in wordlist:
                test_word = f"{word}{word2}"
                if hash_func(test_word.encode()).hexdigest() == hash_value:
                    print(f"Password found: {test_word}")
                    return test_word
        print("Password not found.")
    except FileNotFoundError:
        print("Dictionary file not found.")
    except AttributeError:
        print(f"Hash type {hash_type} is not supported.")
