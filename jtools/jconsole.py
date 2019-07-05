from collections.abc import Iterable

# console escape sequences for changing display settings.
white = '\033[0;30m'
gray = '\033[0;37m'
blue = '\033[0;34m'
green = '\033[0;32m'
cyan = '\033[0;36m'
red = '\033[0;31m'
purple = '\033[0;35m'
yellow = '\033[0;33m'
underline = '\033[4m'
bold = '\033[1m'
endc = '\033[0m'  # reset console formatting
colors = (white, gray, blue, green, cyan, red,
          purple, yellow, underline, bold, endc)


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
    if len(variables) == 0:
        print(blue + 'here' + endc)
        return

    for i in range(0, len(variables)):
        curr = variables[i]
        printstring = bold + purple + f'var {i}:\t' + endc
        if not isinstance(curr, Iterable) or isinstance(curr, str):
            printstring += yellow + f'{variables[i]}' + endc
        else:
            enumeration_string = bold + blue + ', ' if inline else '\n\t\t'
            index = 0
            for x in curr:
                printstring += ('' if index == 0 else enumeration_string) + yellow + str(x) + endc
                index += 1
        print(printstring)
    print(endc)
    return


def ptest(*variables, inline=False):
    """ Pass all parameters to test() and then pause execution until user presses enter."""
    test(*variables, inline=inline)
    print(red)
    input('Process paused. Press any key to un-pause')
    print(endc)
