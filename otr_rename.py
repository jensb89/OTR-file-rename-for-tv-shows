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
from datetime import datetime
import time
from shutil import move
from time import localtime
import codecs
from types import *

from Fernsehserien_de_Scraper import Fernsehserien_de_Scraper


class OTR_Rename(object):
    def __init__(self, filename):
        self.file = filename
        self.parseFileInfo()

    def parseFileInfo(self):
        # Get Title, date and so on from filename
        self.extension = os.path.splitext(self.file)[1]
        m = re.search("(.*)_([0-9]{2}\.[0-9]{2}\.[0-9]{2})_([0-9]{2}\-[0-9]{2})_([A-Za-z0-9]+)", self.file)
        title = m.group(1)
        # Check for SxxExx in filename:
        m2=re.search("(S[0-9]{2}E[0-9]{2})",title)
        if type(m2) is not NoneType:
            title = title.split('_'+m2.group(1))[0]
        title = title.split('__')[0] # for US series SeriesName__EpisodeTitle (problems with shows like CSI__NY)

        self.show = title.replace("_",' ')
        self.epdate = m.group(2)
        self.eptime = m.group(3)
        self.sender = m.group(4)
        if self.sender[:2] != 'us':
            self.lang='de'
        else:
            self.lang='us'
        print self.show + ' (' + self.lang + ')'

    def queryEpisodeInfo(self):
        self.scraper = Fernsehserien_de_Scraper(self.show)

        if self.lang == 'us':
            (d,s,e,t) = self.scraper.getEpisodeGuide(lang='us')

        if self.lang == 'de':
            (d,s,e,t,time_list) = self.scraper.getTimeTable(self.sender)

        # Find match in Date
        if not(d[:]):
            idx = False
        else:
            idx = self.searchDate(self.epdate, d)
        # Found match:     
        if str(idx).isdigit():
            if self.lang == 'de':
                idx = self.checkFollowingDateEntry(self.epdate, self.eptime, d, time_list, idx-1 if idx>0 else idx) #Search for closest eptime on the date
            date, season, episode, title = d[idx], s[idx], e[idx], t[idx]
        else: # No match
            date, season, episode, title = None, None, None, None
        
        return date, season, episode, title

    def buildNewFilename(self):
        # Get filename from the scraped webpage
        date, season, episode, title = self.queryEpisodeInfo()
        if None in (date, season, episode, title):
            newfilename = False
        else:
            newfilename = self.show + '.' + 'S' + season + 'E' + episode + '.' + title + self.extension

        return newfilename

    def copy_and_sort(self):
        if not(os.path.isdir(self.show)):
           os.mkdir(self.show)
       
        log = open('log.txt','a')
        lt = localtime()
        jahr, monat, tag, stunde, minute = lt[0:5]
        log.write(str(jahr)+'-'+ str(monat) +'-'+ str(tag) +' '+ str(stunde) +':'+ str(minute) +' : ')
        #log.write(strftime("%Y-%m-%d %H:%I"))
        log.write("input  " + self.file + "\n")

        newfilename = self.buildNewFilename()
        if newfilename != False:
            newfilename = "".join(i for i in newfilename if i not in r'\/:*?"<>|') 
            newpath = self.show + '/' + newfilename
        else:
            newpath = self.show + '/' + self.file
        
        if not(os.path.isfile(newpath)):
            move(self.file, newpath)
            log.write(str(jahr)+'-'+ str(monat) +'-'+ str(tag) +' '+ str(stunde) +':'+ str(minute) +' : ')
            log.write("output " + newpath + "\n\n")
            print self.file + ' moved to ' + newpath
            #log.write(filename + ' was copied to ' + newpath + '\n')       
        
        log.close()


    @staticmethod
    def searchDate(date, date_list): 
        date=datetime.strptime(date,"%y.%m.%d")
        for index, item in enumerate(date_list):
            if item != u'\xa0' and item != '':
                actualdate = datetime.strptime(item,"%d.%m.%Y")
                if actualdate.date() == date.date():
                    return index

    @staticmethod
    def checkFollowingDateEntry(date,stime,date_list,time_list,idx):
        tc = time.strptime(date+' '+stime,"%y.%m.%d %H-%M")  #Time from filename 
        
        actual=time.strptime(date_list[idx]+' '+time_list[idx],"%d.%m.%Y %H:%M")
        
        if idx <= len(date_list)-2:
            after=time.strptime(date_list[idx+1]+' '+time_list[idx+1],"%d.%m.%Y %H:%M")
        else:
            return idx
        
        trynext = True
        while trynext:

            diffactual= abs(time.mktime(actual)-time.mktime(tc))
            diffnext= abs(time.mktime(after)-time.mktime(tc))
            
            if diffactual > diffnext and idx < len(date_list)-2:
                idx=idx+1
                actual = time.strptime(date_list[idx]+' '+time_list[idx],"%d.%m.%Y %H:%M")
                after = time.strptime(date_list[idx+1]+' '+time_list[idx+1],"%d.%m.%Y %H:%M")  
            elif diffactual > diffnext and idx == len(date_list)-2:
                idx=idx+1
                trynext = False
            else:
                trynext = False
                
        return idx


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        otrfile = OTR_Rename(filename)
        filename_new = otrfile.buildNewFilename()
        if filename_new != False:
            print filename_new
    else:
        print 'Usage: ' + sys.argv[0] + ' filename'