#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
OTR file rename for tv-shows
Extract all information from the (decoded) otrkey file name (onlinetvrecorder.com)
and use the website fernsehserien.de to rename the file with the episode and season info  

@author: Jens
"""
import re
import os
from shutil import move
import otr_rename

def getFileInfo(filename):
    extension = os.path.splitext(filename)[1]

    m=re.search("(.*)_([0-9]{2}\.[0-9]{2}\.[0-9]{2})_([0-9]{2}\-[0-9]{2})_([A-Za-z0-9]+)", filename)
    title = m.group(1)
    title = title.split('__')[0] # for US series SeriesName__EpisodeTitle (problems with shows like CSI__NY)
    title = title.replace("_",' ')
    seriesdate = m.group(2)
    seriestime = m.group(3)
    sender = m.group(4)
    
    return title,seriesdate,sender,extension,seriestime

def copysort(filename):
    title,seriesdate,sender,extension,seriestime = getFileInfo(filename)
    if not(os.path.isdir(title)):
       os.mkdir(title)
   
    log = open('log.txt','a')
    newfilename = otr_rename.buildNewFileName(filename)
    if newfilename != False:
        move(filename,title+'/'+newfilename)
        log.write(filename + ' was copied to ' + title+'/'+newfilename + '\n')
    else:
        move(filename,title+'/'+filename)
        log.write(filename + ' was copied to ' + title+'/'+filename + '\n')
    
    log.close()

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        copysort(filename)
    else:
        print 'Usage: ' + sys.argv[0] + ' filename'
