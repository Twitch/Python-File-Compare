#!/usr/bin/python env
import os,sys,hashlib

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
    dira = []
    dirb = []
    ''' List files in target directories. '''
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
