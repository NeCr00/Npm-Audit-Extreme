import sys
import os

# Check if the OS is Windows, and if so, import colorama and initialize it
if os.name == 'nt':
    import colorama
    colorama.init()

class Log:
    # Define a private method for logging with color
    @staticmethod
    def _log(message, color):
        # Define color codes and reset code for both Windows and other platforms
        if os.name == 'nt':
            colors = {
                'red': colorama.Fore.RED,
                'green': colorama.Fore.GREEN,
                'blue': colorama.Fore.BLUE
            }
            reset = colorama.Style.RESET_ALL
        else:
            colors = {
                'red': '\033[91m',
                'green': '\033[92m',
                'blue': '\033[94m'
            }
            reset = '\033[0m'

        # Write the message to stdout with the specified color and reset formatting
        sys.stdout.write(f"{colors[color]}{message}{reset}\n")
        sys.stdout.flush()

    # Define public methods for logging with different colors
    @staticmethod
    def error(message):
        Log._log(message, 'red')

    @staticmethod
    def success(message):
        Log._log(message, 'green')

    @staticmethod
    def info(message):
        Log._log(message, 'blue')
