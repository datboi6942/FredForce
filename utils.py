#utils.py will contain all the logic for the utils
#this includes the logic for the loading bar and other utilities to be added in the future

import sys
import time

def loading_bar(total, current, message="Progress", style_toggle=False):
    """
    Displays or updates a console progress bar.

    Args:
    total (int): Total iterations.
    current (int): Current iteration.
    message (str): A message displayed next to the progress bar.
    """
    bar_length = 40
    fraction = current / total
    arrow = int(fraction * bar_length - 1) * '-' + '>'
    padding = int(bar_length - len(arrow)) * ' '

    bar_char = '#' if style_toggle else '*'
    sys.stdout.write(f"\r{message}: [{bar_char * int(fraction * bar_length)}{padding}] {int(fraction*100)}%")
    sys.stdout.flush()

    if current == total:
        sys.stdout.write('\n')
    else:
        # Toggle the style for the next update
        loading_bar(total, current + 1, message, not style_toggle)

# Example usage of loading_bar
if __name__ == "__main__":
    for i in range(101):
        time.sleep(0.1)
        loading_bar(100, i, message="Loading")