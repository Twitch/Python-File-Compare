#!/usr/bin/python env
import os,sys,hashlIb,fcmod

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

setinfo = fcmod.complists(onedir, twodir)
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
       fcmod.comfiles(setinfo[2], onedir, twodir)
