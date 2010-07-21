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
    print "You're doing something wrong.\nUsage: %s dir1 dir2" % sys.argv[0]
    exit(2)

# Pad/escape input. This is weak for now, any even number of terminating
# slashes still causes problems.
(onedir, twodir) = sys.argv[1], sys.argv[2]
if re.search("\\\\$", onedir) != None:
    onedir = onedir + "\\"
if re.search("\\\\$", twodir) != None:
    twodir = twodir + "\\"

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

""" Abandon all hope, ye who enter here """

def walkdirs(dir1, dir2):
    dirsa = []
    dirsb = []

    ''' Walk directories and build list of similar structures. '''
    # First, fetch a list of directories to compare.

    for directory in os.walk(dir1):
        relativedirname = "/" + re.sub(dir1, "", directory[0])
        if relativedirname != "/":
            dirsa.append(relativedirname)
    
    for directory in os.walk(dir2):
        relativedirname = "/" + re.sub(dir2, "", directory[0])
        if relativedirname != "/":
            dirsb.append(relativedirname)

    # Return matches for further inspection.
    return set(dirsa).intersection(set(dirsb))


def complists(dir1, dir2):
    print "#######################################"
    print "Comparing \n%s \n%s" % (dir1, dir2)
    print "#######################################"
    ''' List files in target directories. '''
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
            print "File %s in both targets but does not match!" % x
    print "\n"

def outp(datum, fdir=onedir, sdir=twodir):
    if len(datum[0]) > 0:
        print "Items in \"%s\" and not in \"%s\":" % (fdir, sdir)
        for z in datum[0]:
            print "   " + z
        print "\n------------------------------"
    if len(datum[1]) > 0:
        print "Items in \"%s\" and not in \"%s\":" %(sdir, fdir)
        for z in datum[1]:
            print "   " + z
        print "\n------------------------------"
    if len(datum[2]) > 0:
        comfiles(datum[2], fdir, sdir)


subdirs = walkdirs(onedir, twodir)
setinfo = complists(onedir, twodir)
outp(setinfo)

for subdir in subdirs:
    setinfo = complists(onedir + subdir.lstrip("/"), twodir + subdir.lstrip("/"))
    outp(setinfo, onedir + subdir.lstrip("/"), twodir + subdir.lstrip("/"))
