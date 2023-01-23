"""some string utilities """
import string

def replace_by_index(s, i, replacement=''):
    """
    replace the character in s at index i with the strign replacement.
    
    CAUTION: I don't think strings are supposed to be mutable in this way so take care when updating strings
    that are being iterated through. 
    """
    l = list(s)
    l[i] = replacement
    return ''.join(l)

def get_all_indices(s: str, substr: str)->list:
    """
    return a list of indices where substr is found within s
    """
    start = 0
    indices = []
    while start < len(s):
        i = s.find(substr, start)
        if i == -1:
            break
        else:
            indices.append(i)
        start = i + 1
    return indices

def capitalize_abbreviations(s:str):
    """
    return a string with all abbreviations capitalized such as 'M.', 'M.O.', 'M.O'
    """
    i = 1
    while i < len(s):
        if s[i] == '.' and s[i-1] in string.ascii_letters:
            start = i-1 # start of abbreviation
            end = None
            j = i
            #test(s, i, s[i])
            while j+2 < len(s):
                # print(tg.red('loop 2')+'\n\t'+s+'\n')
                if s[j+1] in string.ascii_letters: 
                    if s[j+2] != '.': # abbreviation ends on character
                        end = j+1
                        i = j+3
                        break
                    else:
                        j = j+2
                else: # abbreviation ends on period
                    end = j
                    i = j+1
                    break
            # reaching this line indicates that the string ends on the presumed abbreviation. 
            end = j
            i = j+1

            if end is not None: 
                # test if the supposed abbreviation is surrounded by non-letters. This filters out strings like
                # 'abc.def' or ' f.mp3' which would otherwise be matched. 
                pre, post = True, True
                if start-1 >=0 and s[start-1] in string.ascii_letters:
                    pre = False
                if end+1 < len(s) and s[end+1] in string.ascii_letters:
                    post = False
                if pre and post:
                    for x in range(start, end+1):
                        s = replace_by_index(s, x, s[x].upper())
        else:
            i += 1
    return s

def contains_abbreviation(s:str):
    """
    return true if an abbreviation like O.G. or O.G is found in s
    """
    i = 1
    while i < len(s):
        if s[i] == '.' and s[i-1] in string.ascii_letters:
            start = i-1 # start of abbreviation
            end = None
            j = i
            #test(s, i, s[i])
            while j+2 < len(s):
                # print(tg.red('loop 2')+'\n\t'+s+'\n')
                if s[j+1] in string.ascii_letters: 
                    if s[j+2] != '.': # abbreviation ends on character
                        end = j+1
                        i = j+3
                        break
                    else:
                        j = j+2
                else: # abbreviation ends on period
                    end = j
                    i = j+1
                    break
            # reaching this line indicates that the string ends on the presumed abbreviation. 
            end = j
            i = j+1

            if end is not None: 
                # test if the supposed abbreviation is surrounded by non-letters. This filters out strings like
                # 'abc.def' or ' f.mp3' which would otherwise be matched. 
                pre, post = True, True
                if start-1 >=0 and s[start-1] in string.ascii_letters:
                    pre = False
                if end+1 < len(s) and s[end+1] in string.ascii_letters:
                    post = False
                if pre and post:
                    return True
        else:
            i += 1
    return False

def capitalize_roman_numerals(s:str):
    """
    Cappitalize roman numerals between 1 and 30, (those containing only characters I-V-X)
    
    does not make an effort to determine if the roman numeral is valid, only whether there is a set of 
    IVX characters surrounded by non-alphabet characters. ie 'III A String' or 'A string with xIv in it'.  

    The word vix in 'vix vapo rub' will be capitalized. Necessary evil. 
    """
    roms = 'ivxIVX'
    valid_surrounds = ' \t\n()[]{}\'"'
    i = 0
    while i < len(s):
        if s[i] in roms:
            start = i
            end = None
            j = i
            while j+1 < len(s):
                if s[j+1] in roms:
                    j = j+1
                    continue
                else:
                    end = j
                    i = j+1
                    break
            end = j 
            i = j + 1
            
            pre, post = False, False
            if start-1 > -1:
                if s[start-1] in valid_surrounds:
                    pre = True
            else:
                pre = True
            if end+1 < len(s): 
                if s[end+1] in valid_surrounds:
                    post = True
            else:
                post = True
            if pre and post:
                for x in range(start, end+1):
                    s = replace_by_index(s, x, s[x].upper())
                i = end + 1
                continue
        else:
            i += 1
    return s
    
def advanced_titlecase(s:str):
    """
    capitalize characters that follow white space or bracket-type characters, abbreviations, roman numerals.  
    """

    # Capitalize all alpha characters that follow a whitespace. 
    s = string.capwords(s)

    # capitalize all alpha characters that follow the opening of bracket-type characters or a slash. 
    specials = '"([{/\\'
    for c in specials:
        indices = get_all_indices(s, c)
        for i in indices:
            s = replace_by_index(s, i+1, str.upper(s[i+1]))
    
    # detect and capitalize abreviations  
    s = capitalize_abbreviations(s)
    s = capitalize_roman_numerals(s)
    return s

