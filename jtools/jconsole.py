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

def blue(text=''):
    return Fore.BLUE + str(text) + endc

def green(text=''):
    return Fore.GREEN + str(text) + endc

def cyan(text=''):
    return Fore.CYAN + str(text) + endc

def red(text=''):
    return Fore.RED + str(text) + endc

def purple(text=''):
    return Fore.MAGENTA + str(text) + endc

def yellow(text=''):
    return Fore.YELLOW + str(text) + endc

def underline(text=''):
    return '\033[4m' + str(text) + endc

def bold(text=''):
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
    

def test(*variables):
    """Print the list of parameters with some helpful formatting.

    If no parameters are given, test() will print 'here'."""
    colorama.reinit()
    printstring = blue('here') if len(variables) == 0 else ''
    for i in range(0, len(variables)):
        curr_value = variables[i]
        if not isinstance(curr_value, Iterable) or isinstance(curr_value, str):
            printstring += bold(purple(f'var {i}:\n')) + yellow(f'    {curr_value}\n')
        else:
            printstring += _recursively_add_iterable(variables[i], i)
    print(printstring)


def _recursively_add_iterable(iterable, label_index='', indent_lvl=0):
    """Recursively add iterables to the printstring.

    This function is only called from within test()"""
    value_indent = '    ' * (indent_lvl + 1)
    newline = '\n' + value_indent
    printstring = '' if indent_lvl != 0 else bold(purple(f'var {label_index}:'))

    for i in range(len(iterable)):
        curr_value = iterable[i]
        if isinstance(curr_value, Iterable) and not isinstance(curr_value, str):
            printstring += _recursively_add_iterable(curr_value, indent_lvl=indent_lvl + 1)
        else:
            printstring += newline + yellow(str(curr_value))
    return printstring if indent_lvl != 0 else printstring + '\n'



def ptest(*variables, inline=False):
    """ Pass all parameters to test() and then pause execution until user presses enter."""
    test(*variables)
    input(red('Process paused. Press any key to un-pause'))


