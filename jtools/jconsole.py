from collections.abc import Iterable
import colorama
from colorama import Fore
import progress.bar # console progress bar module
import sys

#initliaze colorama so colors can be used in console text
colorama.init()
#reset formatting
endc = '\033[0m'
Bar = progress.bar.Bar # allows scripts to access the Bar class by importing jconsole

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
    colorama.reinit()
    if len(variables) == 0:
        print(bold(blue('here')))
        return
    else:
        print(_recursively_add_vars(variables))

def _recursively_add_vars(iterable, label_index='', indent_lvl=0):
    """Recursively add iterables to the printstring.

    This function is only called from within test()"""
    indent = '    '
    printstring = ''
    for i in range(len(iterable)):
        if indent_lvl == 0:
            printstring += bold(purple(f'var {i}:\n'))
        curr_value = iterable[i]
        if isinstance(curr_value, str) or not isinstance(curr_value, Iterable):
            if indent_lvl < 2:
                printstring += indent + yellow(str(curr_value)) + '\n'
            else:
                printstring += (indent * indent_lvl) + yellow(str(curr_value)) + '\n'
        else:
            printstring += _recursively_add_vars(curr_value, label_index=i, indent_lvl=indent_lvl + 1)
    return printstring



def ptest(*variables, inline=False):
    """ Pass all parameters to test() and then pause execution until user presses enter."""
    test(*variables)
    input(red('Process paused. Press any key to un-pause'))


