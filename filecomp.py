#!/usr/bin/env python
import os,sys,hashlib,re

"""
/*********************************\
           filecomp.py
     Will compare files in two
      directories for missing
      and/or mismatched files
       (based on md5sums).

      Currently a bit sloppy.

     Written by Twitch(Ben)
\*********************************/
"""

""" Confirm input (very) briefly """
if len(sys.argv) != 3:
    print "You're doing something wrong.\nUsage: %s dir1 dir2" % sys.argv[0]
    exit(2)

(onedir, twodir) = sys.argv[1], sys.argv[2]


''' Determine OS type and use appropriate path seperator. '''
if os.name == "posix":
	pathsep = "/"
elif os.name == "nt":
	pathsep = "\\"
else:
	print "I haven't the faintest idea what operating system you have run me on, but I have no intentions of attempting to work under these conditions!"
	exit(2)


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
	''' This creates relative names for the sub-directories and adds them to the list. '''
	for directory in os.walk(dir1):
		relativedirname = pathsep + re.sub(dir1, "", directory[0])
		if relativedirname != pathsep:
			dirsa.append(relativedirname)
    
	for directory in os.walk(dir2):
		relativedirname = pathsep + re.sub(dir2, "", directory[0])
		if relativedirname != pathsep:
			dirsb.append(relativedirname)

	# Return matches for further inspection.
	return set(dirsa).intersection(set(dirsb))

def complists(dir1, dir2):
	''' Compare list of files in the directories. '''
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

	''' Compare files and return disparities. '''
	indir1 = set(dira).difference(set(dirb))
	indir2 = set(dirb).difference(set(dira))
	return (indir1, indir2, set(dira).intersection(set(dirb)))

def comfiles(files, onedir, twodir):
	''' Compare files which appear in both directories. '''
	firstdir = {}
	secdir = {}
	# Create an absolute path to them from the relative filename and get the md5.
	for f in files:
		of = onedir + pathsep + f
		sf = twodir + pathsep + f
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
	else:
		print "No unique items in \"%s\"" % (fdir)
		
	if len(datum[1]) > 0:
		print "Items in \"%s\" and not in \"%s\":" %(sdir, fdir)
		for z in datum[1]:
			print "   " + z
		print "\n------------------------------"
	else:
		print "No unique items in \"%s\"" % (sdir)
	
	if len(datum[2]) > 0:
		comfiles(datum[2], fdir, sdir)

subdirs = walkdirs(onedir, twodir)
setinfo = complists(onedir, twodir)
outp(setinfo)

# Perform recursion through directories returned by the walkdirs() function.

for subdir in subdirs:
    setinfo = complists(onedir + subdir, twodir + subdir)
    outp(setinfo, onedir + subdir, twodir + subdir)
