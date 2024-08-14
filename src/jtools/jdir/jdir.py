import os, sys
import os.path as opath
from jtools.jconsole import yes_no


def formatbytes(bytesize, unit="KB"):
    """Convert storage size from bytes to the desired unit and return a formatted string"""
    unit = unit.upper()
    lookup = {"B": 1, "KB": pow(2, 10), "MB": pow(2, 20), "GB": pow(2, 30), "TB": pow(2, 40)}
    return '{0:.2f}'.format(bytesize/lookup[unit]) + ' ' + unit


# rewrite to handle symlinks correctly
def get_size(pathstring):
    """recursively calculate a directory's size in bytes."""
    size = 0
    for x in os.scandir(pathstring):
        if x.is_symlink():
            continue # os.path.getsize() fails w/ FileNotFound for broken symlinks and it's not clear if its returning size of the link or the link's target. 
        size += opath.getsize(x)
                
        if x.is_dir():
            size += get_size(x.path)
    return size


def get_all_files(pathstring):
    """recurse into pathstring to generate a list of all files and subdirectories below that point.
    Returns a list of lists like: [[subdirectories], [sub-files]] ()"""
    dirs = []
    files = []
    for dirpath, dirnames, filenames in os.walk(pathstring):
        dirs += [opath.join(dirpath, name) for name in dirnames]
        files += [opath.join(dirpath, name) for name in filenames]
    return [dirs, files]


def get_file_count(pathstring):
    """recursively count the number of files and sub-directories below pathstring
     returned as a tupe (num_dirs, num_files) """
    d, f = 0, 0
    for dirpath, dirnames, filenames in os.walk(pathstring):
        d += len(dirnames)
        f += len(filenames)
    return (d,f)


def dup_rename(pathstring):
    """Return a path with an alternatively named last component (dirname/filename) 
    if pathstring already exists. Looks for an available path using the pattern name_#
    """
    if not opath.exists(pathstring):
        return pathstring
    else:
        ls = os.listdir(opath.dirname(pathstring))
        basename, ext = opath.basename(pathstring), ""
        if opath.isfile(pathstring):
            basename, ext = opath.splitext(basename)
    
        suffix = 2
        while True:
            newname = basename + '_' + str(suffix) + ext
            if newname not in ls:
                return opath.join(opath.dirname(pathstring), newname)
            else:
                suffix += 1

# Rewrite
def is_danger_dir(pathstring):
    """Check whether the given directory is one of the large top lvl directories."""
    pathstring = str(pathstring)
    # reject root dirs like 'C:\'
    if len(pathstring) < 4:
        return True
    # reject all immeidate subdirectories of c:/
    if get_parent_dir(pathstring) == 'c:/':
        return True
    # ask user about network location
    if pathstring.startswith(('//', '\\\\')):
        return not yes_no('This is a network location. Is:{\n' + pathstring + '\n} safe to operate on?')
        
    # reject large user directories
    userdirectories = ('documents', 'downloads', 'desktop', 'google drive', 'downloads', 'videos', 'music', 'pictures')
    parts = opath.split(pathstring)
    if parts[0] == os.getenv('userprofile') and parts[1] in userdirectories:
        return True

    return False


def diff(dir1, dir2):
    """compare two directories to determin which dirs/files are unique to each directory."""
    ls1 = get_all_files(dir1)
    ls1 = ls1[0] + ls1[1]
    ls2 = get_all_files(dir2)
    ls2 = ls2[0] + ls2[1]
    

    ls1a = [x.replace(dir1, '').lstrip('/') for x in ls1]
    ls2a = [x.replace(dir2, '').lstrip('/') for x in ls2]
    
    # test(ls1a, ls2a)
    # for x in ls1a:
    #     if 
    #     if x not in ls2a:
            # print(x)
    u1 = [x for x in ls1a if x not in ls2a]
    u2 = [x for x in ls2a if x not in ls1a]

    test(u1, u2)
    
    return ls1a, ls2a

from jtools.jconsole import test
dir1 = '/media/jeremy/internal_6TB/rsync_backups/2024-08-09@22:05:10_(Full)'
dir2 = '/media/jeremy/internal_6TB/rsync_backups/2024-08-09@22:24:06_(Incremental)'

d = diff(dir1, dir2)
# test(d)
# import sys
# ls = ''
# for x in range(100000000):
#     ls+=str(x)
# print(formatbytes(sys.getsizeof(ls), 'MB'))