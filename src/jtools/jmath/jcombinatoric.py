from jtools.jconsole import test, red, yellow, blue

def combinations_by_index(n, r, offset=0):
    """
    Return a list of all possible r-length combinations of the INDICES in a hypothetical n-length list. These are combinations without replacement.
    
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
    @param r: length of combinations 
    """
    # mapping the indices returned by combinations_by_index() to the values in "items" 
    # avoids a copy of the "items" object being created for each level of recursion. 
    index_combos = combinations_by_index(len(items), r) 
    if isinstance(items, str):
        value_combos = [''.join([items[i] for i in combo]) for combo in index_combos]
    else:
        value_combos = [[items[i] for i in combo] for combo in index_combos]
    return value_combos    

def orderings(items):
    """convenience function"""
    return permutations(items, len(items))

def orderings_by_index(n, index_set=None):
    """
    return a list of all possible orderings of the INDICES in a hypothetical n-length list. 

    These indices may later be mapped to the values in an actual n-length list or other subscriptable object to produce the list
    of all possible orderings of the items in that subscriptable. 
    """
    
    if index_set is None:
        index_set = list(range(n))
    
    length = len(index_set)
    # included for completeness, even though I shouldn't be asking for the orderings of a single item list. 
    if length == 1:
        return [[0]]
    # recursive base case is trivial case of all orderings of the last two indices of a list.
    elif length == 2:
        return [[index_set[0], index_set[1]], [index_set[1], index_set[0]]]
    else:
        orderings = []
        # Pick one element, set it at the first position. Combine it with all possible orderings of the remaining subset of elements. 
        for i in index_set:
            subset = index_set.copy()
            subset.remove(i)
            orderings.extend([[i] + x for x in orderings_by_index(n, subset)])
        
    return orderings

def permutations_by_index(n, r):
    """
    Return a list of all possible r-length permutations of the INDICES in a hypothetical n-length list. These are permutations without replacement.
    
    These indices may later be mapped to the values in an actual n-length list or other subscriptable object to produce
    the list of all r-length permutations of the actual elements in that subscriptable. 

    Permutations do NOT ignore ordering, so 'ab' and 'ba' are considered distinct permutations.

    @param n: length of a subscriptable object (str, list, tuple...etc)
    @param r: size of samples
    """    

    # find all orderings of a r indices. 
    orderings = orderings_by_index(r)
    # when n==r permutations simplifies to all the ORDERINGS of the items in the list. No need to find rlength combinations first. 
    if n == r:
        return orderings
    combinations = combinations_by_index(n, r)
    
    permutations = []
    for x in combinations:
        for o in orderings:
            permutations.extend([[x[i] for i in o]])
    return permutations
    
def permutations(items, r):
    """
    Return a list of all possible r-length permutations of the elements in "items". These are "permutations without replacement". 

    If items is a string a list of strings is returned. Otherwise a list of lists is returned. 

    Permutations do NOT ignore ordering, so 'ab' and 'ba' are considered distinct permutations. 

    @param items: a subscriptable object (str, list, tuple...etc)
    @param r: length of permutations 
    """
    index_perms = permutations_by_index(len(items), r) 
    if isinstance(items, str):
        value_perms = [''.join([items[i] for i in perm]) for perm in index_perms]
    else:
        value_perms = [[items[i] for i in perm] for perm in index_perms]
    return value_perms    


if __name__ == '__main__':

    ##### testing
    items = 'abcde'
    r = 5
    groupings = permutations(items, r)
    #report
    print(blue("\n###############"))
    print(groupings)
    print(yellow(f'N={len(items)}, r = {r}, object = {items}'))
    print(yellow(f'number of groupings produced: {len(groupings)}'))
    print(blue("###############"))