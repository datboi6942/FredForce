#session_manager.py will contain all the logic for managing the session
#this includes saving the users options for the active session
#this includes saving the progress of the attack continusly unless the session completes successfully and hash is cracked
#this includes printing how to resume the session  as soon as the attack begins

import json
import os

class SessionManager:
    def __init__(self, session_file='session.json', create_new=False):
        self.session_file = session_file
        self.session_data = {
            'hash_value': None,
            'hash_mode': None,
            'attack_mode': None,
            'dictionary_file': None,
            'total_words': 0,
            'progress': 0,
            'complete': False,
            'bruteforce_options': None  # Add default bruteforce options here
        }
        if not create_new:
            self.load_session()

    def load_session(self, progress=None):
        try:
            if os.path.exists(self.session_file):
                with open(self.session_file, 'r') as file:
                    self.session_data = json.load(file)
                if progress:
                    self.session_data['progress'] = progress
                print(json.dumps(self.session_data, indent=4))
            else:
                print("No existing session found. Starting a new session.")
        except json.JSONDecodeError:
            print("Error decoding session file. Check file format.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def save_session(self):
        with open(self.session_file, 'w') as file:
            json.dump(self.session_data, file)
        print("Session saved.")

    def update_session(self, **kwargs):
        self.session_data.update(kwargs)
        print(f"Debug: Session data updated - {self.session_data}")
        if 'attack_mode' in kwargs and kwargs['attack_mode'] == 'bruteforce':
            self.session_data['bruteforce_options'] = kwargs.get('bruteforce_options', '')
            self.save_session()
        elif 'attack_mode' in kwargs and kwargs['attack_mode'] == 'hybrid':
            self.session_data['hybrid_options'] = kwargs.get('hybrid_options', '')
            self.save_session()

    def mark_complete(self):
        self.session_data['complete'] = True
        self.save_session()
        print("Session marked as complete.")

    def update_progress(self, progress=0):
        self.session_data['progress'] = progress
        self.save_session()

    def update_total_words(self, total_words):
        self.session_data['total_words'] = total_words
        self.save_session()

# Example usage:
if __name__ == "__main__":
    manager = SessionManager()
    manager.update_session(hash_value='abc123', hash_mode='SHA-256', attack_mode='Hybrid', dictionary_file='dict.txt')
    manager.mark_complete()
