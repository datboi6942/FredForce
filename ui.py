#ui.py will contain all the logic for the user interface
#this includes welcoming the user, asking them for input, and displaying the results of the attack

#welcome the user with an Ascii banner



#ask the user to input a hash

#return the results of hash_identifier.py

#ask the user to confirm the type of hash or enter a manuel one

#display avaible modes and ask the user to select the attack mode

#prompt user to configure the attack

#return the progress of the the attack with a loading bar

#return the results of attack_

import sys
import json
from hash_identifier import identify_hash_types as identify_hash
from session_manager import *
from logger import log_hash, log_attack_mode
from attack_methods import hybrid_attack, bruteforce_attack, dictionary_attack   # Assuming this is the attack method used

def display_banner():
    banner = """
    #########################################
    # Welcome to FredForce Hash Cracker     #
    #########################################
    """
    print(banner)

def get_user_input(prompt):
    return input(prompt)

def main():
    display_banner()
    
    continue_attack = input("Do you want to continue the previous session? (y/n): ")
    if continue_attack.lower() not in ['y', 'n']:
        print("Invalid input. Please enter 'y' or 'n'.")
        return  # Exit or repeat the query
    if continue_attack.lower() == 'y':
        session = SessionManager()
        print(f"Debug: Session instantiated with session_data - {session.session_data}")
        # Directly proceed with the existing session data
        hash_value = session.session_data['hash_value']
        hash_type = session.session_data['hash_mode']
        attack_mode = session.session_data['attack_mode']
        bruteforce_options = session.session_data.get('bruteforce_options', 'L:L:L:N')  # Default pattern
        start_from = session.session_data.get('progress', 0)
        print(f"Resuming from: {start_from}")  # Debug statement to show where the attack is resuming from
        result = bruteforce_attack(hash_value, hash_type, bruteforce_options, start_from=start_from, session=session)
        print(f"Attack result: {result}")
        print("Session loaded. Resume with the following options:")
        print(json.dumps(session.session_data, indent=4))
    else:
        session = SessionManager(create_new=True)  # Adjusted to handle new session creation
        session.session_data = {}  # Explicitly clear session data
        print("Starting New Session")
        # Get hash from user
        print(f"Debug: session object before accessing session_data - {session}")
        hash_value = get_user_input("Enter the hash you want to crack: ")
        session.session_data['hash_value'] = hash_value  # Save the hash_value into session data
        session.save_session()  # Save the session after updating
        log_hash(hash_value)
        
        # Identify or confirm hash type
        print(identify_hash(hash_value))
        hash_type = get_user_input("Enter hash type: ")
        new_hash_type = get_user_input(f"Identified hash type as {hash_type}. Press Enter to confirm or type a different one: ")
        if new_hash_type:
            hash_type = new_hash_type
        session.session_data['hash_mode'] = hash_type  # Update session data immediately after first input
        
        # Select attack mode
        print("Available attack modes: [1] BruteForce [2] Dictionary [3] Hybrid")
        attack_mode = get_user_input("Select an attack mode (number): ")
        session.session_data['attack_mode'] = attack_mode  # Save the attack_mode into session data
        session.save_session()  # Save the session after updating
        log_attack_mode(attack_mode)
        
        # Configure attack based on mode
        if attack_mode == '1':
            print("Starting bruteforce attack...")
            print("Available character set options:")
            print("  'l' for lowercase letters (a-z)")
            print("  'L' for uppercase letters (A-Z)")
            print("  'N' for numbers (0-9)")
            print("  '@' for symbols (all printable ASCII symbols)")
            print("Enter pattern as a combination of 'l', 'L', 'N', and '@' separated by ':'.")
            print("Example pattern: 'L:N:@' for uppercase letters, numbers, and symbols.")
            bruteforce_options = get_user_input("Enter bruteforce options (e.g., 'L:N:@'): ")
            session.session_data['bruteforce_options'] = bruteforce_options  # Save the bruteforce_options into session data
            session.save_session()  # Save the session after updating
            try:
                print(f"Debug: session object before bruteforce attack - {session}")
                start_from = session.session_data.get('progress', 0)  # Ensure this is correctly extracted as an integer
                result = bruteforce_attack(hash_value, hash_type, bruteforce_options, start_from=start_from, session=session)
                print(f"Attack result: {result}")
            except Exception as e:
                print(f"An error occurred during the bruteforce attack: {e}")

        elif attack_mode == '2':
            dictionary_file = get_user_input("Enter path to dictionary file: ")
            session.update_session(hash_value=hash_value, hash_mode=hash_type, attack_mode='dictionary_attack', dictionary_file=dictionary_file)
            print("Starting dictionary attack...")
            try:
                result = dictionary_attack(hash_value, hash_type, dictionary_file)
                print(f"Attack result: {result}")
            except Exception as e:
                print(f"An error occurred during the dictionary attack: {e}")

        elif attack_mode == '3':
            dictionary_file = get_user_input("Enter path to dictionary file")
            bruteforce_options = get_user_input("Enter options for bruteforce ")

            session.update_session(hash_value=hash_value, hash_mode=hash_type, attack_mode='hybrid')
            print("Starting hybrid attack...")
            try:
                result = hybrid_attack(hash_value, hash_type, dictionary_file, bruteforce_options)
                print(f"Attack result: {result}")
            except Exception as e:
                print(f"An error occurred during the hybrid attack: {e}")
        if result:
            session.mark_complete()

if __name__ == "__main__":
    main()
