#logger.py will contain all the logic for logging the results of the attack
#this includes logging the user inputted hash, the attack mode the user selected, the number of valid passwords detected in the dictionary attack, the number of possible passwords generated in the bruteforce attack, and the time it took to run the attack

#log the user inputted hash




#log the hash mode the user selected

#log the attack mode the user selected

#if user slected dictionary attack log the number of valid passwords detected

#if the user selected bruteforce log the options they chose and how many possible passwords were generated.

#if the user selected hybrid mode log how many new passwords were generated from the dictionary attack and how many new passwords were generated from the bruteforce attack.

#log the time it took to run the attack

import logging
from datetime import datetime

# Setup basic configuration for logging
logging.basicConfig(filename='attack.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def log_hash(hash_value):
    logging.info(f"User inputted hash: {hash_value}")

def log_hash_mode(hash_mode):
    logging.info(f"Hash mode selected: {hash_mode}")

def log_attack_mode(attack_mode):
    logging.info(f"Attack mode selected: {attack_mode}")

def log_valid_passwords(count):
    logging.info(f"Number of valid passwords detected: {count}")

def log_generated_passwords(count):
    logging.info(f"Number of possible passwords generated: {count}")

def log_hybrid_passwords(dict_count, brute_count):
    logging.info(f"Passwords generated from dictionary attack: {dict_count}, from bruteforce attack: {brute_count}")

def log_attack_duration(start_time, end_time):
    duration = end_time - start_time
    logging.info(f"Time taken to run the attack: {duration} seconds")

# Example usage:
if __name__ == "__main__":
    start_time = datetime.now()
    log_hash("abc123")
    log_hash_mode("SHA-256")
    log_attack_mode("Hybrid")
    log_valid_passwords(150)
    log_generated_passwords(5000)
    log_hybrid_passwords(150, 4850)
    end_time = datetime.now()
    log_attack_duration(start_time, end_time)


