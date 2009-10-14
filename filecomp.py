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

def walkdirs(dir1, dir2):
    dirsa = []
    dirsb = []
    ''' Walk directories and build list of similar structures. '''

    # First, fetch a list of directories to compare.

    for directory in os.walk(onedir):
        relativedirname = "/" + re.sub(onedir, "", directory[0])
        dirsa.append(relativedirname)
    
    for directory in os.walk(twodir):
        relativedirname = "/" + re.sub(twodir, "", directory[0])
        dirsb.append(relativedirname)

    # Then compare and return matches for further inspection.
    likedirectories = set(dirsa).intersection(set(dirsb))
    return likedirectories


def complists(dir1, dir2):
    ''' List files in target directories. '''
    print dir1
    print dir2
    dira = []
    dirb = []
    for file in os.listdir(dir1):
        dira.append(file)
    for file in os.listdir(dir2):
        dirb.append(file)

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

def outp(datum):
    if len(datum[0]) > 0:
        print "------------------------------\nItems in \"%s\" and not in \"%s\":" % (onedir, twodir)
        for z in datum[0]:
            print z
        if len(datum[1]) > 0:
            print "------------------------------\nItems in \"%s\" and not in \"%s\":" %(twodir, onedir)
            for z in datum[1]:
                print z
        print "------------------------------"
    if len(datum[2]) > 0:
        comfiles(datum[2], onedir, twodir)


print "#######################################"
print "Comparing \n%s \n%s" % (onedir, twodir)
print "#######################################"

subdirs = walkdirs(onedir, twodir)
setinfo = complists(onedir, twodir)
outp(setinfo)

if len(subdirs) > 0:
    contin = raw_input("[( Recurse through sub-directories? )]")
    if contin == "n":
        exit(0)

for subdir in subdirs:
    setinfo = complists(onedir + subdir.lstrip("/"), twodir + subdir.lstrip("/"))
    outp(setinfo)

