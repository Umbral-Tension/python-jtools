import os, sys
import os.path as opath
from jtools.jconsole import yes_no



# rewrite using scandir and include directories
def get_dir_size(pathstring):
    """Calculate a directory's size in bytes."""
    if not (opath.exists(pathstring) and opath.isdir(pathstring)):
        return None
    size = 0
    for dirpath, dirnames, filenames in os.walk(pathstring):
        for f in filenames:
            size += opath.getsize(opath.join(dirpath, f))
    return size


def get_all_filesystem_entries(pathstring, do_files=True, do_dirs=True):
    """return a list of paths of all sub-directories and files below pathstring"""
    ls = []
    for dirpath, dirnames, filenames in os.walk(pathstring):
        if do_files:
            ls += [opath.join(dirpath, name) for name in filenames]
        if do_dirs:    
            ls += [opath.join(dirpath, name) for name in dirnames]
    return ls


def get_all_subdirs(pathstring):
    return get_all_filesystem_entries(pathstring, do_files=False)


def get_all_files(pathstring):
    return get_all_filesystem_entries(pathstring, do_dirs=False)
            
                
def get_file_count(pathstring, count=0):
    """Recursively count the number of files in a directory."""
    for dir_entry in os.scandir(pathstring):
        if dir_entry.is_dir():
            count = get_file_count(dir_entry.path, count)
        else:
            count += 1
    return count

def file_count_walk(pathstring, count=0):
    return

# Rewrite
def dup_rename(file_name, pathstring):
    """Return an alternative filename if 'file_name' already exists.
    looks for an available filename using the pattern name_#
    """
    ls = os.listdir(pathstring)
    if file_name not in ls:
        return file_name
    else:
        suffix = 2
        tup = file_name.rsplit('.', 1)
        name = tup[0]
        ext = tup[1]
        while True:
            rename = name + '_' + str(suffix) + '.' + ext
            if rename not in ls:
                return rename
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

