"""functions to help with filesystem related tasks"""
import os, sys
import os.path as opath
from jtools.jconsole import yes_no, test


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


def get_all_files(pathstring, combined=False):
    """recurse into pathstring to generate a list of all files and subdirectories below that point.
    - Returns a list of lists like: [[subdirectories], [sub-files]] ()
    - if combined is True, combine the dirs and files return lists into one list"""
    dirs = []
    files = []
    for dirpath, dirnames, filenames in os.walk(pathstring):
        dirs += [opath.join(dirpath, name) for name in dirnames]
        files += [opath.join(dirpath, name) for name in filenames]
    if combined:
        return dirs + files
    else:
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
    """compare two directory trees beginning at dir1 and dir2 respectively in order to find which dirs/files are unique to each tree.
    - returns a tuple like ([dir1_uniques],[dir2_uniques]) the list [dir1_uniques] contains the paths of all dirs/files that appear only in dir1. 
    - intended use is to compare two similar directory structures that more or less mirror each other but have minor differences. 
    - treats dir1 and dir2 as root directories and compares their members relative to those roots. i.e. "/some_path/dir1/subdir/filex" "/some_other_path/dir2/subdir/filex" are the same file. 
    - pathstrings are compared, NOT file contents. 
    """
    # list all dirs/files and remove first part of their paths to facilitate str comparison later. 
    sep = os.path.sep
    ls1 = [ x.replace(dir1, '').lstrip(sep)    for x in    get_all_files(dir1, combined=True) ]
    ls2 = [ x.replace(dir2, '').lstrip(sep)    for x in    get_all_files(dir2, combined=True) ]
    # find dirs files unique to each tree and add the first part of their path back on. 
    u1 = sorted([ opath.join(dir1, x)    for x in    ls1     if x not in ls2])
    u2 = sorted([ opath.join(dir2, x)    for x in    ls2     if x not in ls1])
    return u1, u2


