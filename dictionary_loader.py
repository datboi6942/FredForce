#contains all the logic for loading the user selected dictionary file

#prompt the user for path to dictionary file


def load_dictionary(dictpath):
    try:
        with open(dictpath, 'r', encoding='utf-8', errors='ignore') as f:
            dictionary = [line.strip() for line in f]
        print(f"{len(dictionary)} valid passwords loaded.")
        return dictionary
    except FileNotFoundError:
        print("The specified dictionary file was not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
