from collections.abc import Iterable
import colorama
from colorama import Fore
import progress.bar # console progress bar module
import os

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

def cls():
    os.system('cls')

def test(*variables):
    colorama.reinit()
    if len(variables) == 0:
        print(bold(blue('here')))
    else:
        print(_recursively_add_vars(variables))

def _recursively_add_vars(iterable, label_index='', indent_lvl=0):
    """Recurse into iterables and add their values to the printstring that test() will ultimately display.

    This function is only called from within test()"""
    printstring = ''
    BASE_INDENT = '    '
    iterable_is_dictionary = isinstance(iterable, dict)
    if iterable_is_dictionary:
        keys = sorted(list(iterable.keys()))
    # The first call of recursively...() is always done by test() which always passes in its *variables parameter.
    # *variables is an iterable so there is no 'isIterable' check necessary at this outer scope. 
    for i in range(len(iterable)): 
        
        # the 0th indentation lvl refers to the top lvl variables that were actually passed to the test() function.
        # These will be labeled in the display as " test_var 2: " and so on. 
        if indent_lvl == 0:
            printstring += bold(purple(f'test_var {i}:\n'))

        # curr_value is the single object 'under consideration' (for a given loop interation of a given function call)
        # It will be checked to see if it is a simple value that's okay to print, or if it is an iterable that needs to be recursed into further. 
        # note: dictionaries cannot be indexed by just i, so a list of the dictionary's keys is made which CAN be indexed by i. 
        curr_value = iterable[keys[i]] if iterable_is_dictionary else iterable[i]
        
        # This is the recursive function's base case. It stops recursing when it finds a string or non-iterable
        # because it makes sense to print these primitives 'as-is'
        curr_value_is_primitive = isinstance(curr_value, str) or isinstance(curr_value, bool) or not isinstance(curr_value, Iterable)
        
        indent_str = BASE_INDENT * indent_lvl 
        if indent_lvl > 0 and i == 0:
            itertype = type(iterable)
            printstring += f'{indent_str}{bold(itertype)}\n'
        
        if iterable_is_dictionary: # we always want to print dictionary keys, even if their value is another iterable
           printstring += f'{indent_str}{cyan("key:")}{yellow(keys[i])}{cyan(" value:")} '
           if not(curr_value_is_primitive):
               printstring += '\n' # don't want to start printing a lower nested iterable on the same line as the upper dictionary key
        if curr_value_is_primitive:
            if iterable_is_dictionary: #special formatting required for dicitonaries
                printstring += f'{yellow(iterable[keys[i]])}\n'
            else:
                printstring += indent_str + yellow(str(curr_value)) + '\n'
        
        # Continue recursion if curr_value is an iterable. 
        if not(curr_value_is_primitive):
            printstring += _recursively_add_vars(curr_value, label_index=i, indent_lvl=indent_lvl + 1)
    return printstring



def ptest(*variables, inline=False):
    """ Pass all parameters to test() and then pause execution until user presses enter."""
    test(*variables)
    input(red('Process paused. Press any key to un-pause'))


# formatted dir() function 
def dir_(obj):
    import inspect
    from inspect import isclass, isfunction, ismethod        
    # meant to 'overide' inspect.getmembers()
    def getmembers(obj, predicate):
        member_tuples = inspect.getmembers(obj, predicate)
        # extract and return just the names from the (name, value) tuples given by inspect module
        names = [x[0] for x in member_tuples]
        return [x for x in names if not x.startswith('_')]
    
    classes = getmembers(obj, isclass)
    functions = getmembers(obj, isfunction)
    methods = getmembers(obj, isclass)
    return {'classes': classes, 'functions': functions, 'methods': methods}


    
