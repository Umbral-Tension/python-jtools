from collections.abc import Iterable
from typing import KeysView
import colorama
from colorama import Fore
import progress.bar # console progress bar module
import os
import sys

# initialize colorama so colors can be used in console text
colorama.init()
# reset formatting
endc = '\033[0m'
Bar = progress.bar.Bar # allows scripts to access the Bar class by importing jconsole

# return a string that will print the passed parameter in a given color
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

def q(str):
    return f'"{str}"'
    
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
    sys.exit(0)

def cls():
    os.system('cls')

def zen(message='here', title=f'debug info'):
    """Use zenity on linux to display a popup window showing the content of message."""
    os.system(f'zenity --title "{title}" --info --text "{message}"')

def test_(*variables, indent=4, tracers=True, truncate=True):
    """returns the pretty-print string from test() instead of printing it."""
    return _recursively_add_vars(variables, indent=indent, tracers=tracers, truncate=truncate)

def test(*variables, indent=4, tracers=True, truncate=True):
    """pretty print all items in *variables.
    
    @param indent: size of indent to use for nested items
    @param tracers: if true, vertical alignment lines are added for readability
    @param truncate: attempt to fit the printed content to the console window better
    """
    colorama.reinit()
    if len(variables) == 0:
        print(bold(blue('here')))
    else:
        print('\n'.join(_recursively_add_vars(variables, indent=indent, tracers=tracers, truncate=truncate)))

def ptest(*variables, inline=False):
    """ Pass all parameters to test() and then pause execution until user presses enter."""
    test(*variables)
    input(red('Process paused. Press any key to un-pause'))


def _recursively_add_vars(iterable, list_of_lines = [], indent_lvl=0, droplines=[], indent=4, tracers=True, truncate=True):
    """Recurse into iterables, adding their values to the printstring that test() will ultimately display. This function 
    is only called from within test()
    
    @param droplines: list of indent lvls. Tracks which indentation lvls currently need tracer dots.
    """
    lol = list_of_lines
    indent_str = ' ' * indent * indent_lvl
    iterable_is_dictionary = isinstance(iterable, dict)
    keys = list(iterable.keys()) if iterable_is_dictionary else []
    
    # The first call of _recursively...() is always done by test() which always passes in its *variables parameter.
    # *variables is an iterable so there is no 'isIterable' check necessary at this outer scope. 
    for i in range(len(iterable)): 
        
        # the 0th indentation lvl refers to the top lvl variables that were actually passed to the test() function.
        # These will be labeled in the display as "test_var 2: " and so on. 
        if indent_lvl == 0:
            lol.append(bold(purple(f'var {i}:')))

        # curr_value is the single object 'under consideration'.
        curr_value = iterable[keys[i]] if iterable_is_dictionary else iterable[i]
        curr_value_is_primitive = is_primitive(curr_value)

        # build formatted print line
        line = _build_line(iterable, iterable_is_dictionary, keys, i, curr_value, \
            curr_value_is_primitive, indent_lvl, indent, tracers, droplines, truncate)
        if not line is None:
            lol.append(line)

        # Continue recursion if curr_value is not a primitive. 
        if not curr_value_is_primitive:
            if i < len(iterable)-1 and indent_lvl != 0:
                droplines.append(indent_lvl)
            lol = _recursively_add_vars(curr_value, list_of_lines=lol, indent_lvl=indent_lvl+1,\
                 indent=indent, tracers=tracers, droplines=droplines, truncate=truncate) 
    try:
        droplines.remove(indent_lvl)
    except:
        pass
    return lol


def _build_line(iterable, iterable_is_dictionary, keys, curr_index, curr_value,
 curr_value_is_primitive, indent_lvl, indent, tracers, droplines, truncate):
    """Produce a nicely formatted line of text to be used by _recursively_add_vars()"""
    i = curr_index
    curr_val_type = str(type(curr_value)).replace('class ', '').replace("'", "")
    
    # build indentation string w or w/o tracers
    indent_str = ' ' * indent * indent_lvl
    if tracers:
        indent_str = list(indent_str)
        for x in droplines:
            if x != indent_lvl:
                dot = purple('·') # middle dot char is U+00B7
                dropindex = (x * indent)
                try:
                    indent_str[dropindex] = dot
                except:
                    pass
        indent_str = ''.join(indent_str)
    
    
    line = ''
    # Seperate formatting instructions for dictionaries
    if iterable_is_dictionary:
        # we always want to print dictionary keys, even if their associated value is another iterable
        line = f'{indent_str}{cyan("key:")}{yellow(keys[i])}{cyan(" value:")}'
        if curr_value_is_primitive:
            line += f'{yellow(str(curr_value))}'
        else:
            line += f'{curr_val_type}'
    else:
        if curr_value_is_primitive:
            if indent_lvl == 0:
                indent_str += ' ' * indent
            if isinstance(iterable, list):
                line = indent_str + cyan(f'{i}|') + yellow(str(curr_value))
            else:
                line = indent_str + yellow(str(curr_value))
        else: 
            if indent_lvl != 0:
                line = f'{indent_str}{cyan(f"{i}|")}{curr_val_type}'
            else:
                return None
    return line




import builtins
builtin_types = [getattr(builtins, d) for d in dir(builtins) if isinstance(getattr(builtins, d), type)]
def is_primitive(obj):
    """Return true if obj is a 'primitive', defined as being one of (non-iterable, string, set, non-builtin iterable)."""
    is_iterable = isinstance(obj, Iterable)
    is_str_or_set = isinstance(obj, (str, set))
    #iterable objects for which I wouldn't know how best to print them anyway are printed as is. 
    is_non_standard_iterable = is_iterable and type(obj) not in builtin_types

    is_primitive = is_str_or_set or not is_iterable or is_non_standard_iterable
    return is_primitive

# formatted dir() function 
def dir_(obj):
    import inspect
    from inspect import isclass, isfunction, ismethod, isbuiltin
    reg_dir = dir(obj)
    new_dir = {'classes': [], 'functions': [], 'methods': [], 'attributes': []}

    # TODO figure out how to neatly print part of the doc string for object attributes
    def attr_str(attr, attr_name):
        # doc = attr.__doc__
        # if isinstance(doc, str):
        #     doc = doc[:40].replace('\\n', '  ').replace('\r', '  ').strip()
        #     return (attr_name, doc)
        # else:
        #     return attr_name
        return attr_name

    for x in reg_dir:
        attr = getattr(obj, x)
        if x.startswith('_') or x.isupper():
            continue
        elif isfunction(attr) or isbuiltin(attr):
            new_dir['functions'].append(attr_str(attr, x))
        elif isclass(attr):
            new_dir['classes'].append(attr_str(attr, x))
        elif ismethod(attr):
            new_dir['methods'].append(attr_str(attr, x))
        else:
            new_dir['attributes'].append(attr_str(attr, x))
    return new_dir



    
if __name__ == '__main__':
    pass