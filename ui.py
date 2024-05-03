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
import os
import time
from AI import generate_wordlist
from AI import collect_sensitive_information
from AI import get_api_key
from hash_identifier import identify_hash_types as identify_hash
from session_manager import *
from logger import log_hash, log_attack_mode
from attack_methods import hybrid_attack, bruteforce_attack, dictionary_attack
from banner import display_banner   # Assuming this is the attack method used

import os
import time
import math


banner_text = """
                                                                                                  
                                                                                                  
    ,---,.                                      ,---,.                                            
  ,'  .' |                            ,---,   ,'  .' |                                            
,---.'   |   __  ,-.                ,---.'| ,---.'   |    ,---.     __  ,-.                       
|   |   .' ,' ,'/ /|                |   | : |   |   .'   '   ,'\  ,' ,'/ /|                       
:   :  :   '  | |' |    ,---.       |   | | :   :  :    /   /   | '  | |' |    ,---.      ,---.   
:   |  |-, |  |   ,'   /     \    ,--.__| | :   |  |-, .   ; ,. : |  |   ,'   /     \    /     \  
|   :  ;/| '  :  /    /    /  |  /   ,'   | |   :  ;/| '   | |: : '  :  /    /    / '   /    /  | 
|   |   .' |  | '    .    ' / | .   '  /  | |   |   .' '   | .; : |  | '    .    ' /   .    ' / | 
'   :  '   ;  : |    '   ;   /| '   ; |:  | '   :  '   |   :    | ;  : |    '   ; :__  '   ;   /| 
|   |  |   |  , ;    '   |  / | |   | '/  ' |   |  |    \   \  /  |  , ;    '   | '.'| '   |  / | 
|   :  \    ---'     |   :    | |   :    :| |   :  \     `----'    ---'     |   :    : |   :    | 
|   | ,'              \   \  /   \   \  /   |   | ,'                         \   \  /   \   \  /  
`----'                 `----'     `----'    `----'                            `----'     `----'   
                                                                                                 
"""




def red_input(prompt):
    """
    Displays the input prompt in red and returns the user's input.
    """
    return input(f"\033[31m{prompt}\033[0m")

def get_user_input(prompt):
    return red_input(prompt)

def main():
    display_banner(banner_text)
    if not os.path.exists('api_key.txt'):
        api_key = get_user_input("Enter your OpenAI API key: ")
        if api_key:
            with open('api_key.txt', 'w') as file:
                file.write(api_key)
            os.environ['OPENAI_API_KEY'] = api_key  # Set the environment variable
    else:
        api_key = get_api_key()
    from AI import initialize_client
    initialize_client()  # Initialize the OpenAI client after setting the API key
    generate_wordlist_choice = red_input("Would you like to generate a wordlist? (y/n): ")
    
    if generate_wordlist_choice.lower() == 'y':
        print("Generating wordlist...")
        sensitive_info = collect_sensitive_information()
        file_path = red_input("Enter the directory path to save the wordlist: ")
        file_name = red_input("Enter the filename for the wordlist: ")
        wordlist = generate_wordlist(sensitive_info, file_path=file_path, file_name=file_name)
        print("Wordlist generated.")
    
    elif generate_wordlist_choice.lower() != 'n':
        print("Invalid input. Please enter 'y' or 'n'.")
        return  # Exit or repeat the query

    continue_attack = red_input("Do you want to continue the previous session? (y/n): ")

    if continue_attack.lower() not in ['y', 'n']:
        print("Invalid input. Please enter 'y' or 'n'.")
        return  # Exit or repeat the query
    
    if continue_attack.lower() == 'n':
        print("Starting a new session...")
        session = SessionManager(create_new=True)
        session.session_data = {}
        # Get hash from user
        hash_value = red_input("Enter the hash you want to crack: ")
        session.session_data['hash_value'] = hash_value  # Save the hash_value into session data
        session.save_session()  # Save the session after updating
        log_hash(hash_value)
        
        # Identify or confirm hash type
        print(identify_hash(hash_value))
        hash_type = red_input("Enter hash type: ")
        new_hash_type = red_input(f"Identified hash type as {hash_type}. Press Enter to confirm or type a different one: ")
        if new_hash_type:
            hash_type = new_hash_type
        session.session_data['hash_mode'] = hash_type  # Update session data immediately after first input
        
        # Select attack mode
        print("Available attack modes: [1] BruteForce [2] Dictionary [3] Hybrid")
        attack_mode = red_input("Select an attack mode (number): ")
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
            bruteforce_options = red_input("Enter bruteforce options (e.g., 'L:N:@'): ")
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
            dictionary_file = red_input("Enter path to dictionary file: ")
            session.update_session(hash_value=hash_value, hash_mode=hash_type, attack_mode='dictionary_attack', dictionary_file=dictionary_file)
            try:
                result = dictionary_attack(hash_value, hash_type, dictionary_file)
                print(f"\033[91mAttack result: {result}\033[0m")  # Output in red
            except Exception as e:
                print(f"\033[91mAn error occurred during the dictionary attack: {e}\033[0m")  # Output in red

        elif attack_mode == '3':
            print("Hybrid mode selected. This mode combines dictionary and brute force attacks.")
            dictionary_file = red_input("Enter path to dictionary file: ")
            print("For the brute force component, specify the character sets to use:")
            print("  'l' for lowercase letters (a-z)")
            print("  'L' for uppercase letters (A-Z)")
            print("  'N' for numbers (0-9)")
            print("  '@' for symbols (all printable ASCII symbols)")
            print("Enter a pattern as a combination of 'l', 'L', 'N', and '@'.")
            print("Example pattern: 'L:N:@' for uppercase letters, numbers, and symbols.")
            print("You can also specify multiple segments separated by ':' where each segment will be treated as a separate part of the brute force attack.")
            bruteforce_options = red_input("Enter bruteforce options: ")
            print("Enter the position to append brute force options:")
            print("  'start' to prepend to the beginning of the word")
            print("  'end' to append to the end of the word")
            print("  or enter a specific numeric index to insert within the word")
            position = red_input("Choose position (start, end, or index): ")
            result = hybrid_attack(hash_value, hash_type, dictionary_file, bruteforce_options, position)
            print(f"Attack result: {result}")
        if result:
            session.mark_complete()

if __name__ == "__main__":
    main()


