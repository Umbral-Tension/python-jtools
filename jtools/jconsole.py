from collections.abc import Iterable

# console escape sequences for changing display settings.
black = '\033[0;30m'
dark_gray = '\033[1;30m'
white = '\033[1;37m'
blue = '\033[0;34m'
green = '\033[0;32m'
cyan = '\033[0;36m'
red = '\033[0;31m'
purple = '\033[0;35m'
brown = '\033[0;33m'
yellow = '\033[1;33m'
gray = '\033[0;37m'
light_blue = '\033[1;34m'
light_green = '\033[1;32m'
light_cyan = '\033[1;36m'
light_red = '\033[1;31m'
light_purple = '\033[1;35m'
underline = '\033[4m'
bold = '\033[1m'
endc = '\033[0m'  # reset console formatting


def yes_no(s=''):
    """Prompt user for a yes or no response."""
    while True:
        response = input(s + ' (Y/N)')
        if response.lower() == 'y':
            return True
        elif response.lower() == 'n':
            return False
        else:
            print('Use the \'Y\'/\'N\' keys to choose Yes or No')


def exit_app(exit_message=''):
    """Display exit message, then wait for user to press enter before running exit()"""
    print(red + exit_message + endc)
    input('\nPress Enter to exit the program')
    exit()


def test(*variables, inline=False):
    """Print the list of parameters with some helpful formatting.

    Option to print iterables horizontally, 'inline'. If no parameters are given, test() will print 'here'."""
    print(type(variables), type(variables[0]), variables[0])
    if len(variables) == 0:
        print('here')
        return

    for i in range(0, len(variables)):
        curr = variables[i]
        printstring = f'var {i}:\t'
        if not isinstance(curr, Iterable) or isinstance(curr, str):
            printstring += f'{variables[i]}'
        else:
            enumeration_string = ',' if inline else '\n\t\t'
            index = 0
            for x in curr:
                printstring += ('' if index == 0 else enumeration_string) + str(x)
                index += 1
        print(printstring)
    return


def ptest(*variables, inline=False):
    """ Pass all parameters to test() and then pause execution until user presses enter."""
    test(*variables, inline=inline)
    print(red)
    input('Process paused. Press any key to un-pause')
    print(endc)


