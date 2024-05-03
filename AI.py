# AI.py - Module for integrating GPT-4 to generate wordlists for hash cracking

from openai import OpenAI
import os
import sys

def red_input(prompt):
    """
    This function prints the prompt in red and returns the input provided by the user.
    """
    sys.stdout.write("\033[91m" + prompt)
    user_input = input()
    sys.stdout.write("\033[0m")  # Reset the color to default
    return user_input

def get_api_key():
    try:
        with open('api_key.txt', 'r') as file:
            api_key = file.read().strip()
            return api_key
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
api_key = get_api_key()
client = None  # Initialize client as None

def initialize_client():
    global client
    client = OpenAI(api_key=api_key)


# Function to collect sensitive information from the user
def collect_sensitive_information():
    """
    Prompts the user to enter sensitive information about the target.

    Returns:
    str: A string containing all the sensitive information concatenated.
    """
    prompts = {
        "First and last name": "",
        "Birthday": "",
        "Country": "",
        "City/Town": "",
        "Names of relatives": "",
        "Pets": "",
        "Last 4 digits of SSN": "",
        "Address": "",
        "Previous address": "",
        "Email": "",
        "Phone number": "",
        "Schools attended": "",
        "Mother's maiden name": "",
        "Favorite teacher": "",
        "High school mascot": "",
        "Spouse": "",
        "Favorite food": "",
        "Favorite color": "",
        "Make and model of car": "",
        "Nearest living sibling": "",
        "College graduated from": "",
        "Anniversary date": "",
        "Kids' names": ""
    }
    
    print("Please enter the following sensitive information about the target:")
    for prompt in prompts:
        prompts[prompt] = red_input(f"{prompt}: ")
    
    # Concatenate all information into a single string
    sensitive_info = ", ".join(f"{key}: {value}" for key, value in prompts.items() if value)
    return sensitive_info

# Function to generate wordlist based on user-provided information
def generate_wordlist(sensitive_info, model="gpt-4", max_tokens=5000, file_path='.', file_name='generated_wordlist.txt'):
    """
    Generates a wordlist using GPT-4 based on the provided sensitive information, querying for passwords based on the context of all the sensitive information.

    Args:
    sensitive_info (str): String containing concatenated sensitive information about the user/target for wordlist generation.
    model (str): Identifier for the GPT model to use.
    max_tokens (int): Maximum number of tokens to generate.
    file_path (str): The directory path where the wordlist file will be saved.
    file_name (str): The filename for the wordlist file.

    Returns:
    list: A list of potential passwords.
    """
    wordlist = []
    try:
        with open(os.path.join(file_path, file_name), 'w') as file:  # Open file in write mode using the specified path and filename
            while len(wordlist) < 100:  # Loop until at least 100,000 words are generated
                prompt = f"Generate a list of potential passwords based on the following details: {sensitive_info} Passwords must be 8-20 characters contain 1 capital and 1 speical character "
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "system", "content": prompt}],
                    max_tokens=max_tokens,
                    n=1,
                    stop=None,
                    temperature=0.8
                )
                # Filter words to meet length requirements
                potential_words = response.choices[0].message.content.strip().split('\n')
                valid_words = [word for word in potential_words if 8 <= len(word) <= 20 and not word[0].isdigit()]
                for word in valid_words:
                    file.write(word + '\n')  # Write each word to the file
                wordlist.extend(valid_words)
    except Exception as e:
        print(f"An error occurred: {e}")
    return wordlist

# Example usage
if __name__ == "__main__":
    sensitive_info = collect_sensitive_information()
    wordlist = generate_wordlist(sensitive_info)
    print(wordlist)
