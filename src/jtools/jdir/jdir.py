import os, sys
import os.path as opath
from jtools.jconsole import yes_no


# rewrite to handle symlinks correctly
def scandirsize(pathstring):
    """recursively calculate a directory's size in bytes."""
    size = 0
    for x in os.scandir(pathstring):
        if x.is_symlink():
            continue # os.path.getsize() fails w/ FileNotFound for broken symlinks and it's not clear if its returning size of the link or the link's target. 
        size += opath.getsize(x)
                
        if x.is_dir():
            size += scandirsize(x.path)
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

def formatbytes(bytesize, unit="KB"):
    """Convert storage size from bytes to the desired unit and return a formatted string"""
    unit = unit.upper()
    lookup = {"B": 1, "KB": pow(2, 10), "MB": pow(2, 20), "GB": pow(2, 30), "TB": pow(2, 40)}
    return '{0:.2f}'.format(bytesize/lookup[unit]) + ' ' + unit

