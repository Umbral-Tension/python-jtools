import os, sys
from os import path


# Returns a path string with all slashes removed. Useful for comparing path strings whose slash direction
# is unknown. I.E two path strings may refer to the same location but have different slash directions, and
# a comparison would yield False, which is probably undesirable.
def no_slash(pathstring):
    return pathstring.replace('\\', '').replace('/', '')


# Calculate size of a directory in bytes (doesn't SEEM to be a method that does this directly in os or shutil)
# should add exception handling for if aPath does not exist.
def get_dir_size(pathstring):
    if not os.path.isdir(pathstring):
        return -1
    size = 0
    for currPath, directory, filenames, in os.walk(pathstring):
        for f in filenames:
            size += os.path.getsize(os.path.join(currPath, f))
    return size

def get_file_size(pathstring):
    return path.getsize(norm(pathstring))


def delete_empty_directories(pathstring):
    """ deletes all empty subdirectories of pathstring """
    pathstring = norm(pathstring)
    if not path.exists(pathstring):
        return
    for currpath, dirs, files, in os.walk(pathstring):
        if currpath != pathstring:
            os.rmdir(currpath)



# Should replace with something built in as I'm sure there's something available.
# Counts the number of files in a directory
def get_file_count(pathstring, count=0):
    for dir_entry in os.scandir(pathstring):
        if dir_entry.is_dir():
            count = get_file_count(dir_entry.path, count)
        else:
            count += 1
    return count


# Checks if a file name already exists in a directory and if so,
# looks for an available file name using the pattern name_#
def dup_rename(file_name, pathstring):
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


# normalize path strings. change / to \, convert to lowercase, collapse redunant ..'s
def norm(pathstring):
    return path.normpath(path.normcase(pathstring))


def get_parent_dir(pathstring):

    return path.split(norm(pathstring))[0]


# Checks whether the given directory is one of the large top
# level directors (root like C:\ are detected via the path's length)
def is_danger_dir(pathstring):
    pathstring = str(norm(pathstring))
    # reject root dirs like 'C:\'
    if len(pathstring) < 4:
        return True
    # reject all immeidate subdirectories of c:/
    if get_parent_dir(pathstring) == norm('c:/'):
        return True
    # reject network locations
    if pathstring.startswith(('//', '\\\\')):
        return True
    # reject large user directories
    userdirectories = ('documents', 'downloads', 'desktop', 'google drive', 'downloads', 'videos', 'music', 'pictures')
    parts = path.split(pathstring)
    if parts[0] == norm(os.getenv('userprofile')) and parts[1] in userdirectories:
        return True

    return False


def formatbytes(bytesize, unit = "KiB"):
    unit = unit.upper()
    lookup = {"B": 1, "KB": pow(2, 10), "MB": pow(2, 20), "GB": pow(2, 30), "TB": pow(2, 40)}
    return '{0:.2f}'.format(bytesize/lookup[unit]) + ' ' + unit

