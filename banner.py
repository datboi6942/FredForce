import os
import time
import math



import os
import time

def clear_screen():
    """Clears the console screen."""
    if os.name == 'nt':  # for Windows
        os.system('cls')
    else:  # for Mac and Linux(here, os.name is 'posix')
        os.system('clear')

def display_banner(text, duration=10):
    """Displays the ASCII banner with a color cycling effect."""
    colors = [31, 32, 33, 34, 35, 36, 37]  # ANSI color codes for red, green, yellow, blue, magenta, cyan, white
    frames_per_second = 5
    total_frames = duration * frames_per_second

    for frame in range(total_frames):
        clear_screen()
        color_code = colors[frame % len(colors)]  # Cycle through colors
        colored_text = "\n".join(f"\033[{color_code}m{line}\033[0m" for line in text.split('\n'))
        print(colored_text)
        time.sleep(1 / frames_per_second)
        print("\033[0m")




