#!/usr/bin/env python

import shutil
import os
import time

"""Copy specified files or folders into one directory with added time stamp."""

# this script uses shutil.copytree and shutil.copy2 to make the backups
# note that there are also copy_tree and copy_file in distutils.dir_util package

## PARAMETERS ##
# list of files and folders to backup
originals = [r'c:\some\folder', r'c:\some\file.ext', r'C:\some\other\file.png']
# folder to backup to (a single folder to keep this script simple)
backupto = r'D:\backups'
# a stamp to be added to the backup of original paths (could be '' too)
stamp = '_expired' + time.strftime('%Y%m%d%H%M%S')
# file path to write out log into in the end
logpath = r'D:\backups\log.txt'
# mode to use for the log file, either 'w' for write or 'a' for append
logmode = 'w'
# replace separators in original path? If True, colons will be removed.
# True enables backups like c:/a/a/a and c:/a/b/a -> c-a-a-a and c-a-b-a
replaceSep = True
# string to replace separators in the original path
sepReplace = '-'
## PARAMETERS END ##

# list for logging errors
logging = []

def getPathType(pth):
    """Determine what type of path pth is"""
    if os.path.isdir(pth):
        return 'directory'
    elif os.path.isfile(pth):
        return 'file'
    elif os.path.islink(pth):
        return 'link'
    else:
        return 'unknown'

def addStamp(path, stamp="", period='.'):
    """Insert stamp before the first period of basename of path. I no period found, stamp is appended to the end of path"""
    dname = os.path.dirname(path)
    bname = os.path.basename(path)
    if bname.find(period) < 0:
        return path + stamp
    # insert stamp
    bsplit = bname.split(period)
    bname = bsplit[0] + str(stamp) + str(period) + period.join(bsplit[1:])
    return os.path.join(dname, bname)

def makeBackup(source, destination):
    """make a backup of source as destination"""
    ptype = getPathType(source)
    if ptype == 'directory':
        # print(source, destination) # debug
        shutil.copytree(source, destination)
    elif ptype == 'file':
        # print(source, destination) # debug
        shutil.copy2(source, destination)
    else:
        raise Exception('Backup of path type '+ str(ptype) + ' is not supported!')

def listToFile(alist, filepath, mode="a", separator="\t"):
    """Write alist like [['abc','def'],['ghi',['jkl']] into a file filepath"""
    try:
        afile = open(filepath, mode)
        for i in alist:
            row = []
            for j in i:
                j = j.replace("\n", " ").replace("\t", " ")
                row.append(j)
            afile.write(separator.join(row) + "\n")
    except Exception as ex:
        print str(ex)
    finally:
        if 'afile' in dir():
            afile.close()

# body of the program
if __name__ == '__main__':
    try:
        for b in originals:
            logitem = [time.strftime('%Y%m%d%H%M%S'), b]
            dest= addStamp(os.path.basename(b), stamp)
            if replaceSep:
                dest = os.path.join(os.path.dirname(b), dest)
                dest = dest.replace("\\", sepReplace).replace("/", sepReplace).replace(":", "")
            dest = os.path.join(backupto, dest)
            try:
                makeBackup(b, dest) # the crititcal function call
                logitem.append(str(dest))
            except Exception as ex:
                logitem.append(str(ex))
            logging.append(logitem)
        listToFile(logging, logpath, logmode) # write results to output file
    except Exception as err:
        print(str(err))
