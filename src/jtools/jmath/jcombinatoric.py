from jtools.jconsole import test, red, yellow, blue





def combinations_by_index(n, r, offset=0):
    """
    Return a list of all possible r-length combinations of the INDICES in a hypothetical n-length list. 
    
    These indices may later be mapped to the values in an actual n-length list or other subscriptable object to produce
    the list of all r-length combinations of the actual elements in that subscriptable. 

    Combinations ignore ordering, so 'ab' and 'ba' are not considered distinct combinations in the string 'abhor'.
    However if elements repeat themselves within "items" such as in the string 'antenna', then 'an' and 'na' are 
    legitimately distinct combinations and will both be included.  

    @param n: length of a subscriptable object (str, list, tuple...etc)
    @param r: size of samples
    @param offset: used internally 
    """
    if n < r: # not possible, i.e. 5choose8
        raise ValueError
    if r == 1:
        return [[x] for x in range(offset, n)]
    else:
        perms = []
        for i in range(offset, (n-r)+1):
            sub_combos = combinations_by_index(n, r-1, offset=i+1)
            perms.extend([[i] + x for x in sub_combos])
        return perms
    

def combinations(items, r):
    """
    Return a list of all possible r-length combinations of the elements in "items". These are "combinations without replacement". 

    If items is a string a list of strings is returned. Otherwise a list of lists is returned. 

    Combinations ignore ordering, so 'ab' and 'ba' are not considered distinct combinations in the string 'abhor'.
    However if elements repeat themselves within "items" such as in the string 'antenna', then 'an' and 'na' are 
    legitimately distinct combinations and will both be included.  

    @param items: a subscriptable object (str, list, tuple...etc)
    @param r: size of samples 
    """
    # mapping the indices returned by combinations_by_index() to the values in "items" 
    # avoids a copy of the "items" object being created for each level of recursion. 
    index_combos = combinations_by_index(len(items), r) 
    if isinstance(items, str):
        values = [''.join([items[i] for i in combo]) for combo in index_combos]
    else:
        values = [[items[i] for i in combo] for combo in index_combos]
    return values    


def get_index_permutations(item, n: int) -> list:
    """
    Return a list of all possible r-length combinations of the INDICES in a hypothetical n-length list. 
    
    These indices may later be mapped to the values in an actual n-length list or other subscriptable object to produce
    the list of all r-length combinations of the actual elements in that subscriptable. 

    Combinations ignore ordering, so 'ab' and 'ba' are not considered distinct combinations in the string 'abhor'.
    However if elements repeat themselves within "items" such as in the string 'antenna', then 'an' and 'na' are 
    legitimately distinct combinations and will both be included.  

    @param n: length of a subscriptable object (str, list, tuple...etc)
    @param r: size of samples
    @param offset: used internally 
   
   #  x  x  x      x     x  x   x  x        x
   # [0][1][2][3] [0][1][2][3] [0][1][2][3][4]
   
    """
    pass





if __name__ == '__main__':
    #####USE THIS SCHEME TO TEST PERMUTATIONS WHEN YOU MAKE IT
    items = [1,2,4,6]
    r = 2
    combos = combinations(items, r)
    #report
    print(blue("\n###############"))
    print(combos)
    print(yellow(f'N={len(items)}, r = {r}, object = {items}'))
    print(yellow(f'number of groupings produced: {len(combos)}'))
    print(blue("###############"))