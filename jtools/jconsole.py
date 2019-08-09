from collections.abc import Iterable
import colorama
from colorama import Fore

#initliaze colorama so colors can be used in console text
colorama.init()
#reset formatting
endc = '\033[0m'

#return a string that will print the passed parameter in a given color
def white(text):
    return Fore.WHITE + str(text) + endc

def blue(text):
    return Fore.BLUE + str(text) + endc

def green(text):
    return Fore.GREEN + str(text) + endc

def cyan(text):
    return Fore.CYAN + str(text) + endc

def red(text):
    return Fore.RED + str(text) + endc

def purple(text):
    return Fore.MAGENTA + str(text) + endc

def yellow(text):
    return Fore.YELLOW + str(text) + endc

def underline(text):
    return '\033[4m' + str(text) + endc

def bold(text):
    return '\033[1m' + str(text) + endc


def yes_no(s=''):
    """Prompt user for a yes or no response."""
    while True:
        response = input(s + ' (Y/N):')
        if response.lower() == 'y':
            return True
        elif response.lower() == 'n':
            return False
        else:
            print('Use the \'Y\'/\'N\' keys to choose Yes or No')
    

def exit_app(exit_message=''):
    """Display exit message, then wait for user to press enter before running exit()"""
    print(red(exit_message))
    input('\nPress Enter to exit the program')
    exit()
    

def test(*variables, inline=False):
    """Print the list of parameters with some helpful formatting.

    Option to print iterables horizontally, 'inline'. If no parameters are given, test() will print 'here'."""
    colorama.reinit()
    if len(variables) == 0:
        print(blue('here'))
        
        return

    for i in range(0, len(variables)):
        curr = variables[i]
        printstring = bold(purple(f'var {i}:\t'))
        if not isinstance(curr, Iterable) or isinstance(curr, str):
            printstring += yellow(f'{variables[i]}')
        else:
            enumeration_string = bold(blue(', ' if inline else '\n\t\t'))
            index = 0
            for x in curr:
                printstring += ('' if index == 0 else enumeration_string) + yellow(str(x))
                index += 1
        print(printstring)
    

def ptest(*variables, inline=False):
    """ Pass all parameters to test() and then pause execution until user presses enter."""
    test(*variables, inline=inline)
    input(red('Process paused. Press any key to un-pause'))

    

exit_app(('sdfdsfsdf'))