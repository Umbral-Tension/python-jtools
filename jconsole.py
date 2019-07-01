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


# prompts for a yes or no response.
def yes_no(s=''):
    while True:
        response = input(s + ' (Y/N)')
        if response.lower() == 'y':
            return True
        elif response.lower() == 'n':
            return False
        else:
            print('Use the \'Y\'/\'N\' keys to choose Yes or No')


def exit_app(exit_message=''):
    print(red + exit_message + endc)
    input('\nPress Enter to exit the program')
    exit()

# Debugging tool that prints the contents of whatever variables are passed to it w/ some
# helpful formatting. Option to print iterables horizontally 'inline'.
# If no parameters are passed, test() will print 'here'.
#todo currently there's an issue where ptest is passing in a tuple whose only element
# is a tuple that contains the parameters originally passed to ptest(). This results in
# test() printing them all under 'var 0:' vertically.
# Maybe introduce a recusion level tracker / exception for ptest() / make inline a boolean function parameter.
def test(*variables):
    print(type(variables), type(variables[0]), variables[0])
    if len(variables) == 0:
        print('here')
        return
    inline = True if str(variables[0]) == 'jinline' else False
    enumeration_string = ',' if inline else '\n\t'
    start = 1 if inline else 0

    for i in range(start, len(variables)):
        curr = variables[i]
        printstring = f'var {i}: '
        if not isinstance(curr, Iterable) or isinstance(curr, str):
            printstring += f'\t{variables[i]}'
        else:
            if inline:
                printstring += '\t'
            index = 0
            for x in curr:
                #printstring = printstring + '\t' if index == 0 else printstring
                printstring += ('' if index == 0 else enumeration_string) + str(x)
                index += 1
        print(printstring)
    return


def ptest(*variables):
    test(variables)
    print(red)
    input('Process paused. Press any key to un-pause')
    print(endc)


test('jinline', 'sdfsdf', (2,4,5,0))
print('-------------------------')
ptest('jinline', 'sdfsdf', (2,4,5,0))
test()
