#config.py will contain all of the configuration options for the attack
#this includes things like the attack mode, the hash type, the hash value, and the dictionary file to use for the attack


# Pseudocode for config.py

'''1. Define a configuration class or a set of variables to store configuration options:
   - attack_mode: Type of attack (e.g., 'hybrid', 'brute_force', 'dictionary')
   - hash_type: Type of hash used (e.g., 'md5', 'sha256')
   - hash_value: The hash value that needs to be cracked
   - dictionary_file: Path to the dictionary file used for dictionary attacks

2. Initialize default values for each configuration option.

3. Provide a method or mechanism to update these configurations from user input or a configuration file.

4. Include error handling to manage incorrect or unsupported configuration values.

5. Optionally, provide a function to display current configuration settings.'''

class AttackConfig:
    def __init__(self, attack_mode='hybrid', hash_type='sha256', hash_value=None, dictionary_file='dictionary.txt'):
        self.attack_mode = attack_mode
        self.hash_type = hash_type
        self.hash_value = hash_value
        self.dictionary_file = dictionary_file

    def update_config(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                print(f"Warning: {key} is not a valid configuration option.")
                return False
        return True

    def display_config(self):
        print("Current Configuration:")
        print(f"Attack Mode: {self.attack_mode}")
        print(f"Hash Type: {self.hash_type}")
        print(f"Hash Value: {self.hash_value}")
        print(f"Dictionary File: {self.dictionary_file}")

# Example usage
config = AttackConfig()
config.display_config()
config.update_config(hash_value='abc123', dictionary_file='new_dict.txt')
config.display_config()