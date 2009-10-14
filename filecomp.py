#!/usr/bin/env python
import os,sys,hashlib,re

"""
/*********************************\
           filecomp.py
     Will compare files in two
      directories for missing
      and/or mismatched files
       (based upon md5sums).

      Currently a bit sloppy
       and lacks recursion.

     Written by Benjamin.Sauls
\*********************************/
"""

""" Confirm input (very) briefly """
if len(sys.argv) != 3:
    print "You're doing something wrong.\nUsage: %s dir1 dir1" % sys.argv[0]
    exit(2)

(onedir, twodir) = sys.argv[1], sys.argv[2]

def sumfile(fobj):
    '''Returns an md5 hash for an object with read() method.'''
    m = hashlib.md5()
    while True:
        d = fobj.read(8096)
        if not d:
            break
        m.update(d)
    return m.hexdigest()

def md5sum(fname):
    '''Returns md5 of a file, or stdin if fname is "-".'''
    if fname == '-':
        ret = sumfile(sys.stdin)
    else:
        try:
            f = file(fname, 'rb')
        except:
            return 'Failed to open file'
        ret = sumfile(f)
        f.close()
    return ret

def complists(dir1, dir2):
    dirsa = []
    dirsb = []
    ''' List files in target directories. '''

    """
    Trying to make recursion happen. So far, to no avail.
    """
    # First, fetch a list of directories to compare.

    for directory in os.walk(onedir):
        relativedirname = "/" + re.sub(onedir, "", directory[0])
        dirsa.append(relativedirname)
    
    for directory in os.walk(twodir):
        relativedirname = "/" + re.sub(twodir, "", directory[0])
        dirsb.append(relativedirname)

    # Then compare and return matches for further inspection.
    likedirectories = set(dirsa).intersection(set(dirsb))
    
    ''' Compare files and display disparities. '''
    indir1 = set(dira).difference(set(dirb))
    indir2 = set(dirb).difference(set(dira))
    return (indir1, indir2, set(dira).intersection(set(dirb)))

def comfiles(files, onedir, twodir):
    firstdir = {}
    secdir = {}
    for f in files:
        of = onedir + "\\" + f
        sf = twodir + "\\" + f
        firstdir[f] = md5sum(of)
        secdir[f] = md5sum(sf)
    for x in firstdir:
        if firstdir[x] != secdir[x]:
            print "File %s does not match!" % x

print "#######################################"
print "Comparing \n%s \n%s" % (onedir, twodir)
print "#######################################"

setinfo = complists(onedir, twodir)
if len(setinfo[0]) > 0:
    print "------------------------------\nItems in \"%s\" and not in \"%s\":" % (onedir, twodir)
    for z in setinfo[0]:
            print z
    if len(setinfo[1]) > 0:
        print "------------------------------\nItems in \"%s\" and not in \"%s\":" %(twodir, onedir)
        for z in setinfo[1]:
            print z
    print "------------------------------"
    
if len(setinfo[2]) > 0:
       comfiles(setinfo[2], onedir, twodir)
